from datetime import datetime

from pydantic import BaseModel


class FeedItemOut(BaseModel):
    id: int
    title: str
    summary: str | None = None
    url: str
    source: str | None = None
    category: str | None = None
    published_at: datetime | None = None
    score: int | float | None = None
    related_count: int | None = None


class FeedResponse(BaseModel):
    items: list[FeedItemOut]
