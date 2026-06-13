from fastapi import APIRouter

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/overview")
async def overview():
    return {"total_questions": 0, "total_reviews": 0, "total_interviews": 0}


@router.get("/trend")
async def trend():
    return {"items": []}


@router.get("/category")
async def category_stats():
    return {"items": []}


@router.get("/difficulty")
async def difficulty_stats():
    return {"items": []}


@router.get("/heatmap")
async def heatmap():
    return {"items": []}


@router.get("/interview-scores")
async def interview_scores():
    return {"items": []}
