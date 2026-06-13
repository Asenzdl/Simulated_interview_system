from __future__ import annotations

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Category
from src.schemas import CategoryCreate, CategoryUpdate, CategoryOut, PageResult


def _to_out(c: Category) -> CategoryOut:
    return CategoryOut.model_validate(c)


async def create_category(db: AsyncSession, data: CategoryCreate) -> CategoryOut:
    cat = Category(**data.model_dump())
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return _to_out(cat)


async def get_category(db: AsyncSession, category_id: int) -> CategoryOut | None:
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    return _to_out(cat) if cat else None


async def list_categories(db: AsyncSession) -> PageResult[CategoryOut]:
    count = (await db.execute(select(func.count()).select_from(Category))).scalar_one()
    result = await db.execute(select(Category).order_by(Category.sort_order, Category.id))
    items = [_to_out(c) for c in result.scalars().all()]
    return PageResult(items=items, total=count, page=1, page_size=count, pages=1)


async def update_category(
    db: AsyncSession, category_id: int, data: CategoryUpdate
) -> CategoryOut | None:
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if cat is None:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cat, field, value)

    await db.commit()
    await db.refresh(cat)
    return _to_out(cat)


async def delete_category(db: AsyncSession, category_id: int) -> bool:
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if cat is None:
        return False
    await db.delete(cat)
    await db.commit()
    return True
