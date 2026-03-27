from __future__ import annotations

from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.cluster_item import ClusterItem
from app.models.event_cluster import EventCluster
from app.models.news_item import NewsItem
from app.services.dedup.deduper import is_similar_title
from app.services.ranking.scorer import score_item


def rebuild_clusters(db: Session) -> int:
    db.query(ClusterItem).delete()
    db.query(EventCluster).delete()
    db.commit()

    items = db.query(NewsItem).order_by(NewsItem.published_at.desc(), NewsItem.id.desc()).all()
    buckets: list[list[NewsItem]] = []

    for item in items:
        placed = False
        for bucket in buckets:
            if is_similar_title(item.normalized_title or item.title, bucket[0].normalized_title or bucket[0].title, threshold=85):
                bucket.append(item)
                placed = True
                break
        if not placed:
            buckets.append([item])

    for bucket in buckets:
        primary = bucket[0]
        keyword_hits = 0
        related_count = len(bucket)
        cluster_score = score_item(
            primary.source.name if primary.source else "Unknown",
            primary.published_at,
            related_count=related_count,
            keyword_hits=keyword_hits,
        )
        cluster = EventCluster(
            canonical_title=primary.title,
            canonical_summary=primary.summary,
            category=primary.category,
            score=cluster_score,
            first_seen_at=min((item.published_at for item in bucket if item.published_at), default=primary.fetched_at),
            last_seen_at=max((item.published_at for item in bucket if item.published_at), default=primary.fetched_at),
            related_count=related_count,
        )
        db.add(cluster)
        db.flush()

        for item in bucket:
            db.add(ClusterItem(cluster_id=cluster.id, news_item_id=item.id))

    db.commit()
    return len(buckets)


def get_cluster_details(db: Session, cluster_id: int):
    cluster = db.query(EventCluster).filter(EventCluster.id == cluster_id).first()
    if not cluster:
        return None
    relations = db.query(ClusterItem).filter(ClusterItem.cluster_id == cluster_id).all()
    items = [rel.news_item for rel in relations]
    return {"cluster": cluster, "items": items}


def list_hot_clusters(db: Session, limit: int = 20, category: str | None = None):
    query = db.query(EventCluster)
    if category:
        query = query.filter(EventCluster.category == category)
    return query.order_by(EventCluster.score.desc(), EventCluster.last_seen_at.desc()).limit(limit).all()
