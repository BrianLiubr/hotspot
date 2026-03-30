# Hotnews Project

热点新闻聚合服务，已拆成 **后端 API（FastAPI）+ 前端 Web（Vue3）**。

## 目录

- `hotnews_project/`：后端 API
- `hotnews_web/`：前端页面
- `docker-compose.yml`：本地一键启动

## 后端能力

主推荐 API 前缀：`/api`

- `GET /health`
- `GET /api/health`
- `GET /api/v1/sources`
- `GET /api/v1/hotnews?date=2026-03-18&limit=10&source=sample-static`
- `POST /api/v1/collect`

> 为兼容旧调用，当前无前缀的 `/v1/*` 也暂时保留。

### 特性

- 默认查询日期为昨天（Asia/Shanghai）
- 支持 CORS，默认允许本地 Vite 开发端口访问
- `POST /api/v1/collect` 返回更前端友好的结果：成功/失败源明细、总条数、消息摘要

## 本地开发

### 1) 启动后端

```bash
cd hotnews_project
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

打开：
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health
- API Health: http://127.0.0.1:8000/api/health

### 2) 启动前端

```bash
cd hotnews_web
npm install
npm run dev
```

打开：
- Web: http://127.0.0.1:5173

开发环境下前端默认请求：
- `http://127.0.0.1:8000/api`

## Docker Compose

项目根目录执行：

```bash
docker compose up --build
```

启动后访问：
- 前端：http://127.0.0.1:8080
- 后端：http://127.0.0.1:8000
- API 文档：http://127.0.0.1:8000/docs

生产/容器环境下前端通过 Nginx 反代：
- `/api/* -> api:8000/*`

## 前端页面

当前已实现：

- 日期选择（默认昨天）
- 来源筛选
- limit 数量控制
- 热点列表展示：
  - title
  - summary
  - source
  - published_at
  - url
  - rank_score
  - category
  - collected_at
- “立即采集”按钮，调用 `/api/v1/collect` 后自动刷新列表

## 说明

- 当前内置 RSS 示例源和静态示例源，先保证链路跑通
- 后续可继续接入更多公开、低风险热榜源
- 如果你后面要继续做登录、后台管理、定时采集、消息推送，现在这个结构已经比较适合继续扩展
