from __future__ import annotations

from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.news_item import NewsItem
from app.models.refresh_job import RefreshJob
from app.models.source import Source
from app.services.classify.keyword_classifier import classify_text
from app.services.parser.normalizer import normalize_item
from app.services.source_registry import DEFAULT_SOURCES


def parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return parsedate_to_datetime(value)
    except Exception:  # noqa: BLE001
        return None


def seed_sources(db: Session) -> int:
    created = 0
    for item in DEFAULT_SOURCES:
        exists = db.query(Source).filter(Source.url == item["url"]).first()
        if exists:
            continue
        db.add(Source(**item))
        created += 1
    db.commit()
    return created


def store_items(db: Session, source: Source, raw_items: list[dict[str, Any]]) -> int:
    created = 0
    for raw_item in raw_items:
        normalized = normalize_item(raw_item)
        if not normalized.get("url") or not normalized.get("title"):
            continue
        exists = db.query(NewsItem).filter(NewsItem.url == normalized["url"]).first()
        if exists:
            continue
        category, scores = classify_text(normalized["title"], normalized.get("summary", ""))
        score = sum(scores.values()) + 1
        db.add(
            NewsItem(
                source_id=source.id,
                title=normalized["title"],
                normalized_title=normalized.get("normalized_title"),
                summary=normalized.get("summary"),
                url=normalized["url"],
                author=normalized.get("author"),
                published_at=parse_datetime(normalized.get("published_at")),
                category=category or source.category_default,
                language=normalized.get("language", "zh"),
                content_hash=normalized.get("content_hash"),
                raw_score=str(score),
                raw_payload=raw_item,
            )
        )
        created += 1
    db.commit()
    return created


def create_refresh_job(
    db: Session,
    trigger_type: str,
    status: str,
    message: str,
    stats_payload: dict | None = None,
    error_count: int = 0,
) -> RefreshJob:
    job = RefreshJob(
        trigger_type=trigger_type,
        status=status,
        started_at=datetime.utcnow(),
        finished_at=datetime.utcnow(),
        message=message,
        stats_payload=stats_payload,
        error_count=error_count,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
