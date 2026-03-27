from fastapi import APIRouter

from app.services.refresh.pipeline import run_refresh
from app.services.source_registry import DEFAULT_SOURCES

router = APIRouter()


@router.get("/jobs")
async def list_jobs():
    preview = await run_refresh(trigger_type="preview")
    return {
        "items": [
            {
                "id": 1,
                "trigger_type": preview["trigger_type"],
                "status": preview["status"],
                "started_at": preview["started_at"],
                "message": preview["message"],
            }
        ]
    }


@router.post("/refresh")
async def trigger_refresh():
    preview = await run_refresh(trigger_type="manual")
    return {"ok": True, "message": preview["message"], "count": len(preview["items"])}


@router.post("/rerank")
def rerank():
    return {"ok": True, "message": "重算榜单入口已预留"}


@router.get("/sources")
def list_sources():
    return {"items": DEFAULT_SOURCES}
