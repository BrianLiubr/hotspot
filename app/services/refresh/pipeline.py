from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.source import Source
from app.services.clustering import rebuild_clusters
from app.services.fetchers.rss_fetcher import RSSFetcher
from app.services.storage import create_refresh_job, seed_sources, store_items


async def collect_source_items(source: Source | dict[str, Any], limit_per_source: int = 10) -> list[dict[str, Any]]:
    source_payload = {
        "name": source.name if hasattr(source, "name") else source["name"],
        "url": source.url if hasattr(source, "url") else source["url"],
        "max_items": limit_per_source,
    }
    fetcher = RSSFetcher()
    return await fetcher.fetch(source_payload)


async def run_refresh(db: Session, trigger_type: str = "manual", limit_per_source: int = 5) -> dict[str, Any]:
    started_at = datetime.utcnow().isoformat()
    seed_sources(db)
    sources = db.query(Source).filter(Source.enabled.is_(True)).all()

    total_created = 0
    errors: list[dict[str, str]] = []

    for source in sources:
        if source.type != "rss":
            continue
        try:
            raw_items = await collect_source_items(source, limit_per_source=limit_per_source)
            total_created += store_items(db, source, raw_items)
        except Exception as exc:  # noqa: BLE001
            errors.append({"source": source.name, "error": str(exc)})

    cluster_count = rebuild_clusters(db)
    message = f"刷新完成，新增 {total_created} 条记录，聚合 {cluster_count} 个事件"
    if errors:
        message += f"，失败源 {len(errors)} 个"

    job = create_refresh_job(
        db,
        trigger_type=trigger_type,
        status="success" if not errors else "partial_success",
        message=message,
        stats_payload={"created": total_created, "clusters": cluster_count, "errors": errors},
    )

    return {
        "id": job.id,
        "trigger_type": trigger_type,
        "status": job.status,
        "started_at": started_at,
        "finished_at": datetime.utcnow().isoformat(),
        "message": message,
        "count": total_created,
        "clusters": cluster_count,
        "errors": errors,
    }
