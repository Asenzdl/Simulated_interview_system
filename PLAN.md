# 智能模拟面试系统 — 开发计划

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Next.js 16 + Tailwind CSS 4 + shadcn/ui + Framer Motion |
| 后端 | FastAPI + SQLAlchemy 2.0 async + aiosqlite |
| 数据库 | SQLite + ChromaDB (向量搜索) |
| AI | OpenAI SDK (兼容 DeepSeek 等第三方) |
| 闪卡算法 | fsrs-python |
| 包管理 | pnpm (前端) + uv (后端) |

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

## Phase 2: 题库管理

### 2.1 后端 questions CRUD ✅
- [x] question_service.py — TDD: 先写 pytest 测试 (19 tests)
- [x] api/questions.py — 真实 CRUD 逻辑
- [x] 验证: 25 tests all pass

### 2.2 后端 categories CRUD ✅
- [x] category_service.py + api/categories.py — 分类增删改查
- [x] 验证: 34 tests all pass

### 2.3 后端批量导入 ✅
- [x] import_service.py — Markdown 解析（`## 标题 #标签` + `答案:` 分隔）
- [x] 验证: 42 tests all pass

### 2.4 前端基础设施 ✅
- [x] types/index.ts — TypeScript 类型定义
- [x] lib/api.ts — API 请求封装
- [x] 验证: tsc --noEmit 通过

### 2.5 前端布局框架 ✅
- [x] layout.tsx — SidebarProvider + AppSidebar + SidebarInset
- [x] AppSidebar 组件（6 个导航项）
- [x] 验证: tsc --noEmit 通过

### 2.6 前端题库页面 ✅
- [x] QuestionTable — DataTable 展示
- [x] QuestionDialog — 弹窗式创建/编辑
- [x] QuestionDeleteDialog — 删除确认弹窗
- [x] 验证: tsc --noEmit 通过

### 2.7 前端分类管理 ✅
- [x] CategoryManager — 侧边 Sheet 管理
- [x] 集成到题库页面
- [x] 验证: tsc --noEmit 通过

### 2.8 题目编辑改为独立页面 ✅
- [x] question-form.tsx — 纯表单组件，左右分栏 Card 布局
- [x] app/questions/new/page.tsx — 新建题目页面
- [x] app/questions/[id]/edit/page.tsx — 编辑题目页面（加载数据回显）
- [x] 修改 questions/page.tsx — 按钮改为 router.push 跳转
- [x] 删除 question-dialog.tsx
- [x] 验证: tsc --noEmit 通过

### 2.9 前端批量导入 ✅
- [x] ImportDialog — 拖拽上传 + 预览 + 分类选择
- [x] 集成到题库列表页（批量导入按钮）
- [x] 验证: tsc --noEmit 通过

### 2.10 批量删除题目 ✅
- [x] question-table.tsx — 每行 Checkbox + 表头全选 + 选中行高亮
- [x] questions/page.tsx — selectedIds + 批量删除按钮 + AlertDialog 确认
- [x] 验证: tsc --noEmit 通过

### 2.11 题目标题去重 ✅
- [x] models/question.py — title 字段加 unique 约束
- [x] Alembic migration — 添加 unique 索引
- [x] question_service.py — create 捕获唯一性冲突，返回 409 错误
- [x] import_service.py — import 跳过重复标题，返回 imported + skipped
- [x] 前端 ImportDialog — 显示跳过数量
- [x] 验证: 42 tests all pass

### 2.12 标题行内编辑入口 ✅
- [x] question-table.tsx — 标题 hover 时右侧显示「打开」链接
- [x] 下拉菜单精简为只保留「删除」
- [x] 验证: tsc --noEmit 通过

## Phase 3: 闪卡复习

### 3.1 后端 FSRS 核心
- [ ] core/fsrs.py — Card ↔ DB 转换
- [ ] review_service.py — TDD: 先写 pytest
- [ ] api/review.py — due/next/rate/stats
- [ ] 验证: curl 测试 FSRS 计算正确

### 3.2 前端闪卡组件
- [ ] FlashCard — Framer Motion 3D 翻转
- [ ] RatingButtons — Again/Hard/Good/Easy
- [ ] ReviewProgress — 进度条
- [ ] 验证: 翻转动效流畅

### 3.3 前端复习页面
- [ ] app/review/page.tsx — 复习流程
- [ ] ReviewComplete — 完成统计弹窗
- [ ] 验证: 完整复习流程可用

## Phase 4: AI 模拟面试

### 4.1 后端 LLM 封装
- [ ] core/llm.py — OpenAI 兼容客户端
- [ ] prompts/ — 面试官 + 评分 Prompt
- [ ] 验证: 单独调用 LLM 返回正常

### 4.2 后端面试 API
- [ ] interview_service.py — 多轮对话 + 评分
- [ ] api/interview.py — SSE 流式端点
- [ ] 验证: curl 测试 SSE 流式输出

### 4.3 前端 SSE 封装
- [ ] lib/sse.ts — fetch + ReadableStream
- [ ] 验证: 能接收流式数据

### 4.4 前端面试页面
- [ ] ChatPanel — 对话面板
- [ ] StreamingText — 打字机效果
- [ ] ScoreRadar — 六维雷达图
- [ ] 验证: 完整面试流程可用

## Phase 5: 错题本

### 5.1 后端错题逻辑
- [ ] api/errors.py — CRUD + 标记掌握
- [ ] 复习/面试自动记录错题
- [ ] 验证: curl 测试

### 5.2 前端错题页面
- [ ] ErrorList — 筛选列表
- [ ] ErrorDetailDialog — 详情 + 掌握标记
- [ ] 验证: 错题展示和操作正常

## Phase 6: 相似题目

### 6.1 后端向量搜索
- [ ] core/chroma.py — ChromaDB 客户端
- [ ] embedding_service.py — embedding 同步 + 查询
- [ ] api/similar.py — 搜索接口
- [ ] 验证: 搜索返回相关结果

### 6.2 前端相似题目展示
- [ ] SimilarQuestionsPanel — 侧边栏组件
- [ ] 集成到复习页面
- [ ] 验证: 复习时能看到相似题目推荐

## Phase 7: 数据分析

### 7.1 后端统计 API
- [ ] analytics_service.py — SQL 聚合查询
- [ ] api/analytics.py — overview/trend/category/heatmap
- [ ] 验证: curl 返回正确数据

### 7.2 前端分析页面
- [ ] OverviewCards — 总览卡片
- [ ] TrendChart — 趋势折线图
- [ ] CategoryPie — 分类饼图
- [ ] Heatmap — 学习热力图
- [ ] 验证: 图表渲染正确

### 7.3 前端仪表盘首页
- [ ] app/page.tsx — Dashboard 组合
- [ ] 验证: 首页展示关键数据

## Phase 8: UI 打磨

- [ ] 暗黑/亮色主题切换
- [ ] Framer Motion 页面过渡动画
- [ ] Loading 骨架屏
- [ ] Toast 通知反馈
- [ ] 响应式布局优化
- [ ] Markdown 代码高亮
- [ ] 整体视觉一致性检查

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
