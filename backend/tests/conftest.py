import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database import Base
from src.models import Category, Tag, Question  # noqa: F401 — ensure models registered


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def sample_category(db_session: AsyncSession):
    cat = Category(name="JavaScript", color="#f7df1e", icon="js", sort_order=1)
    db_session.add(cat)
    await db_session.commit()
    await db_session.refresh(cat)
    return cat


@pytest_asyncio.fixture
async def sample_question(db_session: AsyncSession, sample_category):
    from src.services.question_service import create_question
    from src.schemas import QuestionCreate

    data = QuestionCreate(
        title="什么是闭包？",
        content="请解释 JavaScript 闭包的概念",
        answer="闭包是函数和其词法环境的组合...",
        category_id=sample_category.id,
        difficulty=3,
        question_type="theory",
        tags=["闭包", "作用域"],
    )
    return await create_question(db_session, data)
