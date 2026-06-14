# 技术架构详细规格

## 1. 数据库表结构

### categories
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | auto-increment |
| name | VARCHAR(100) NOT NULL | category name |
| color | VARCHAR(7) | hex color code |
| icon | VARCHAR(50) | icon identifier |
| sort_order | INTEGER DEFAULT 0 | sort weight |
| created_at | DATETIME | creation time |

### tags
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | auto-increment |
| name | VARCHAR(50) NOT NULL UNIQUE | tag name |
| created_at | DATETIME | creation time |

### question_tags (junction table)
| Column | Type | Description |
|--------|------|-------------|
| question_id | INTEGER FK -> questions.id | |
| tag_id | INTEGER FK -> tags.id | |
| PK | (question_id, tag_id) | composite key |

### questions (core table)
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | auto-increment |
| title | TEXT NOT NULL UNIQUE | question title |
| content | TEXT | detailed content (Markdown) |
| answer | TEXT | standard answer (Markdown) |
| category_id | INTEGER FK -> categories.id | category |
| difficulty | INTEGER CHECK(1-5) | difficulty level |
| question_type | VARCHAR(20) | coding/theory/scenario/behavioral |
| is_active | BOOLEAN DEFAULT TRUE | active flag |
| chroma_id | VARCHAR(36) | reserved, unused |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### card_states (FSRS card state, 1:1 with questions)
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | |
| question_id | INTEGER FK UNIQUE | 1:1 with question |
| due | DATETIME NOT NULL | next review time |
| stability | FLOAT | FSRS stability param |
| difficulty | FLOAT | FSRS difficulty param |
| elapsed_days | INTEGER DEFAULT 0 | days elapsed |
| scheduled_days | INTEGER DEFAULT 0 | scheduled interval |
| reps | INTEGER DEFAULT 0 | review count |
| lapses | INTEGER DEFAULT 0 | lapse count |
| state | INTEGER DEFAULT 0 | 0=New 1=Learning 2=Review 3=Relearning |
| last_review | DATETIME | last review time |
| created_at | DATETIME | |
| updated_at | DATETIME | |

### review_logs
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | |
| question_id | INTEGER FK -> questions.id | |
| rating | INTEGER NOT NULL | 1=Again 2=Hard 3=Good 4=Easy |
| review_datetime | DATETIME NOT NULL | |
| state_before | INTEGER | FSRS state before |
| state_after | INTEGER | FSRS state after |
| elapsed_days | INTEGER | days since last review |
| scheduled_days | INTEGER | next interval |
| created_at | DATETIME | |

### 未使用的表（模型已定义但功能未实现）

以下表存在于 SQLAlchemy models 中，但对应的业务功能已砍掉：

- `interview_sessions` / `interview_messages` — AI 模拟面试（已砍掉）
- `error_records` — 独立错题本（已砍掉，FSRS 的 Again 评分替代）

### ER Relationships (已实现)
```
Category 1--N Question N--N Tag (via question_tags)
Question 1--1 CardState (FSRS)
Question 1--N ReviewLog
```

---

## 2. API 端点

### /api/questions
| Method | Path | Description | Query Params |
|--------|------|-------------|--------------|
| GET | /api/questions | 分页列表 + 筛选搜索 | page, page_size, category_id, difficulty, search |
| GET | /api/questions/{id} | 单题详情 | |
| POST | /api/questions | 创建题目 | |
| PUT | /api/questions/{id} | 更新题目 | |
| DELETE | /api/questions/{id} | 删除题目 | |
| POST | /api/questions/import | Markdown 批量导入 | category_id, difficulty |

### /api/categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/categories | 列表 |
| POST | /api/categories | 创建 |
| PUT | /api/categories/{id} | 更新 |
| DELETE | /api/categories/{id} | 删除 |

### /api/review
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/review/due | 到期卡片列表 |
| GET | /api/review/next | 下一张待复习卡片 |
| POST | /api/review/{question_id}/rate | 提交评分 (1-4) |
| GET | /api/review/stats | 复习统计 |
| GET | /api/review/queue-count | 待复习数量 |

### /api/analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/analytics/overview | 总题数、待复习、已掌握、今日已复习 |

---

## 3. 前端组件树

### Layout
- `AppSidebar` — 侧边导航（仪表盘、题库管理、闪卡复习、模拟面试、错题本、数据分析）
- `SidebarInset` — Header + Content

### Dashboard /
- 4 个数据卡片（总题数、待复习、已掌握、今日已复习）
- 待复习入口按钮

### Questions /questions
- `QuestionTable` — 表格展示 + Checkbox 多选 + 行内编辑入口
- `QuestionDeleteDialog` — 删除确认弹窗
- `ImportDialog` — 拖拽上传 + 预览 + 分类选择
- `CategoryManager` — 侧边 Sheet 分类管理

### Questions /questions/new, /questions/[id]/edit
- `QuestionForm` — 左右分栏 Card 表单

### Review /review
- `FlashCard` — 淡入淡出切换正面/背面 + Markdown + 代码高亮 + 侧边抽屉
- `RatingButtons` — 忘了/模糊/记得/秒答
- `ReviewProgress` — 进度条
- `ReviewComplete` — 完成统计弹窗

---

## 4. 关键技术决策

### 4.1 Async Backend
SQLAlchemy 2.0 async + aiosqlite. FastAPI is async, sync DB blocks event loop. Use create_async_engine with sqlite+aiosqlite URL, async_sessionmaker for session factory, get_db dependency.

### 4.2 FSRS (v4+)
Use `Scheduler` class. API: `Scheduler().review_card(card, Rating.Good)` returns tuple of (Card, ReviewLog). Rating: `Rating.Again/1, Hard/2, Good/3, Easy/4`. Serialize Card fields to card_states table.

### 4.3 Markdown 渲染
react-markdown + remark-gfm (表格/任务列表) + rehype-highlight (代码语法高亮, GitHub 主题)。

### 4.4 闪卡交互
正面深色背景白字（题目），背面白底黑字（答案）。固定 550px 高度，答案过长内部滚动（scrollbar-hide）。淡入淡出切换（0.1s）。切换卡片时自动回到正面。

### 4.5 级联删除
Question 关联 CardState/ReviewLog/ErrorRecord 设置 `cascade="all, delete-orphan"`，删除题目时自动清理关联数据。

---

## 5. 依赖版本

### Backend (pyproject.toml) — Python >=3.12
- fastapi, uvicorn, sqlalchemy[asyncio], aiosqlite, alembic
- fsrs>=4.0.0
- pydantic-settings, python-multipart

### Frontend (package.json)
- next, react, react-dom
- framer-motion, recharts, lucide-react
- react-markdown, remark-gfm, rehype-highlight, highlight.js
- @tailwindcss/typography
