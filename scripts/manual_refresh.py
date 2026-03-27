import asyncio

from app.services.refresh.pipeline import run_refresh


if __name__ == "__main__":
    print(asyncio.run(run_refresh(trigger_type="manual")))
