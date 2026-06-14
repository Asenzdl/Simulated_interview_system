"""Phase 3.1 — review_service.py TDD tests."""

from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Question, CardState, ReviewLog, Category
from src.schemas import RateRequest


# ── fixtures ──────────────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def category(db_session: AsyncSession):
    cat = Category(name="JavaScript", color="#f7df1e", icon="js", sort_order=1)
    db_session.add(cat)
    await db_session.commit()
    await db_session.refresh(cat)
    return cat


@pytest_asyncio.fixture
async def question_a(db_session: AsyncSession, category):
    q = Question(title="什么是闭包？", content="解释闭包", answer="闭包是...", category_id=category.id, difficulty=3)
    db_session.add(q)
    await db_session.commit()
    await db_session.refresh(q)
    return q


@pytest_asyncio.fixture
async def question_b(db_session: AsyncSession, category):
    q = Question(title="什么是 Promise？", content="解释 Promise", answer="Promise 是...", category_id=category.id, difficulty=2)
    db_session.add(q)
    await db_session.commit()
    await db_session.refresh(q)
    return q


@pytest_asyncio.fixture
async def due_card(db_session: AsyncSession, question_a):
    """A card that is already due (due in the past)."""
    now = datetime.now(timezone.utc)
    card = CardState(
        question_id=question_a.id,
        due=now - timedelta(minutes=5),
        stability=2.5,
        difficulty=5.0,
        state=2,  # Review
        reps=3,
    )
    db_session.add(card)
    await db_session.commit()
    await db_session.refresh(card)
    return card


@pytest_asyncio.fixture
async def not_due_card(db_session: AsyncSession, question_b):
    """A card that is NOT yet due."""
    now = datetime.now(timezone.utc)
    card = CardState(
        question_id=question_b.id,
        due=now + timedelta(days=2),
        stability=10.0,
        difficulty=3.0,
        state=2,  # Review
        reps=5,
    )
    db_session.add(card)
    await db_session.commit()
    await db_session.refresh(card)
    return card


# ── import service under test (will fail until implemented) ───────────────

from src.services.review_service import get_due_cards, get_next_card, rate_card, get_review_stats


# ── get_due_cards ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_due_cards_returns_due(db_session, due_card, question_a):
    items = await get_due_cards(db_session)
    assert len(items) == 1
    assert items[0].question_id == question_a.id


@pytest.mark.asyncio
async def test_get_due_cards_excludes_not_due(db_session, due_card, not_due_card):
    items = await get_due_cards(db_session)
    assert len(items) == 1  # only due_card


@pytest.mark.asyncio
async def test_get_due_cards_empty_when_none_due(db_session, not_due_card):
    items = await get_due_cards(db_session)
    assert len(items) == 0


@pytest.mark.asyncio
async def test_get_due_cards_includes_new_questions(db_session, question_a):
    """Questions without CardState should also appear (new cards, due immediately)."""
    items = await get_due_cards(db_session)
    assert len(items) == 1
    assert items[0].question_id == question_a.id


@pytest.mark.asyncio
async def test_get_due_cards_ordered_by_due(db_session, category):
    """Due cards should be ordered by due date ascending."""
    now = datetime.now(timezone.utc)
    q1 = Question(title="Q1", answer="a", category_id=category.id)
    q2 = Question(title="Q2", answer="a", category_id=category.id)
    db_session.add_all([q1, q2])
    await db_session.flush()

    c1 = CardState(question_id=q1.id, due=now - timedelta(hours=1), state=2)
    c2 = CardState(question_id=q2.id, due=now - timedelta(minutes=10), state=2)
    db_session.add_all([c1, c2])
    await db_session.commit()

    items = await get_due_cards(db_session)
    assert len(items) == 2
    assert items[0].question_id == q1.id  # earlier due first (ascending)
    assert items[1].question_id == q2.id


# ── get_next_card ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_next_card_returns_earliest_due(db_session, due_card, question_a):
    card = await get_next_card(db_session)
    assert card is not None
    assert card.question_id == question_a.id


@pytest.mark.asyncio
async def test_get_next_card_returns_none_when_empty(db_session):
    card = await get_next_card(db_session)
    assert card is None


@pytest.mark.asyncio
async def test_get_next_card_skips_not_due(db_session, not_due_card):
    card = await get_next_card(db_session)
    assert card is None


# ── rate_card ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_rate_new_card_creates_card_state(db_session, question_a):
    """Rating a question that has no CardState should create one."""
    result = await rate_card(db_session, question_a.id, 3)  # Good
    assert result.question_id == question_a.id
    assert result.state in (1, 2)  # Learning or Review
    assert result.reps == 1

    # Verify CardState persisted in DB
    from sqlalchemy import select
    cs = (await db_session.execute(
        select(CardState).where(CardState.question_id == question_a.id)
    )).scalar_one_or_none()
    assert cs is not None
    assert cs.reps == 1


@pytest.mark.asyncio
async def test_rate_existing_card_updates_state(db_session, due_card, question_a):
    """Rating a question that already has CardState should update it."""
    old_reps = due_card.reps
    old_due = due_card.due
    result = await rate_card(db_session, question_a.id, 3)  # Good
    assert result.reps == old_reps + 1
    # Due should have changed
    assert result.due != old_due


@pytest.mark.asyncio
async def test_rate_creates_review_log(db_session, question_a):
    """Each rating should create a ReviewLog entry."""
    await rate_card(db_session, question_a.id, 3)

    from sqlalchemy import select, func
    count = (await db_session.execute(
        select(func.count()).select_from(ReviewLog).where(ReviewLog.question_id == question_a.id)
    )).scalar_one()
    assert count == 1


@pytest.mark.asyncio
async def test_rate_again_resets_card(db_session, question_a):
    """Rating Again should increase lapses."""
    await rate_card(db_session, question_a.id, 3)  # first Good
    result = await rate_card(db_session, question_a.id, 1)  # Again
    assert result.lapses >= 1


@pytest.mark.asyncio
async def test_rate_nonexistent_question_raises(db_session):
    with pytest.raises(ValueError, match="题目不存在"):
        await rate_card(db_session, 99999, 3)


@pytest.mark.asyncio
async def test_rate_invalid_rating_raises(db_session, question_a):
    with pytest.raises(ValueError, match="评分值无效"):
        await rate_card(db_session, question_a.id, 0)
    with pytest.raises(ValueError, match="评分值无效"):
        await rate_card(db_session, question_a.id, 5)


# ── get_review_stats ──────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_stats_empty(db_session):
    stats = await get_review_stats(db_session)
    assert stats.total_reviewed == 0
    assert stats.due_count == 0
    assert stats.again_count == 0


@pytest.mark.asyncio
async def test_stats_counts_ratings(db_session, question_a, question_b):
    await rate_card(db_session, question_a.id, 3)  # Good
    await rate_card(db_session, question_a.id, 1)  # Again
    await rate_card(db_session, question_b.id, 4)  # Easy

    stats = await get_review_stats(db_session)
    assert stats.total_reviewed == 3
    assert stats.good_count == 1
    assert stats.again_count == 1
    assert stats.easy_count == 1


@pytest.mark.asyncio
async def test_stats_due_count(db_session, due_card, not_due_card):
    stats = await get_review_stats(db_session)
    assert stats.due_count == 1
