import asyncio

from app.db import SessionLocal
from app.services.refresh.pipeline import run_refresh


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print(asyncio.run(run_refresh(db, trigger_type="manual")))
    finally:
        db.close()
