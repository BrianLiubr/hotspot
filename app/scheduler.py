from __future__ import annotations

import asyncio
from contextlib import suppress

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config import settings
from app.db import SessionLocal
from app.services.refresh.pipeline import run_refresh

scheduler = AsyncIOScheduler(timezone=settings.default_timezone)


async def scheduled_refresh() -> None:
    db = SessionLocal()
    try:
        await run_refresh(db, trigger_type="auto")
    finally:
        db.close()


def start_scheduler() -> None:
    if scheduler.running:
        return
    scheduler.add_job(
        lambda: asyncio.create_task(scheduled_refresh()),
        trigger=IntervalTrigger(minutes=settings.refresh_interval_minutes),
        id="auto-refresh",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        with suppress(Exception):
            scheduler.shutdown(wait=False)
