import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import QuestionCreate, QuestionUpdate
from src.services.question_service import (
    create_question,
    get_question,
    list_questions,
    update_question,
    delete_question,
)


# ── create ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_question_basic(db_session: AsyncSession):
    data = QuestionCreate(title="什么是 Promise？")
    q = await create_question(db_session, data)

    assert q.id is not None
    assert q.title == "什么是 Promise？"
    assert q.difficulty == 1
    assert q.question_type == "theory"
    assert q.is_active is True
    assert q.tags == []
    assert q.category is None


@pytest.mark.asyncio
async def test_create_question_with_tags(db_session: AsyncSession):
    data = QuestionCreate(title="闭包", tags=["JS", "作用域"])
    q = await create_question(db_session, data)

    assert len(q.tags) == 2
    tag_names = {t.name for t in q.tags}
    assert tag_names == {"JS", "作用域"}


@pytest.mark.asyncio
async def test_create_question_with_category(db_session: AsyncSession, sample_category):
    data = QuestionCreate(title="原型链", category_id=sample_category.id)
    q = await create_question(db_session, data)

    assert q.category is not None
    assert q.category.id == sample_category.id
    assert q.category.name == "JavaScript"


@pytest.mark.asyncio
async def test_create_question_reuses_existing_tags(db_session: AsyncSession):
    """相同 tag name 不应重复创建"""
    await create_question(db_session, QuestionCreate(title="Q1", tags=["JS"]))
    q2 = await create_question(db_session, QuestionCreate(title="Q2", tags=["JS"]))

    from src.models import Tag
    result = await db_session.execute(Tag.__table__.select())
    all_tags = result.fetchall()
    assert len(all_tags) == 1
    assert q2.tags[0].id == all_tags[0].id


# ── get ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_question(db_session: AsyncSession, sample_question):
    q = await get_question(db_session, sample_question.id)

    assert q is not None
    assert q.title == "什么是闭包？"
    assert q.category is not None
    assert len(q.tags) == 2


@pytest.mark.asyncio
async def test_get_question_not_found(db_session: AsyncSession):
    q = await get_question(db_session, 9999)
    assert q is None


# ── list ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_questions_empty(db_session: AsyncSession):
    result = await list_questions(db_session)
    assert result.items == []
    assert result.total == 0


@pytest.mark.asyncio
async def test_list_questions_with_data(db_session: AsyncSession, sample_question):
    result = await list_questions(db_session)
    assert result.total == 1
    assert len(result.items) == 1
    assert result.items[0].title == "什么是闭包？"


@pytest.mark.asyncio
async def test_list_questions_pagination(db_session: AsyncSession):
    for i in range(5):
        await create_question(db_session, QuestionCreate(title=f"Q{i}"))

    page1 = await list_questions(db_session, page=1, page_size=2)
    assert page1.total == 5
    assert len(page1.items) == 2
    assert page1.pages == 3

    page3 = await list_questions(db_session, page=3, page_size=2)
    assert len(page3.items) == 1


@pytest.mark.asyncio
async def test_list_questions_filter_category(db_session: AsyncSession, sample_category):
    await create_question(db_session, QuestionCreate(title="A", category_id=sample_category.id))
    await create_question(db_session, QuestionCreate(title="B"))

    result = await list_questions(db_session, category_id=sample_category.id)
    assert result.total == 1
    assert result.items[0].title == "A"


@pytest.mark.asyncio
async def test_list_questions_filter_difficulty(db_session: AsyncSession):
    await create_question(db_session, QuestionCreate(title="Easy", difficulty=1))
    await create_question(db_session, QuestionCreate(title="Hard", difficulty=5))

    result = await list_questions(db_session, difficulty=5)
    assert result.total == 1
    assert result.items[0].title == "Hard"


@pytest.mark.asyncio
async def test_list_questions_search(db_session: AsyncSession):
    await create_question(db_session, QuestionCreate(title="什么是闭包？"))
    await create_question(db_session, QuestionCreate(title="Promise 用法"))

    result = await list_questions(db_session, search="闭包")
    assert result.total == 1
    assert "闭包" in result.items[0].title


# ── update ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_question_title(db_session: AsyncSession, sample_question):
    q = await update_question(db_session, sample_question.id, QuestionUpdate(title="新标题"))
    assert q is not None
    assert q.title == "新标题"


@pytest.mark.asyncio
async def test_update_question_tags(db_session: AsyncSession, sample_question):
    q = await update_question(db_session, sample_question.id, QuestionUpdate(tags=["新标签"]))
    assert q is not None
    tag_names = {t.name for t in q.tags}
    assert tag_names == {"新标签"}


@pytest.mark.asyncio
async def test_update_question_clear_tags(db_session: AsyncSession, sample_question):
    q = await update_question(db_session, sample_question.id, QuestionUpdate(tags=[]))
    assert q is not None
    assert q.tags == []


@pytest.mark.asyncio
async def test_update_question_not_found(db_session: AsyncSession):
    q = await update_question(db_session, 9999, QuestionUpdate(title="X"))
    assert q is None


@pytest.mark.asyncio
async def test_update_question_partial(db_session: AsyncSession, sample_question):
    original_title = sample_question.title
    q = await update_question(db_session, sample_question.id, QuestionUpdate(difficulty=5))
    assert q is not None
    assert q.title == original_title  # 不变
    assert q.difficulty == 5


# ── delete ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_question(db_session: AsyncSession, sample_question):
    ok = await delete_question(db_session, sample_question.id)
    assert ok is True

    q = await get_question(db_session, sample_question.id)
    assert q is None


@pytest.mark.asyncio
async def test_delete_question_not_found(db_session: AsyncSession):
    ok = await delete_question(db_session, 9999)
    assert ok is False
