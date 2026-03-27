from fastapi import APIRouter

router = APIRouter()


MOCK_ITEMS = [
    {
        "id": 1,
        "title": "示例热点：AI 模型发布带动产业讨论",
        "summary": "这里先用占位数据打通 API。",
        "category": "ai",
        "source": "OpenAI Blog",
        "published_at": "2026-03-27 15:30",
        "score": 88,
        "related_count": 3,
    },
    {
        "id": 2,
        "title": "示例热点：市场对最新宏观数据作出反应",
        "summary": "财经榜单后续接真实排序。",
        "category": "finance",
        "source": "中国新闻网",
        "published_at": "2026-03-27 15:10",
        "score": 81,
        "related_count": 2,
    },
    {
        "id": 3,
        "title": "示例热点：社会新闻事件持续更新",
        "summary": "社会新闻类占位数据。",
        "category": "society",
        "source": "新华社",
        "published_at": "2026-03-27 14:50",
        "score": 76,
        "related_count": 4,
    },
]


@router.get("/hot")
def hot_feed():
    return {"items": MOCK_ITEMS}


@router.get("/latest")
def latest_feed():
    return {"items": MOCK_ITEMS}


@router.get("/category/{category}")
def category_feed(category: str):
    return {"items": [item for item in MOCK_ITEMS if item["category"] == category]}
