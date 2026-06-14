from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Question, CardState, ReviewLog

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/overview")
async def overview(db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # 总题数
    total = (await db.execute(
        select(func.count()).select_from(Question)
    )).scalar_one()

    # 待复习：CardState 已到期 + 无 CardState 的新题
    due_cs = (await db.execute(
        select(func.count()).select_from(CardState).where(CardState.due <= now)
    )).scalar_one()
    new_q = (await db.execute(
        select(func.count()).select_from(Question)
        .where(Question.is_active == True)  # noqa: E712
        .where(~Question.id.in_(select(CardState.question_id)))
    )).scalar_one()
    due_count = due_cs + new_q

    # 已掌握：reps >= 3 且 stability >= 10 的卡片
    mastered = (await db.execute(
        select(func.count()).select_from(CardState)
        .where(CardState.reps >= 3, CardState.stability >= 10)
    )).scalar_one()

    # 今日已复习
    today_reviewed = (await db.execute(
        select(func.count()).select_from(ReviewLog)
        .where(ReviewLog.review_datetime >= today_start)
    )).scalar_one()

    return {
        "total_questions": total,
        "due_count": due_count,
        "mastered_count": mastered,
        "today_reviewed": today_reviewed,
    }
