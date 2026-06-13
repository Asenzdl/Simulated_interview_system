from fastapi import APIRouter

router = APIRouter(prefix="/api/questions", tags=["questions"])


@router.get("/")
async def list_questions():
    return {"items": [], "total": 0}


@router.post("/")
async def create_question():
    return {"message": "TODO"}


@router.get("/{question_id}")
async def get_question(question_id: int):
    return {"message": "TODO"}


@router.put("/{question_id}")
async def update_question(question_id: int):
    return {"message": "TODO"}


@router.delete("/{question_id}")
async def delete_question(question_id: int):
    return {"message": "TODO"}


@router.post("/import")
async def import_questions():
    return {"message": "TODO"}
