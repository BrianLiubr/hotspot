from fastapi import APIRouter, HTTPException

router = APIRouter()


MOCK_EVENTS = {
    1: {
        "id": 1,
        "title": "示例热点：AI 模型发布带动产业讨论",
        "summary": "这里先展示事件详情占位数据。",
        "category": "ai",
        "score": 88,
        "sources": ["OpenAI Blog", "Hacker News", "Google AI Blog"],
    }
}


@router.get("/{event_id}")
def event_detail(event_id: int):
    event = MOCK_EVENTS.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
