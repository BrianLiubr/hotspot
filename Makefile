up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

init-db:
	. .venv/bin/activate && PYTHONPATH=. python -m scripts.init_db

refresh:
	. .venv/bin/activate && PYTHONPATH=. python -m scripts.manual_refresh

test:
	. .venv/bin/activate && PYTHONPATH=. pytest tests

migrate:
	. .venv/bin/activate && PYTHONPATH=. alembic upgrade head

revision:
	. .venv/bin/activate && PYTHONPATH=. alembic revision --autogenerate -m "init"
