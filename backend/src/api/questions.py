from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas import QuestionCreate, QuestionUpdate, QuestionOut, PageResult
from src.services.question_service import (
    create_question,
    get_question,
    list_questions,
    update_question,
    delete_question,
)
from src.services.import_service import import_questions

router = APIRouter(prefix="/api/questions", tags=["questions"])


@router.get("/", response_model=PageResult[QuestionOut])
async def list_questions_api(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: int | None = None,
    difficulty: int | None = Query(None, ge=1, le=5),
    is_active: bool | None = None,
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await list_questions(
        db, page=page, page_size=page_size,
        category_id=category_id, difficulty=difficulty,
        is_active=is_active, search=search,
    )


@router.post("/", response_model=QuestionOut, status_code=201)
async def create_question_api(data: QuestionCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_question(db, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{question_id}", response_model=QuestionOut)
async def get_question_api(question_id: int, db: AsyncSession = Depends(get_db)):
    q = await get_question(db, question_id)
    if q is None:
        raise HTTPException(status_code=404, detail="题目不存在")
    return q


@router.put("/{question_id}", response_model=QuestionOut)
async def update_question_api(
    question_id: int, data: QuestionUpdate, db: AsyncSession = Depends(get_db)
):
    q = await update_question(db, question_id, data)
    if q is None:
        raise HTTPException(status_code=404, detail="题目不存在")
    return q


@router.delete("/{question_id}", status_code=204)
async def delete_question_api(question_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_question(db, question_id)
    if not ok:
        raise HTTPException(status_code=404, detail="题目不存在")


@router.post("/import")
async def import_questions_api(
    file_content: str = Body(..., media_type="text/plain"),
    category_id: int | None = None,
    difficulty: int = Query(1, ge=1, le=5),
    db: AsyncSession = Depends(get_db),
):
    if len(file_content) > 1_000_000:
        raise HTTPException(status_code=413, detail="导入内容过大（最大 1MB）")
    result = await import_questions(db, file_content, category_id=category_id, difficulty=difficulty)
    return result
