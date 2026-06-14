# 面试复习系统

个人使用的面试复习工具：题库管理、闪卡复习（FSRS）、Dashboard 数据概览。

## 技术栈

- 前端: Next.js 16 + Tailwind CSS 4 + shadcn/ui
- 后端: FastAPI + SQLAlchemy 2.0 async + aiosqlite
- 数据库: SQLite
- 闪卡: fsrs-python
- Markdown: react-markdown + remark-gfm + rehype-highlight
- 包管理: pnpm（前端）+ uv（后端）

## 启动命令

```bash
# 后端
cd backend && uv run uvicorn src.main:app --reload --port 8000

# 前端
cd frontend && pnpm dev

# 后端测试
cd backend && uv run pytest
```

- 前端: http://localhost:3000
- 后端 API 文档: http://localhost:8000/docs

## 项目结构

- `PLAN.md` — 开发进度 checklist（checkbox 跟踪）
- `ARCHITECTURE.md` — 技术细节参考（数据库表、API 规格、组件树）
- `frontend/src/` — Next.js 前端源码
- `backend/src/` — FastAPI 后端源码
- `data/` — SQLite 数据库

## 开发约定

- 后端 service 层用 TDD：先写 pytest 测试，再实现
- 每步写完即验证，不堆积代码
- API 写完用 curl 验证，前端写完用浏览器验证
- UI 要求现代优雅，CRUD 通过弹窗（Dialog）进行，不用内联表单
- 配置从 `.env` 读取，不硬编码

## ECC 工具使用

- 后端 service 层开发：`ecc:tdd-workflow`
- 后端 API 写完：`ecc:fastapi-review`
- 前端组件写完：`ecc:react-review`
- 每个 Phase 完成：`ecc:code-review`
- 构建/启动报错：`ecc:build-fix`

## Git 规范

- Commit 用 Conventional Commits 格式：`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`
- 前缀用英文，描述可中英文混用
- 每个功能点单独 commit，不做大杂烩
- 功能点完成后，询问用户是否确认 commit 和 push
