from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.review import RateRequest, CardStateOut, ReviewStatsOut
from ..services.review_service import get_due_cards, get_next_card, rate_card, get_review_stats

router = APIRouter(prefix="/api/review", tags=["review"])


@router.get("/due", response_model=list[CardStateOut])
async def get_due(db: AsyncSession = Depends(get_db)):
    return await get_due_cards(db)


@router.get("/next", response_model=CardStateOut | None)
async def next_card(db: AsyncSession = Depends(get_db)):
    card = await get_next_card(db)
    return card


@router.post("/{question_id}/rate", response_model=CardStateOut)
async def rate(question_id: int, body: RateRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await rate_card(db, question_id, body.rating)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stats", response_model=ReviewStatsOut)
async def stats(db: AsyncSession = Depends(get_db)):
    return await get_review_stats(db)


@router.get("/queue-count")
async def queue_count(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select, func
    from ..models import CardState, Question

    now = datetime.now(timezone.utc)
    due_cs = (await db.execute(
        select(func.count()).select_from(CardState).where(CardState.due <= now)
    )).scalar_one()
    new_q = (await db.execute(
        select(func.count()).select_from(Question)
        .where(Question.is_active == True)  # noqa: E712
        .where(~Question.id.in_(select(CardState.question_id)))
    )).scalar_one()
    return {"count": due_cs + new_q}
