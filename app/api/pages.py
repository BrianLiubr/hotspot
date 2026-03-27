from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.config import settings
from app.services.clustering import get_cluster_details
from app.services.queries import list_category_event_clusters, list_latest_items, list_refresh_jobs, list_hot_event_clusters, list_sources


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    items = list_hot_event_clusters(db)
    jobs = list_refresh_jobs(db, limit=1)
    last_refresh = jobs[0].finished_at.isoformat() if jobs and jobs[0].finished_at else "未刷新"
    return templates.TemplateResponse(
        request,
        "index.html",
        {"items": items, "page_title": "热点总榜", "last_refresh": last_refresh},
    )


@router.get("/latest", response_class=HTMLResponse)
def latest(request: Request, db: Session = Depends(get_db)):
    items = list_latest_items(db)
    return templates.TemplateResponse(
        request,
        "latest.html",
        {"items": items, "page_title": "最新内容"},
    )


@router.get("/category/{category}", response_class=HTMLResponse)
def category(request: Request, category: str, db: Session = Depends(get_db)):
    items = list_category_event_clusters(db, category)
    return templates.TemplateResponse(
        request,
        "category.html",
        {"items": items, "page_title": f"分类：{category}", "category": category},
    )


@router.get("/events/{event_id}", response_class=HTMLResponse)
def event_detail(request: Request, event_id: int, db: Session = Depends(get_db)):
    data = get_cluster_details(db, event_id)
    return templates.TemplateResponse(
        request,
        "event_detail.html",
        {"item": data["cluster"] if data else None, "related_items": data["items"] if data else [], "page_title": f"事件详情 #{event_id}"},
    )


@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db)):
    jobs = list_refresh_jobs(db)
    sources = list_sources(db)
    return templates.TemplateResponse(
        request,
        "admin.html",
        {
            "jobs": jobs,
            "page_title": "管理后台",
            "refresh_interval_minutes": settings.refresh_interval_minutes,
            "source_count": len(sources),
        },
    )
