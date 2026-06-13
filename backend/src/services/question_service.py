from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Question, Tag, question_tags
from src.schemas import QuestionCreate, QuestionUpdate, QuestionOut, PageResult


async def _get_or_create_tags(db: AsyncSession, tag_names: list[str]) -> list[Tag]:
    tags = []
    for name in tag_names:
        result = await db.execute(select(Tag).where(Tag.name == name))
        tag = result.scalar_one_or_none()
        if tag is None:
            tag = Tag(name=name)
            db.add(tag)
            await db.flush()
        tags.append(tag)
    return tags


def _to_out(q: Question) -> QuestionOut:
    return QuestionOut.model_validate(q)


async def create_question(db: AsyncSession, data: QuestionCreate) -> QuestionOut:
    q = Question(
        title=data.title,
        content=data.content,
        answer=data.answer,
        category_id=data.category_id,
        difficulty=data.difficulty,
        question_type=data.question_type,
        is_active=data.is_active,
    )
    if data.tags:
        q.tags = await _get_or_create_tags(db, data.tags)

    db.add(q)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("该标题已存在，请使用其他标题")

    result = await db.execute(
        select(Question)
        .options(selectinload(Question.category), selectinload(Question.tags))
        .where(Question.id == q.id)
    )
    return _to_out(result.scalar_one())


async def get_question(db: AsyncSession, question_id: int) -> QuestionOut | None:
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.category), selectinload(Question.tags))
        .where(Question.id == question_id)
    )
    q = result.scalar_one_or_none()
    return _to_out(q) if q else None


async def list_questions(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    category_id: int | None = None,
    difficulty: int | None = None,
    is_active: bool | None = None,
    search: str | None = None,
) -> PageResult[QuestionOut]:
    base = select(Question).options(
        selectinload(Question.category), selectinload(Question.tags)
    )
    count_base = select(func.count()).select_from(Question)

    if category_id is not None:
        base = base.where(Question.category_id == category_id)
        count_base = count_base.where(Question.category_id == category_id)
    if difficulty is not None:
        base = base.where(Question.difficulty == difficulty)
        count_base = count_base.where(Question.difficulty == difficulty)
    if is_active is not None:
        base = base.where(Question.is_active == is_active)
        count_base = count_base.where(Question.is_active == is_active)
    if search:
        base = base.where(Question.title.contains(search))
        count_base = count_base.where(Question.title.contains(search))

    total = (await db.execute(count_base)).scalar_one()
    pages = (total + page_size - 1) // page_size if total > 0 else 0

    offset = (page - 1) * page_size
    result = await db.execute(base.order_by(Question.id.desc()).offset(offset).limit(page_size))
    items = [_to_out(q) for q in result.scalars().all()]

    return PageResult(items=items, total=total, page=page, page_size=page_size, pages=pages)


async def update_question(
    db: AsyncSession, question_id: int, data: QuestionUpdate
) -> QuestionOut | None:
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.tags))
        .where(Question.id == question_id)
    )
    q = result.scalar_one_or_none()
    if q is None:
        return None

    update_data = data.model_dump(exclude_unset=True)
    tags_data = update_data.pop("tags", None)

    for field, value in update_data.items():
        setattr(q, field, value)

    if tags_data is not None:
        q.tags = await _get_or_create_tags(db, tags_data) if tags_data else []

    await db.commit()

    result = await db.execute(
        select(Question)
        .options(selectinload(Question.category), selectinload(Question.tags))
        .where(Question.id == question_id)
    )
    return _to_out(result.scalar_one())


async def delete_question(db: AsyncSession, question_id: int) -> bool:
    result = await db.execute(select(Question).where(Question.id == question_id))
    q = result.scalar_one_or_none()
    if q is None:
        return False
    await db.delete(q)
    await db.commit()
    return True
