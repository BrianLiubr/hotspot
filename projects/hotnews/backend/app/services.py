from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Iterable

from dateutil import parser as date_parser
from sqlalchemy.orm import Session

from app.config import TIMEZONE
from app.models import CollectionRun, NewsItem, Source


@dataclass
class CollectedItem:
    source_name: str
    title: str
    summary: str | None
    url: str
    published_at: datetime | None
    rank_score: float | None = None
    category: str | None = None


class CollectorProtocol:
    name: str
    source_type: str
    base_url: str | None

    def collect(self) -> list[CollectedItem]: ...


def normalize_datetime(value: datetime | str | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = date_parser.parse(value)
        except Exception:
            return None
    if value.tzinfo is None:
        return value.replace(tzinfo=TIMEZONE)
    return value.astimezone(TIMEZONE)


def get_query_date(input_date: str | None) -> date:
    now = datetime.now(TIMEZONE)
    if not input_date:
        return (now - timedelta(days=1)).date()
    return date.fromisoformat(input_date)


def end_of_day(target_date: date) -> datetime:
    return datetime.combine(target_date, time(23, 59, 59), tzinfo=TIMEZONE)


def ensure_source(db: Session, collector: CollectorProtocol) -> Source:
    source = db.query(Source).filter(Source.name == collector.name).first()
    if source:
        source.type = collector.source_type
        source.base_url = collector.base_url
        source.enabled = True
        db.add(source)
        db.commit()
        db.refresh(source)
        return source

    source = Source(
        name=collector.name,
        type=collector.source_type,
        enabled=True,
        base_url=collector.base_url,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def content_hash(title: str, url: str) -> str:
    return hashlib.sha256(f"{title}|{url}".encode("utf-8")).hexdigest()


def save_collected_items(db: Session, source: Source, items: Iterable[CollectedItem]) -> int:
    saved = 0
    now = datetime.now(TIMEZONE)
    for item in items:
        existing = db.query(NewsItem).filter(NewsItem.url == item.url).first()
        if existing:
            existing.title = item.title
            existing.summary = item.summary
            existing.published_at = normalize_datetime(item.published_at)
            existing.rank_score = item.rank_score
            existing.category = item.category
            existing.collected_at = now
            db.add(existing)
            saved += 1
            continue

        db_item = NewsItem(
            title=item.title,
            summary=item.summary,
            url=item.url,
            source_id=source.id,
            published_at=normalize_datetime(item.published_at),
            rank_score=item.rank_score,
            category=item.category,
            content_hash=content_hash(item.title, item.url),
            collected_at=now,
        )
        db.add(db_item)
        saved += 1

    db.commit()
    return saved


def record_run(db: Session, source_name: str, status: str, item_count: int, error_message: str | None = None) -> None:
    run = CollectionRun(
        source_name=source_name,
        run_time=datetime.now(TIMEZONE),
        status=status,
        item_count=item_count,
        error_message=error_message,
    )
    db.add(run)
    db.commit()


def query_hotnews(db: Session, target_date: date, limit: int, source_name: str | None = None):
    cutoff = end_of_day(target_date)
    query = db.query(NewsItem, Source.name).join(Source, NewsItem.source_id == Source.id)
    query = query.filter((NewsItem.published_at.is_(None)) | (NewsItem.published_at <= cutoff))
    if source_name:
        query = query.filter(Source.name == source_name)
    query = query.order_by(NewsItem.rank_score.desc().nullslast(), NewsItem.published_at.desc().nullslast(), NewsItem.collected_at.desc())
    return query.limit(limit).all()
