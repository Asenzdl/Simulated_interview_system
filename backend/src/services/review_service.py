"""Phase 3.1 — FSRS-based spaced repetition review service."""

from __future__ import annotations

from datetime import datetime, timezone

from fsrs import Scheduler, Card, Rating, State
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Question, CardState, ReviewLog
from src.schemas.review import CardStateOut, ReviewStatsOut

_scheduler = Scheduler(desired_retention=0.9)


# ── helpers ───────────────────────────────────────────────────────────────


def _ensure_utc(dt: datetime | None) -> datetime | None:
    """Ensure a datetime is timezone-aware UTC (SQLite returns naive datetimes)."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def _card_state_to_fsrs(cs: CardState, question_id: int) -> Card:
    """Convert a DB CardState to an fsrs Card."""
    return Card.from_dict({
        "card_id": question_id,
        "state": cs.state,
        "step": 0,
        "stability": cs.stability if cs.stability else None,
        "difficulty": cs.difficulty if cs.difficulty else None,
        "due": _ensure_utc(cs.due).isoformat(),
        "last_review": _ensure_utc(cs.last_review).isoformat() if cs.last_review else None,
    })


def _db_card_to_out(cs: CardState) -> CardStateOut:
    return CardStateOut.model_validate(cs)


# ── public API ────────────────────────────────────────────────────────────


async def get_due_cards(db: AsyncSession) -> list[CardStateOut]:
    """Return all cards due for review (including new questions without CardState).

    Results ordered by due date ascending (newest due first).
    """
    now = datetime.now(timezone.utc)
    items: list[CardStateOut] = []

    # 1. Cards with CardState that are due
    result = await db.execute(
        select(CardState)
        .where(CardState.due <= now)
        .order_by(CardState.due.asc())
    )
    for cs in result.scalars().all():
        items.append(_db_card_to_out(cs))

    # 2. Questions without any CardState (new cards — due immediately)
    existing_ids = {cs.question_id for cs in items}
    new_q_result = await db.execute(
        select(Question.id)
        .where(Question.is_active == True)  # noqa: E712
        .where(~Question.id.in_(select(CardState.question_id)))
    )
    for qid in new_q_result.scalars().all():
        if qid not in existing_ids:
            items.append(CardStateOut(
                question_id=qid,
                due=now,
                stability=0.0,
                difficulty=0.0,
                elapsed_days=0,
                scheduled_days=0,
                reps=0,
                lapses=0,
                state=0,
                last_review=None,
            ))

    return items


async def get_next_card(db: AsyncSession) -> CardStateOut | None:
    """Return the next due card, or None if queue is empty."""
    items = await get_due_cards(db)
    return items[0] if items else None


async def rate_card(db: AsyncSession, question_id: int, rating: int) -> CardStateOut:
    """Rate a card and update its FSRS schedule.

    Creates CardState if it doesn't exist. Always creates a ReviewLog.
    """
    if rating < 1 or rating > 4:
        raise ValueError("评分值无效，必须为 1-4")

    # Verify question exists
    q = (await db.execute(select(Question).where(Question.id == question_id))).scalar_one_or_none()
    if q is None:
        raise ValueError("题目不存在")

    now = datetime.now(timezone.utc)

    # Load or create CardState
    cs = (await db.execute(select(CardState).where(CardState.question_id == question_id))).scalar_one_or_none()
    if cs is None:
        # New card — start with default FSRS card
        fsrs_card = Card()
    else:
        fsrs_card = _card_state_to_fsrs(cs, question_id)

    # Snapshot before review
    state_before = fsrs_card.state.value if isinstance(fsrs_card.state, State) else fsrs_card.state

    # Review with FSRS
    updated_card, review_log = _scheduler.review_card(fsrs_card, Rating(rating))

    state_after = updated_card.state.value if isinstance(updated_card.state, State) else updated_card.state

    # Upsert CardState
    if cs is None:
        cs = CardState(question_id=question_id, due=updated_card.due, reps=0, lapses=0)
        db.add(cs)

    cs.due = updated_card.due
    cs.stability = updated_card.stability or 0.0
    cs.difficulty = updated_card.difficulty or 0.0
    cs.state = state_after
    cs.last_review = now
    cs.reps += 1
    if rating == 1:  # Again
        cs.lapses += 1

    # Create ReviewLog
    log = ReviewLog(
        question_id=question_id,
        rating=rating,
        review_datetime=now,
        state_before=state_before,
        state_after=state_after,
        elapsed_days=0,
        scheduled_days=0,
    )
    db.add(log)

    await db.commit()
    await db.refresh(cs)
    return _db_card_to_out(cs)


async def get_review_stats(db: AsyncSession) -> ReviewStatsOut:
    """Return review statistics."""
    now = datetime.now(timezone.utc)

    # Count due cards: CardState due <= now + new questions without CardState
    due_cs = (await db.execute(
        select(func.count()).select_from(CardState).where(CardState.due <= now)
    )).scalar_one()

    new_q = (await db.execute(
        select(func.count()).select_from(Question)
        .where(Question.is_active == True)  # noqa: E712
        .where(~Question.id.in_(select(CardState.question_id)))
    )).scalar_one()

    due_count = due_cs + new_q

    # Count ratings
    again_count = (await db.execute(
        select(func.count()).select_from(ReviewLog).where(ReviewLog.rating == 1)
    )).scalar_one()
    hard_count = (await db.execute(
        select(func.count()).select_from(ReviewLog).where(ReviewLog.rating == 2)
    )).scalar_one()
    good_count = (await db.execute(
        select(func.count()).select_from(ReviewLog).where(ReviewLog.rating == 3)
    )).scalar_one()
    easy_count = (await db.execute(
        select(func.count()).select_from(ReviewLog).where(ReviewLog.rating == 4)
    )).scalar_one()

    return ReviewStatsOut(
        total_reviewed=again_count + hard_count + good_count + easy_count,
        again_count=again_count,
        hard_count=hard_count,
        good_count=good_count,
        easy_count=easy_count,
        due_count=due_count,
    )
