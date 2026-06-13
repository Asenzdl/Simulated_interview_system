import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import CategoryCreate, CategoryUpdate
from src.services.category_service import (
    create_category,
    get_category,
    list_categories,
    update_category,
    delete_category,
)


async def test_create_category(db_session: AsyncSession):
    data = CategoryCreate(name="JavaScript", color="#f7df1e", icon="js", sort_order=1)
    cat = await create_category(db_session, data)

    assert cat.id is not None
    assert cat.name == "JavaScript"
    assert cat.color == "#f7df1e"
    assert cat.icon == "js"
    assert cat.sort_order == 1


async def test_get_category(db_session: AsyncSession, sample_category):
    cat = await get_category(db_session, sample_category.id)
    assert cat is not None
    assert cat.name == "JavaScript"


async def test_get_category_not_found(db_session: AsyncSession):
    cat = await get_category(db_session, 9999)
    assert cat is None


async def test_list_categories(db_session: AsyncSession, sample_category):
    result = await list_categories(db_session)
    assert result.total == 1
    assert result.items[0].name == "JavaScript"


async def test_list_categories_sorted(db_session: AsyncSession):
    await create_category(db_session, CategoryCreate(name="B", sort_order=2))
    await create_category(db_session, CategoryCreate(name="A", sort_order=1))

    result = await list_categories(db_session)
    assert result.items[0].name == "A"
    assert result.items[1].name == "B"


async def test_update_category(db_session: AsyncSession, sample_category):
    cat = await update_category(db_session, sample_category.id, CategoryUpdate(name="TS", color="#3178c6"))
    assert cat is not None
    assert cat.name == "TS"
    assert cat.color == "#3178c6"


async def test_update_category_not_found(db_session: AsyncSession):
    cat = await update_category(db_session, 9999, CategoryUpdate(name="X"))
    assert cat is None


async def test_delete_category(db_session: AsyncSession, sample_category):
    ok = await delete_category(db_session, sample_category.id)
    assert ok is True
    cat = await get_category(db_session, sample_category.id)
    assert cat is None


async def test_delete_category_not_found(db_session: AsyncSession):
    ok = await delete_category(db_session, 9999)
    assert ok is False
