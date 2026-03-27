from fastapi import APIRouter

from app.services.refresh.pipeline import collect_preview_items

router = APIRouter()


@router.get("/hot")
async def hot_feed():
    items = await collect_preview_items(limit_per_source=5)
    return {"items": items[:20]}


@router.get("/latest")
async def latest_feed():
    items = await collect_preview_items(limit_per_source=5)
    return {"items": items[:20]}


@router.get("/category/{category}")
async def category_feed(category: str):
    items = await collect_preview_items(limit_per_source=5)
    return {"items": [item for item in items if item.get("category") == category][:20]}
