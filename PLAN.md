# 智能面试复习系统 — 开发计划

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Next.js 16 + Tailwind CSS 4 + shadcn/ui |
| 后端 | FastAPI + SQLAlchemy 2.0 async + aiosqlite |
| 数据库 | SQLite |
| 闪卡 | fsrs-python |
| Markdown | react-markdown + remark-gfm + rehype-highlight |
| 包管理 | pnpm（前端）+ uv（后端） |

## 开发节奏

每步写完即验证，不堆积代码：
- 后端 service 层：TDD（先写 pytest 测试，再实现）
- 后端 API 层：写完用 curl 验证，再 ecc:code-review
- 前端组件：写完浏览器验证，再 ecc:react-review

---

## Phase 0: 脚手架 ✅

- [x] git init + .gitignore + .env
- [x] pnpm create next-app (Next.js 16, Tailwind, TypeScript)
- [x] uv init + 后端依赖安装
- [x] 验证: 前后端均能独立启动

## Phase 1: 后端基础 ✅

- [x] config.py (pydantic-settings)
- [x] database.py (async engine + session)
- [x] SQLAlchemy models (9 张表)
- [x] Alembic 迁移配置 + 初始 migration
- [x] Pydantic schemas (所有请求/响应模型)
- [x] main.py CORS + 路由挂载 (7 个路由组 stub)
- [x] 验证: /docs 可访问，数据库表创建成功

## Phase 2: 题库管理 ✅

- [x] question_service.py — TDD: 19 tests (CRUD + 分页 + 筛选)
- [x] category_service.py — 分类增删改查
- [x] import_service.py — Markdown 批量导入
- [x] api/questions.py + api/categories.py — 真实 CRUD 逻辑
- [x] 前端: types, api, layout, sidebar, 题库页面, 分类管理, 批量导入, 批量删除
- [x] 题目标题去重 (unique 约束 + 导入跳过重复)
- [x] 标题行内编辑入口
- [x] 验证: 42 tests all pass, tsc --noEmit 通过

## Phase 3: 闪卡复习 ✅

- [x] review_service.py — TDD: 17 tests (get_due, next, rate, stats)
- [x] api/review.py — due/next/rate/stats/queue-count
- [x] FlashCard — 淡入淡出切换 + Markdown 渲染 + 代码高亮 + 侧边抽屉
- [x] RatingButtons — 忘了/模糊/记得/秒答
- [x] ReviewProgress — 进度条
- [x] ReviewComplete — 完成统计弹窗
- [x] app/review/page.tsx — 完整复习流程
- [x] 验证: 59 tests all pass, tsc --noEmit 通过

## Phase 4: Dashboard 首页 ✅

- [x] /api/analytics/overview — 总题数、待复习、已掌握、今日已复习
- [x] 首页 4 个数据卡片 + 待复习入口按钮
- [x] 验证: 数据正确显示

## 已砍掉的功能

以下功能经分析投入产出比不足，不再实现：

- ~~AI 模拟面试~~ — 核心需求是记忆，不是表达训练
- ~~错题本~~ — FSRS 已自动处理（Again 评分缩短间隔）
- ~~相似题目 (ChromaDB)~~ — 运维成本高，分类+标签够用
- ~~数据分析独立页面~~ — Dashboard 首页已覆盖
- ~~暗黑模式切换~~ — 不需要

---

## 验证命令

```bash
# 后端
cd backend && uv run uvicorn src.main:app --reload --port 8000

# 前端
cd frontend && pnpm dev

# 后端测试
cd backend && uv run pytest

# 访问
# 前端: http://localhost:3000
# 后端文档: http://localhost:8000/docs
```
