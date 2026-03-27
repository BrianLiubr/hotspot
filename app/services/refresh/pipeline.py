from __future__ import annotations

from datetime import datetime
from typing import Any

from app.services.classify.keyword_classifier import classify_text
from app.services.fetchers.rss_fetcher import RSSFetcher
from app.services.parser.normalizer import normalize_item
from app.services.source_registry import DEFAULT_SOURCES


async def collect_preview_items(limit_per_source: int = 5) -> list[dict[str, Any]]:
    fetcher = RSSFetcher()
    collected: list[dict[str, Any]] = []

    for source in DEFAULT_SOURCES:
        source_payload = {**source, "max_items": limit_per_source}
        try:
            raw_items = await fetcher.fetch(source_payload)
        except Exception as exc:  # noqa: BLE001
            collected.append(
                {
                    "title": f"抓取失败：{source['name']}",
                    "summary": str(exc),
                    "url": source["url"],
                    "category": source["category_default"],
                    "source": source["name"],
                    "published_at": None,
                    "score": 0,
                    "related_count": 0,
                    "error": True,
                }
            )
            continue

        for item in raw_items:
            normalized = normalize_item(item)
            category, scores = classify_text(normalized["title"], normalized.get("summary", ""))
            normalized["category"] = category or source["category_default"]
            normalized["source"] = source["name"]
            normalized["score"] = sum(scores.values()) + 1
            normalized["related_count"] = 1
            collected.append(normalized)

    return collected


async def run_refresh(trigger_type: str = "manual") -> dict[str, Any]:
    started_at = datetime.utcnow().isoformat()
    items = await collect_preview_items()
    return {
        "trigger_type": trigger_type,
        "status": "success",
        "started_at": started_at,
        "finished_at": datetime.utcnow().isoformat(),
        "message": f"预览抓取完成，共处理 {len(items)} 条记录",
        "items": items,
    }
