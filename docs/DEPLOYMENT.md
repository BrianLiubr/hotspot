# Deployment Guide

## Docker Compose（推荐）

### 1. 准备 Docker 环境变量

```bash
cp .env.docker.example .env.docker
```

默认数据库是容器内 PostgreSQL：

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/hotspot_hub
```

### 2. 启动服务

```bash
docker compose up --build
```

或者：

```bash
make up
```

### 3. 访问地址

- 首页：<http://127.0.0.1:8000/>
- 管理后台：<http://127.0.0.1:8000/admin>
- 健康检查：<http://127.0.0.1:8000/health>

## 容器启动时会做什么

`entrypoint.sh` 会自动执行：
1. 等待 PostgreSQL 可连接
2. 初始化数据库表
3. 先做一次手动刷新
4. 启动 FastAPI 服务

Compose 中使用 `sh /app/entrypoint.sh` 启动，避免 bind mount 场景下脚本执行位失效。

## 注意事项

- 如果 Docker daemon 没启动，`docker compose up` 会失败
- 当前 `init_db` 是重建表逻辑，适合 MVP / 开发期，不适合生产保数据升级
- 生产环境建议后续切成 Alembic 迁移而不是 drop/create
- 现在的自动刷新是在应用进程里跑，容器停掉就不刷新了

## VPS 部署建议

- 安装 Docker / Docker Compose
- 拉取仓库
- 配置 `.env.docker`
- 执行 `docker compose up -d --build`
- 用 Nginx / Caddy 做反代
- 如需公网访问，记得开 80/443 或反代端口
