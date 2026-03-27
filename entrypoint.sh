#!/bin/sh
set -e

export PYTHONPATH=/app

echo "[entrypoint] waiting for database..."
python - <<'PY'
import os
import time
from sqlalchemy import create_engine, text

url = os.environ.get("DATABASE_URL")
engine = create_engine(url, pool_pre_ping=True)

for i in range(30):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[entrypoint] database ready")
        break
    except Exception as exc:
        print(f"[entrypoint] waiting... {exc}")
        time.sleep(2)
else:
    raise SystemExit("database not ready after retries")
PY

echo "[entrypoint] initializing database"
python -m scripts.init_db

echo "[entrypoint] seeding first refresh"
python -m scripts.manual_refresh || true

echo "[entrypoint] starting app"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
