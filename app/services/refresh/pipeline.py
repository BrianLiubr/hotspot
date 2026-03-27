from datetime import datetime


def run_refresh(trigger_type: str = "manual") -> dict:
    return {
        "trigger_type": trigger_type,
        "status": "pending",
        "started_at": datetime.utcnow().isoformat(),
        "message": "刷新 pipeline 已占位，下一步接入真实抓取 / 入库 / 聚合流程",
    }
