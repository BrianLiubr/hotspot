from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.event_cluster import EventCluster
from app.models.news_item import NewsItem
from app.models.refresh_job import RefreshJob
from app.models.source import Source


def list_hot_items(db: Session, limit: int = 20):
    return db.query(NewsItem).order_by(desc(NewsItem.fetched_at)).limit(limit).all()


def list_latest_items(db: Session, limit: int = 20):
    return db.query(NewsItem).order_by(desc(NewsItem.published_at), desc(NewsItem.fetched_at)).limit(limit).all()


def list_category_items(db: Session, category: str, limit: int = 20):
    return (
        db.query(NewsItem)
        .filter(NewsItem.category == category)
        .order_by(desc(NewsItem.published_at), desc(NewsItem.fetched_at))
        .limit(limit)
        .all()
    )


def list_hot_event_clusters(db: Session, limit: int = 20):
    return db.query(EventCluster).order_by(desc(EventCluster.score), desc(EventCluster.last_seen_at)).limit(limit).all()


def list_category_event_clusters(db: Session, category: str, limit: int = 20):
    return (
        db.query(EventCluster)
        .filter(EventCluster.category == category)
        .order_by(desc(EventCluster.score), desc(EventCluster.last_seen_at))
        .limit(limit)
        .all()
    )


def list_sources(db: Session):
    return db.query(Source).order_by(Source.id.asc()).all()


def list_refresh_jobs(db: Session, limit: int = 10):
    return db.query(RefreshJob).order_by(desc(RefreshJob.created_at)).limit(limit).all()


def get_news_item(db: Session, item_id: int):
    return db.query(NewsItem).filter(NewsItem.id == item_id).first()


def get_event_cluster(db: Session, cluster_id: int):
    return db.query(EventCluster).filter(EventCluster.id == cluster_id).first()
