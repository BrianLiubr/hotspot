from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models.cluster_item import ClusterItem
from app.models.event_cluster import EventCluster
from app.models.news_item import NewsItem
from app.services.classify.keyword_classifier import classify_text
from app.services.dedup.deduper import is_similar_title
from app.services.ranking.scorer import score_item


def _keyword_hits(item: NewsItem) -> int:
    _, scores = classify_text(item.title or "", item.summary or "")
    return sum(scores.values())


def _cluster_match(item: NewsItem, primary: NewsItem) -> bool:
    if not item.normalized_title or not primary.normalized_title:
        return False
    if item.normalized_title == primary.normalized_title:
        return True
    return is_similar_title(item.normalized_title, primary.normalized_title, threshold=72)


def rebuild_clusters(db: Session) -> int:
    db.query(ClusterItem).delete()
    db.query(EventCluster).delete()
    db.commit()

    items = (
        db.query(NewsItem)
        .options(joinedload(NewsItem.source))
        .order_by(NewsItem.published_at.desc(), NewsItem.id.desc())
        .all()
    )
    buckets: list[list[NewsItem]] = []

    for item in items:
        placed = False
        for bucket in buckets:
            if _cluster_match(item, bucket[0]):
                bucket.append(item)
                placed = True
                break
        if not placed:
            buckets.append([item])

    for bucket in buckets:
        primary = bucket[0]
        keyword_hits = max((_keyword_hits(item) for item in bucket), default=0)
        related_count = len(bucket)
        source_name = primary.source.name if primary.source else "Unknown"
        category = primary.category
        cluster_score = score_item(
            source_name,
            primary.published_at,
            related_count=related_count,
            keyword_hits=keyword_hits,
            category=category,
        )
        cluster = EventCluster(
            canonical_title=primary.title,
            canonical_summary=primary.summary,
            category=category,
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
    relations = (
        db.query(ClusterItem)
        .options(joinedload(ClusterItem.news_item).joinedload(NewsItem.source))
        .filter(ClusterItem.cluster_id == cluster_id)
        .all()
    )
    items = [rel.news_item for rel in relations]
    return {"cluster": cluster, "items": items}


def list_hot_clusters(db: Session, limit: int = 20, category: str | None = None):
    query = db.query(EventCluster)
    if category:
        query = query.filter(EventCluster.category == category)
    return query.order_by(EventCluster.score.desc(), EventCluster.last_seen_at.desc()).limit(limit).all()
