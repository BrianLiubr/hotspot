from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get("/jobs")
def list_jobs():
    return {
        "items": [
            {
                "id": 1,
                "trigger_type": "manual",
                "status": "pending",
                "started_at": datetime.utcnow().isoformat(),
                "message": "等待接入真实刷新任务",
            }
        ]
    }


@router.post("/refresh")
def trigger_refresh():
    return {"ok": True, "message": "手动刷新入口已预留，后续接真实 pipeline"}


@router.post("/rerank")
def rerank():
    return {"ok": True, "message": "重算榜单入口已预留"}


@router.get("/sources")
def list_sources():
    return {"items": []}
