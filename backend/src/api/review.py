from fastapi import APIRouter

router = APIRouter(prefix="/api/review", tags=["review"])


@router.get("/due")
async def get_due_cards():
    return {"items": [], "total": 0}


@router.get("/next")
async def get_next_card():
    return {"message": "TODO"}


@router.post("/{question_id}/rate")
async def rate_card(question_id: int):
    return {"message": "TODO"}


@router.get("/stats")
async def review_stats():
    return {"total_reviewed": 0, "due_count": 0}


@router.get("/queue-count")
async def queue_count():
    return {"count": 0}
