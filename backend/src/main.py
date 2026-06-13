from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .config import settings
from . import models  # noqa: F401
from .api import questions, categories, review, interview, errors, analytics, similar


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Only create tables if DB file doesn't exist (first run)
    db_path = Path(settings.database_url.replace("sqlite+aiosqlite:///", ""))
    if not db_path.exists():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="面试系统 API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


app.include_router(questions.router)
app.include_router(categories.router)
app.include_router(review.router)
app.include_router(interview.router)
app.include_router(errors.router)
app.include_router(analytics.router)
app.include_router(similar.router)
