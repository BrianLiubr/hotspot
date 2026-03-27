# Hotspot Hub

中文 AI / 财经 / 社会新闻热点聚合平台 MVP。

当前版本已经支持：
- RSS 抓取真实数据
- SQLite 本地存储
- AI / 财经 / 社会三类分类
- 基础事件聚合与热点排序
- 网页展示总榜 / 最新 / 分类 / 事件详情
- 手动刷新
- 应用运行时每 30 分钟自动刷新
- 管理后台查看刷新任务和错误信息

---

## 1. 技术栈

- FastAPI
- SQLAlchemy
- SQLite（默认开发环境）
- Alembic
- Jinja2
- APScheduler
- httpx / feedparser / BeautifulSoup / trafilatura

---

## 2. 项目结构

```txt
app/
  api/              # 页面与 JSON API
  models/           # 数据模型
  services/         # 抓取、分类、聚合、排序、存储
  templates/        # Jinja2 模板
  static/           # CSS / JS
  scheduler.py      # 自动刷新调度器
scripts/
  init_db.py        # 初始化数据库
  manual_refresh.py # 手动触发刷新
tests/              # 基础测试
```

---

## 3. 本地启动

### 3.1 创建虚拟环境并安装依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3.2 准备环境变量

```bash
cp .env.example .env
```

默认使用本地 SQLite：

```env
DATABASE_URL=sqlite:///./hotspot.db
```

### 3.3 初始化数据库

```bash
PYTHONPATH=. python -m scripts.init_db
```

### 3.4 首次抓取数据

```bash
PYTHONPATH=. python -m scripts.manual_refresh
```

### 3.5 启动服务

```bash
PYTHONPATH=. uvicorn app.main:app --reload
```

启动后访问：
- 首页：<http://127.0.0.1:8000/>
- 管理页：<http://127.0.0.1:8000/admin>
- 健康检查：<http://127.0.0.1:8000/health>

---

## 4. 常用命令

### 使用 Makefile

```bash
make init-db
make refresh
make test
```

### 直接执行

```bash
PYTHONPATH=. python -m scripts.init_db
PYTHONPATH=. python -m scripts.manual_refresh
PYTHONPATH=. pytest tests
```

---

## 5. 当前数据流

当前刷新流程：
1. 读取默认 RSS 数据源
2. 拉取最新内容
3. 做标题与摘要清洗
4. 分类（AI / 财经 / 社会）
5. 写入 `news_items`
6. 重建 `event_clusters`
7. 写入 `refresh_jobs`
8. 前台页面与 API 从数据库读取

---

## 6. 已实现页面

- `/` 热点总榜（事件聚合视图）
- `/latest` 最新内容
- `/category/{category}` 分类热点榜
- `/events/{id}` 事件详情
- `/admin` 管理后台

---

## 7. 已实现 API

- `GET /health`
- `GET /api/feed/hot`
- `GET /api/feed/latest`
- `GET /api/feed/category/{category}`
- `GET /api/feed/event/{id}`
- `GET /api/admin/jobs`
- `GET /api/admin/sources`
- `POST /api/admin/refresh`

---

## 8. 当前限制

当前版本仍属于 MVP，存在这些限制：
- 主要依赖 RSS，尚未接更多中文源
- 事件聚合仍以标题规则和相似度为主
- 热度排序是规则版，不是学习型算法
- 自动刷新依赖应用进程存活
- 默认开发环境使用 SQLite，不是生产级部署方案

---

## 9. 下一步建议

优先建议：
1. 提升中文标题归一化与聚合质量
2. 增加更多稳定中文源
3. 给 `event_cluster` 增加更丰富的聚合信息
4. 切换到 PostgreSQL + Docker 常驻部署
5. 增加真正的后台源管理能力

---

## 10. Docker 部署

已提供：
- `Dockerfile`
- `docker-compose.yml`
- `.env.docker.example`
- `entrypoint.sh`
- `docs/DEPLOYMENT.md`

快速启动：

```bash
cp .env.docker.example .env.docker
docker compose up --build
```

容器会自动：
- 等待 PostgreSQL
- 初始化数据库
- 首次抓取数据
- 启动 Web 服务

Docker Compose 使用 `sh /app/entrypoint.sh`，避免本地挂载目录时脚本权限问题。

---

## 11. 当前状态

当前仓库已经是：
**可本地运行、可 Docker 部署、可抓真实数据、可自动刷新的热点平台 MVP 原型。**
