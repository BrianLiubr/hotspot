from datetime import datetime

from pydantic import BaseModel


class SourceOut(BaseModel):
    id: int
    name: str
    type: str
    enabled: bool
    base_url: str | None = None

    class Config:
        from_attributes = True


class NewsItemOut(BaseModel):
    title: str
    summary: str | None = None
    source: str
    published_at: datetime | None = None
    url: str
    rank_score: float | None = None
    category: str | None = None
    collected_at: datetime


class HotnewsResponse(BaseModel):
    date: str
    count: int
    items: list[NewsItemOut]


class CollectRequest(BaseModel):
    source_names: list[str] | None = None


class CollectResponse(BaseModel):
    status: str
    collected_sources: list[str]
    total_items: int
