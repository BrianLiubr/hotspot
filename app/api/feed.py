from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.clustering import get_cluster_details
from app.services.queries import list_category_event_clusters, list_hot_event_clusters, list_latest_items

router = APIRouter()


def serialize_clusters(items):
    return {
        "items": [
            {
                "id": item.id,
                "title": item.canonical_title,
                "summary": item.canonical_summary,
                "category": item.category,
                "published_at": item.last_seen_at.isoformat() if item.last_seen_at else None,
                "score": item.score,
                "related_count": item.related_count,
            }
            for item in items
        ]
    }


def serialize_latest(items):
    return {
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "summary": item.summary,
                "url": item.url,
                "source": item.source.name if item.source else None,
                "category": item.category,
                "published_at": item.published_at.isoformat() if item.published_at else None,
                "score": item.raw_score,
                "related_count": 1,
            }
            for item in items
        ]
    }


@router.get("/hot")
def hot_feed(db: Session = Depends(get_db)):
    return serialize_clusters(list_hot_event_clusters(db))


@router.get("/latest")
def latest_feed(db: Session = Depends(get_db)):
    return serialize_latest(list_latest_items(db))


@router.get("/category/{category}")
def category_feed(category: str, db: Session = Depends(get_db)):
    return serialize_clusters(list_category_event_clusters(db, category))


@router.get("/event/{cluster_id}")
def event_feed(cluster_id: int, db: Session = Depends(get_db)):
    data = get_cluster_details(db, cluster_id)
    if not data:
        return {"item": None}
    return {
        "item": {
            "id": data["cluster"].id,
            "title": data["cluster"].canonical_title,
            "summary": data["cluster"].canonical_summary,
            "category": data["cluster"].category,
            "score": data["cluster"].score,
            "related_count": data["cluster"].related_count,
            "sources": [
                {
                    "id": item.id,
                    "title": item.title,
                    "url": item.url,
                    "source": item.source.name if item.source else None,
                }
                for item in data["items"]
            ],
        }
    }
