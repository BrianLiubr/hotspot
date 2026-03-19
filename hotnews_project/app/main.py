from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app.collector_registry import get_collectors, get_collectors_map
from app.database import Base, engine, get_db
from app.models import Source
from app.schemas import CollectResponse, HotnewsResponse, NewsItemOut, SourceOut
from app.services import ensure_source, get_query_date, query_hotnews, record_run, save_collected_items

app = FastAPI(title="Hotnews Project API", version="0.1.0")
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def startup_seed_sources() -> None:
    db = next(get_db())
    try:
        for collector in get_collectors():
            ensure_source(db, collector)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/v1/sources", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.query(Source).order_by(Source.name.asc()).all()


@app.get("/v1/hotnews", response_model=HotnewsResponse)
def get_hotnews(
    date: str | None = Query(default=None, description="查询日期，默认昨天，格式 YYYY-MM-DD"),
    limit: int = Query(default=20, ge=1, le=100),
    source: str | None = Query(default=None),
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
def collect_hotnews(payload: CollectRequest | None = None, db: Session = Depends(get_db)):
    collectors_map = get_collectors_map()
    selected_names = (payload.source_names if payload else None) or list(collectors_map.keys())
    missing = [name for name in selected_names if name not in collectors_map]
    if missing:
        raise HTTPException(status_code=404, detail=f"Unknown sources: {', '.join(missing)}")

    total_items = 0
    collected_sources: list[str] = []

    for name in selected_names:
        collector = collectors_map[name]
        source = ensure_source(db, collector)
        try:
            items = collector.collect()
            saved = save_collected_items(db, source, items)
            record_run(db, source_name=name, status="success", item_count=saved)
            total_items += saved
            collected_sources.append(name)
        except Exception as exc:
            record_run(db, source_name=name, status="failed", item_count=0, error_message=str(exc))

    return CollectResponse(status="ok", collected_sources=collected_sources, total_items=total_items)
