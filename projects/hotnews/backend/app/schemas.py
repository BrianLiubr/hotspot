from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SourceOut(BaseModel):
    id: int
    name: str
    type: str
    enabled: bool
    base_url: Optional[str] = None

    class Config:
        from_attributes = True


class NewsItemOut(BaseModel):
    title: str
    summary: Optional[str] = None
    source: str
    published_at: Optional[datetime] = None
    url: str
    rank_score: Optional[float] = None
    category: Optional[str] = None
    collected_at: datetime


class HotnewsResponse(BaseModel):
    date: str
    count: int
    items: List[NewsItemOut]


class CollectRequest(BaseModel):
    source_names: Optional[List[str]] = None


class CollectSourceResult(BaseModel):
    source: str
    status: str
    item_count: int = 0
    error_message: Optional[str] = None


class CollectResponse(BaseModel):
    status: str
    collected_sources: List[str]
    total_items: int
    requested_sources: List[str] = Field(default_factory=list)
    success_count: int = 0
    failed_count: int = 0
    results: List[CollectSourceResult] = Field(default_factory=list)
    message: Optional[str] = None
