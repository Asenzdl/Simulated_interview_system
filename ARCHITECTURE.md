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
| title | TEXT NOT NULL | question title |
| content | TEXT | detailed content (Markdown) |
| answer | TEXT | standard answer (Markdown) |
| category_id | INTEGER FK -> categories.id | category |
| difficulty | INTEGER CHECK(1-5) | difficulty level |
| question_type | VARCHAR(20) | coding/theory/scenario/behavioral |
| is_active | BOOLEAN DEFAULT TRUE | active flag |
| chroma_id | VARCHAR(36) | ChromaDB document ID (UUID) |
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

### interview_sessions
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | |
| question_id | INTEGER FK -> questions.id | |
| status | VARCHAR(20) | active/completed/abandoned |
| overall_score | FLOAT | 0-100 |
| dimension_scores | JSON | 6-dimension scores |
| ai_feedback | TEXT | AI feedback text |
| model_used | VARCHAR(100) | model name used |
| started_at | DATETIME | |
| ended_at | DATETIME | |
| created_at | DATETIME | |

### interview_messages
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | |
| session_id | INTEGER FK -> interview_sessions.id | |
| role | VARCHAR(20) | user/assistant/system |
| content | TEXT NOT NULL | message content |
| created_at | DATETIME | |

### error_records
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | |
| question_id | INTEGER FK -> questions.id | |
| source | VARCHAR(20) | review/interview |
| error_type | VARCHAR(50) | error category |
| user_answer | TEXT | user answer |
| notes | TEXT | user notes |
| is_mastered | BOOLEAN DEFAULT FALSE | mastered flag |
| mastered_at | DATETIME | when mastered |
| created_at | DATETIME | |

### ER Relationships
```
Category 1--N Question N--N Tag (via question_tags)
Question 1--1 CardState (FSRS)
Question 1--N ReviewLog
Question 1--N ErrorRecord
InterviewSession 1--N InterviewMessage
Question 1--N InterviewSession
```

---

## 2. API 端点详细规格

### /api/questions
| Method | Path | Description | Query Params |
|--------|------|-------------|--------------|
| GET | /api/questions | list with pagination, filter, search | page, page_size, category_id, tag, difficulty, search, sort_by, sort_order |
| GET | /api/questions/{id} | single detail | |
| POST | /api/questions | create | |
| PUT | /api/questions/{id} | update | |
| DELETE | /api/questions/{id} | delete | |
| POST | /api/questions/import | bulk import (Markdown/TXT file) | |
| GET | /api/questions/export | export | |

### /api/categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/categories | list |
| POST | /api/categories | create |
| PUT | /api/categories/{id} | update |
| DELETE | /api/categories/{id} | delete |

### /api/review
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/review/due | due card list |
| GET | /api/review/next | next card to review |
| POST | /api/review/{question_id}/rate | submit rating |
| GET | /api/review/stats | today stats |
| GET | /api/review/queue-count | due count |

### /api/interview
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/interview/start | start new session |
| POST | /api/interview/{session_id}/message | send answer, SSE stream response |
| POST | /api/interview/{session_id}/end | end session, trigger AI scoring |
| GET | /api/interview/sessions | session history |
| GET | /api/interview/sessions/{id} | session detail with messages |

### SSE 流式格式
```
event: token
data: {"content": "some text"}

event: done
data: {"full_response": "complete response...", "message_id": 42}
```

### /api/errors
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/errors | list with filter |
| POST | /api/errors | record error |
| PUT | /api/errors/{id} | update (add notes, mark mastered) |
| DELETE | /api/errors/{id} | delete |
| POST | /api/errors/{id}/master | mark mastered |

### /api/similar
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/similar/{question_id} | find similar |
| GET | /api/similar/search | text search similar |

### /api/analytics
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/analytics/overview | total stats |
| GET | /api/analytics/trend | daily trend data |
| GET | /api/analytics/category | category distribution |
| GET | /api/analytics/difficulty | difficulty distribution |
| GET | /api/analytics/heatmap | learning heatmap |
| GET | /api/analytics/interview-scores | interview score trend |

---

## 3. 前端组件树

### Layout
- `AppShell` — Sidebar + Header + Content area
- `Sidebar` — shadcn Sidebar, collapsible
- `Header` — title, theme toggle, search

### Dashboard /
- `OverviewCards` — 4 stat cards (total questions, reviews, mastered, errors)
- `TrendChart` — 7/30 day trend (Recharts line chart)
- `DueQueuePreview` — today's due cards preview
- `RecentActivity` — latest review/interview activity

### Questions /questions
- `QuestionTable` — shadcn DataTable with pagination, filter, sort
- `QuestionDialog` — create/edit modal (shadcn Dialog)
- `QuestionImportDialog` — drag-drop upload, Markdown parse preview
- `CategoryManager` — side Sheet for category CRUD
- `BulkActionBar` — batch operations toolbar

