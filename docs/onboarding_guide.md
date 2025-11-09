## 新手上手指南（Onboarding Guide）

本指南面向第一次接触本项目的开发者，目标是在 1 天内完成环境跑通、理解核心架构、完成功能改造的小任务。

### 0. 你需要的背景
- Python 基础（函数、模块、虚拟环境）
- 基础 HTTP/REST 知识（GET/POST、Header、JSON）
- 对 Docker/Docker Compose 有基本了解

---

### 1. 一小时跑通环境

1) 克隆并启动
```bash
git clone <repo>
cd FASTAPI-TEST
cp example.env .env
docker-compose up -d
```

2) 初始化数据库
```bash
curl -X POST http://localhost:8000/db/renew \
  -H "X-SUPER-ADMIN-TOKEN: admin.root"
```

3) 验证运行
- 打开 `http://localhost:8000/docs` 能查看到接口文档
- 登录测试：`POST /public/auth/login` → `test-username` / `test-password`
- 用 Token 访问 `/private/*` 接口

---

### 2. 十五分钟建立心智模型

- 入口：`src/server.py` 初始化 FastAPI 应用与中间件，聚合所有路由
- 路由：`src/routers/server.py` 分发到 `public` / `private` / `root` / `db`
- 依赖：`src/dependencies/` 定义认证（JWT、API Key）与数据库会话
- 数据：
  - 连接与会话：`src/database/database.py`
  - ORM 模型：`src/database/models/sample.py`
  - CRUD：`src/crud/`
- 工具：`src/utils/`（JWT、密码、S3/MinIO、Swagger UI 等）

建议阅读顺序：
1. `src/server.py`（应用启动）
2. `src/routers/server.py`（路由总览）
3. `src/dependencies/auth.py`（认证流程）
4. `src/database/database.py` 与 `src/database/models/sample.py`（数据库）
5. `src/crud/user.py`（CRUD 示例）

---

### 3. 首个任务（建议 1 小时内完成）

目标：新增一个公开接口，返回服务器时间。

步骤：
1) 在 `src/routers/public/server.py` 增加：
```python
@router.get("/time")
async def get_time():
    import datetime
    return {"server_time": datetime.datetime.utcnow().isoformat() + "Z"}
```
2) 保存后访问 `http://localhost:8000/public/time`

交付检查：接口 200 返回 `server_time` 字段。

---

### 4. 第二个任务：新增受保护接口

目标：返回当前登录用户的用户名。

步骤：
1) 在 `src/routers/private/server.py` 新增路由模块或在现有模块新增：
```python
from fastapi import Depends
from src.dependencies.auth import get_current_user

@router.get("/whoami")
async def whoami(user = Depends(get_current_user)):
    return {"username": user.account[0].username}
```
2) 获取 Token 后访问 `GET /private/whoami`

交付检查：返回 `username` 与登录时一致。

---

### 5. 第三个任务：数据库 + CRUD

目标：新增 `Product` 表与创建接口。

步骤：
1) 在 `src/database/models/sample.py` 添加模型，执行 Alembic 迁移（或用 `/db/renew` 重建）
2) 在 `src/crud/` 添加 `product.py`，实现 `create_product`
3) 新增 `src/schemas/product.py` 定义请求/响应模型
4) 在 `src/routers/private/` 新增 `product.py` 路由并注册到 `private/server.py`

交付检查：
- `POST /private/product` 能创建，数据库能看到记录（用 Adminer）。

---

### 6. 常见坑位与排查（FAQ）

- 端口被占用：修改 `docker-compose.yaml` 暴露端口或释放本机端口
- MySQL 未就绪：等待 30~60 秒；查看 `docker-compose logs mysql`
- 登录失败：确认 `X-SUPER-ADMIN-TOKEN`、测试用户是否已写入（执行过 `/db/renew`）
- MinIO/S3 403：检查 `example.env` 中存储配置是否一致（S3_PROVIDER、MinIO 账号）
- Sentry 未上报：需配置 `SENTRY_DSN` 并重启容器

---

### 7. 日常开发工作流

1) 写代码（新增路由/CRUD/模型）
2) 如有模型变化：执行迁移或用 `/db/renew` 重建本地库
3) 通过 Swagger UI 测试接口
4) 查看日志与错误：`docker-compose logs -f backend`
5) 提交代码：确保无敏感信息（.env 不入库）

---

### 8. 最后检查清单（新人自测）

- 能本地启动并访问 `/docs`
- 能 `POST /public/auth/login` 获取 JWT
- 能访问一个 `private` 路由（带 Token）
- 能在 Adminer 看到至少 3 张表（users/accounts/blobs）
- 能跑通一个自己新增的接口

---

参考阅读：
- `docs/quick_start.md`（5 分钟跑通）
- `docs/architecture.md`（架构与技术说明）
- `docs/diagrams.md`（Mermaid 流程图）
