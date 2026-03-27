from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.queries import list_category_items, list_hot_items, list_latest_items

router = APIRouter()


def serialize(items):
    return {
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "summary": item.summary,
                "url": item.url,
                "source": None,
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
    return serialize(list_hot_items(db))


@router.get("/latest")
def latest_feed(db: Session = Depends(get_db)):
    return serialize(list_latest_items(db))


@router.get("/category/{category}")
def category_feed(category: str, db: Session = Depends(get_db)):
    return serialize(list_category_items(db, category))