### Review /review
- `FlashCard` — 3D flip card (Framer Motion rotateY 0→180, preserve-3d, backface-hidden)
- `RatingButtons` — Again / Hard / Good / Easy
- `ReviewProgress` — progress bar
- `SimilarQuestionsPanel` — right sidebar with similar questions
- `ReviewComplete` — completion stats dialog

### Interview /interview
- `InterviewConfig` — pre-start settings (question, model)
- `ChatPanel` — conversation container
- `MessageBubble` — user/assistant message with Markdown rendering
- `StreamingText` — typewriter effect for AI response
- `ScoreRadar` — 6-dimension radar chart (Recharts)
- `InterviewHistory` — session list

### Errors /errors
- `ErrorList` — filterable table
- `ErrorDetailDialog` — comparison, notes, mastery toggle

### Analytics /analytics
- `OverviewCards` — total stats
- `TrendChart` — daily review trend
- `CategoryPie` — category distribution
- `DifficultyBar` — difficulty distribution
- `Heatmap` — GitHub-style learning calendar
- `InterviewScores` — interview score trend

---

## 4. 关键技术决策

### 4.1 Async Backend
SQLAlchemy 2.0 async + aiosqlite. FastAPI is async, sync DB blocks event loop. Use create_async_engine with sqlite+aiosqlite URL, async_sessionmaker for session factory, get_db dependency.

### 4.2 SSE Streaming
Use FastAPI EventSourceResponse (sse-starlette). More standard than manual StreamingResponse. Yield dicts with event and data fields.

### 4.3 OpenAI-Compatible LLM
Use openai Python SDK directly. DeepSeek/Moonshot/Qwen all support OpenAI API format. Configure base_url and api_key. Avoid LangChain complexity.

### 4.4 ChromaDB
PersistentClient + OpenAIEmbeddingFunction. Sync on question create/update via upsert. Query with query_texts for similar questions.

### 4.5 FSRS (v6.x)
Use `Scheduler` class, not `FSRS`. API: `Scheduler().review_card(card, Rating.Good)` returns tuple of (Card, ReviewLog). Rating enum: `Rating.Again/1, Rating.Hard/2, Rating.Good/3, Rating.Easy/4`. Serialize Card fields to card_states table.

### 4.6 Frontend SSE
fetch + ReadableStream (EventSource does not support POST). Parse SSE lines from buffer.

### 4.7 3D Flip Card
Framer Motion animate rotateY 0 to 180. transformStyle preserve-3d. backface-hidden on both faces.

### 4.8 Proxy
next.config.ts rewrites /api/* to http://localhost:8000/api/*. X-Accel-Buffering: no header for SSE.

---

## 5. 风险与应对

| 风险 | 可能性 | 应对 |
|------|--------|------|
| LLM 返回格式不稳定 | 高 | JSON mode + 重试 + 正则兜底解析 |
| ChromaDB embedding 不可用 | 中 | 异步处理 + 关键词匹配降级 |
| SSE 流中断 | 中 | 前端重连 + 后端 15s 心跳 |
| aiosqlite 并发限制 | 低 | SQLite WAL 模式 + 单用户场景 |
| FSRS 参数不直观 | 低 | 前端隐藏内部参数，只显示下次复习时间 |

---

## 6. 依赖版本

### Backend (pyproject.toml) — Python >=3.12
- fastapi>=0.115.0 (installed: 0.136.3)
- uvicorn[standard]>=0.34.0 (installed: 0.49.0)
- sqlalchemy[asyncio]>=2.0.0 (installed: 2.0.50)
- aiosqlite>=0.20.0 (installed: 0.22.1)
- alembic>=1.14.0 (installed: 1.18.4)
- chromadb>=0.6.0 (installed: 1.5.9)
- openai>=1.60.0 (installed: 2.41.1)
- fsrs>=4.0.0 (installed: 6.3.1)
- pydantic-settings>=2.0.0 (installed: 2.14.1)
- python-multipart>=0.0.18 (installed: 0.0.32)
- sse-starlette>=2.0.0 (installed: 3.4.4)

### Frontend (package.json)
- next ^16.0.0
- react ^19.0.0
- react-dom ^19.0.0
- framer-motion ^11.0.0
- recharts ^2.15.0
- lucide-react ^0.468.0
- react-markdown ^9.0.0
- remark-gfm ^4.0.0
- highlight.js ^11.11.0
- date-fns ^4.1.0
- zod ^3.24.0

---

## 7. 配置文件参考

### .env.example
```
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL_ID=deepseek-chat
EMBEDDING_MODEL_ID=text-embedding-v3
BACKEND_PORT=8000
```

### next.config.ts
```ts
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
    ];
  },
  async headers() {
    return [
      {
        source: "/api/:path*",
        headers: [
          { key: "X-Accel-Buffering", value: "no" },
        ],
      },
    ];
  },
};
```
