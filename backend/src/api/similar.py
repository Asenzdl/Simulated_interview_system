from fastapi import APIRouter

router = APIRouter(prefix="/api/similar", tags=["similar"])


@router.get("/{question_id}")
async def find_similar(question_id: int):
    return {"items": []}


@router.get("/search")
async def search_similar(q: str = ""):
    return {"items": []}
