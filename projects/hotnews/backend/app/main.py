from contextlib import contextmanager
from typing import Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.collector_registry import get_collectors, get_collectors_map
from app.config import BACKEND_CORS_ORIGINS
from app.database import Base, engine, get_db
from app.models import Source
from app.schemas import (
    CollectRequest,
    CollectResponse,
    CollectSourceResult,
    HotnewsResponse,
    NewsItemOut,
    SourceOut,
)
from app.services import ensure_source, get_query_date, query_hotnews, record_run, save_collected_items


@contextmanager
def db_session_scope():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Hotnews Project API", version="0.3.0")
api_router = APIRouter(prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def startup_seed_sources() -> None:
    with db_session_scope() as db:
        for collector in get_collectors():
            ensure_source(db, collector)


@app.get("/health")
@api_router.get("/health")
def health():
    return {"status": "ok", "cors_origins": BACKEND_CORS_ORIGINS, "api_prefix": "/api"}


@app.get("/v1/sources", response_model=list[SourceOut])
@api_router.get("/v1/sources", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.query(Source).order_by(Source.name.asc()).all()


@app.get("/v1/hotnews", response_model=HotnewsResponse)
@api_router.get("/v1/hotnews", response_model=HotnewsResponse)
def get_hotnews(
    date: Optional[str] = Query(default=None, description="查询日期，默认昨天，格式 YYYY-MM-DD"),
    limit: int = Query(default=20, ge=1, le=100),
    source: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    target_date = get_query_date(date)
    rows = query_hotnews(db, target_date=target_date, limit=limit, source_name=source)
    items = [
        NewsItemOut(
            title=item.title,
            summary=item.summary,
            source=source_name,
            published_at=item.published_at,
            url=item.url,
            rank_score=item.rank_score,
            category=item.category,
            collected_at=item.collected_at,
        )
        for item, source_name in rows
    ]
    return HotnewsResponse(date=target_date.isoformat(), count=len(items), items=items)


@app.post("/v1/collect", response_model=CollectResponse)
@api_router.post("/v1/collect", response_model=CollectResponse)
def collect_hotnews(payload: Optional[CollectRequest] = None, db: Session = Depends(get_db)):
    collectors_map = get_collectors_map()
    selected_names = (payload.source_names if payload else None) or list(collectors_map.keys())
    missing = [name for name in selected_names if name not in collectors_map]
    if missing:
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"Unknown sources: {', '.join(missing)}",
                "missing_sources": missing,
            },
        )

    total_items = 0
    collected_sources: list[str] = []
    results: list[CollectSourceResult] = []

    for name in selected_names:
        collector = collectors_map[name]
        source = ensure_source(db, collector)
        try:
            items = collector.collect()
            saved = save_collected_items(db, source, items)
            record_run(db, source_name=name, status="success", item_count=saved)
            total_items += saved
            collected_sources.append(name)
            results.append(CollectSourceResult(source=name, status="success", item_count=saved))
        except Exception as exc:
            error_message = str(exc)
            record_run(db, source_name=name, status="failed", item_count=0, error_message=error_message)
            results.append(
                CollectSourceResult(source=name, status="failed", item_count=0, error_message=error_message)
            )

    failed_count = len([item for item in results if item.status == "failed"])
    success_count = len(results) - failed_count
    status = "partial_success" if failed_count and success_count else ("failed" if failed_count else "ok")
    message = None
    if status == "ok":
        message = "采集完成"
    elif status == "partial_success":
        message = "部分源采集成功"
    else:
        message = "采集失败"

    return CollectResponse(
        status=status,
        collected_sources=collected_sources,
        total_items=total_items,
        requested_sources=selected_names,
        success_count=success_count,
        failed_count=failed_count,
        results=results,
        message=message,
    )


app.include_router(api_router)
