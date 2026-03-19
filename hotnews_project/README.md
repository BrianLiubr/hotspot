# Hotnews Project

获取“调用时往前到前一天”的热点新闻聚合服务（MVP）。

## 目标

- 提供 API 查询指定日期（默认昨天）的热点新闻
- 优先使用免费、公开、低风险的数据源
- 支持后续扩展网页端和机器人端

## 技术栈

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- httpx
- feedparser

## 快速开始

```bash
cd hotnews_project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

打开：
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## API

- `GET /health`
- `GET /v1/sources`
- `GET /v1/hotnews?date=2026-03-18&limit=10`
- `POST /v1/collect`

## 说明

- 默认查询日期为昨天（Asia/Shanghai）
- 当前内置一个 RSS 示例源和一个静态示例源，便于先把框架跑通
- 后续可继续接公开新闻列表页、公开热榜页等低风险数据源
