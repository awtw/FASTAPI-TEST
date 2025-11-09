# 🚀 快速入门指南（中文）

> 本文迁移自仓库根目录的 QUICK_START_CN.md，帮助你 5 分钟上手本项目。

## 1. 启动项目

```bash
cd FASTAPI-TEST
docker-compose up -d
```

初始化数据库：
```bash
curl -X POST http://localhost:8000/db/renew \
  -H "X-SUPER-ADMIN-TOKEN: admin.root"
```

访问：
- API: http://localhost:8000
- 文档: http://localhost:8000/docs
- Adminer: http://localhost:8001
- MinIO 控制台: http://localhost:9001

## 2. 登录测试

- POST `/public/auth/login`，使用：`test-username` / `test-password`
- 获取到 JWT 后，使用 Bearer Token 访问 `/private/*`

## 3. 目录结构（简）

```
src/
├── routers/      # API 路由（public/private/db）
├── database/     # 连接、模型、工具
├── crud/         # 增删改查
├── schemas/      # Pydantic 模型
└── dependencies/ # 认证/数据库依赖
```

## 4. 常用命令

```bash
# 查看日志
docker-compose logs -f backend
# 重启
docker-compose restart backend
# 重新构建
docker-compose up -d --build
```

更多细节请阅读 `docs/onboarding_guide.md` 与 `docs/architecture.md`。
