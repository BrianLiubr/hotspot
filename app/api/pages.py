from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.refresh.pipeline import collect_preview_items


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    items = await collect_preview_items(limit_per_source=5)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"items": items[:20], "page_title": "热点总榜", "last_refresh": "实时预览模式"},
    )


@router.get("/latest", response_class=HTMLResponse)
async def latest(request: Request):
    items = await collect_preview_items(limit_per_source=5)
    return templates.TemplateResponse(
        request,
        "latest.html",
        {"items": items[:20], "page_title": "最新内容"},
    )


@router.get("/category/{category}", response_class=HTMLResponse)
async def category(request: Request, category: str):
    items = await collect_preview_items(limit_per_source=5)
    filtered = [item for item in items if item.get("category") == category]
    return templates.TemplateResponse(
        request,
        "category.html",
        {"items": filtered, "page_title": f"分类：{category}", "category": category},
    )


@router.get("/events/{event_id}", response_class=HTMLResponse)
def event_detail(request: Request, event_id: int):
    return templates.TemplateResponse(
        request,
        "event_detail.html",
        {"item": None, "page_title": f"事件详情 #{event_id}"},
    )


@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    jobs = [
        {"id": 1, "trigger_type": "manual", "status": "ready", "message": "已接入预览抓取入口"}
    ]
    return templates.TemplateResponse(
        request,
        "admin.html",
        {"jobs": jobs, "page_title": "管理后台"},
    )
