from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


MOCK_ITEMS = [
    {
        "id": 1,
        "title": "示例热点：AI 模型发布带动产业讨论",
        "summary": "这里先用占位数据打通页面，后续接真实抓取与聚合结果。",
        "category": "ai",
        "source": "OpenAI Blog",
        "published_at": "2026-03-27 15:30",
        "score": 88,
        "related_count": 3,
    },
    {
        "id": 2,
        "title": "示例热点：市场对最新宏观数据作出反应",
        "summary": "财经页后续会接多来源聚合与热度排序。",
        "category": "finance",
        "source": "中国新闻网",
        "published_at": "2026-03-27 15:10",
        "score": 81,
        "related_count": 2,
    },
    {
        "id": 3,
        "title": "示例热点：社会新闻事件持续更新",
        "summary": "社会类先以稳定媒体源为主，后续再扩展。",
        "category": "society",
        "source": "新华社",
        "published_at": "2026-03-27 14:50",
        "score": 76,
        "related_count": 4,
    },
]


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"items": MOCK_ITEMS, "page_title": "热点总榜", "last_refresh": "未刷新"},
    )


@router.get("/latest", response_class=HTMLResponse)
def latest(request: Request):
    return templates.TemplateResponse(
        request,
        "latest.html",
        {"items": MOCK_ITEMS, "page_title": "最新内容"},
    )


@router.get("/category/{category}", response_class=HTMLResponse)
def category(request: Request, category: str):
    items = [item for item in MOCK_ITEMS if item["category"] == category]
    return templates.TemplateResponse(
        request,
        "category.html",
        {"items": items, "page_title": f"分类：{category}", "category": category},
    )


@router.get("/events/{event_id}", response_class=HTMLResponse)
def event_detail(request: Request, event_id: int):
    item = next((item for item in MOCK_ITEMS if item["id"] == event_id), None)
    return templates.TemplateResponse(
        request,
        "event_detail.html",
        {"item": item, "page_title": "事件详情"},
    )


@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    jobs = [
        {"id": 1, "trigger_type": "manual", "status": "pending", "message": "等待接入真实刷新任务"}
    ]
    return templates.TemplateResponse(
        request,
        "admin.html",
        {"jobs": jobs, "page_title": "管理后台"},
    )
