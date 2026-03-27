from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.queries import list_refresh_jobs, list_sources
from app.services.refresh.pipeline import run_refresh
from app.services.storage import seed_sources

router = APIRouter()


@router.get("/jobs")
def jobs(db: Session = Depends(get_db)):
    items = list_refresh_jobs(db)
    return {
        "items": [
            {
                "id": item.id,
                "trigger_type": item.trigger_type,
                "status": item.status,
                "started_at": item.started_at.isoformat() if item.started_at else None,
                "finished_at": item.finished_at.isoformat() if item.finished_at else None,
                "message": item.message,
            }
            for item in items
        ]
    }


@router.post("/refresh")
async def trigger_refresh(db: Session = Depends(get_db)):
    result = await run_refresh(db, trigger_type="manual")
    return {"ok": True, "message": result["message"], "count": result["count"], "errors": result["errors"]}


@router.post("/rerank")
def rerank():
    return {"ok": True, "message": "重算榜单入口已预留"}


@router.get("/sources")
def sources(db: Session = Depends(get_db)):
    seed_sources(db)
    items = list_sources(db)
    return {
        "items": [
            {
                "id": item.id,
                "name": item.name,
                "type": item.type,
                "url": item.url,
                "category_default": item.category_default,
                "weight": item.weight,
                "enabled": item.enabled,
            }
            for item in items
        ]
    }
