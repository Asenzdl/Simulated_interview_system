from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas import CategoryCreate, CategoryUpdate, CategoryOut, PageResult
from src.services.category_service import (
    create_category,
    get_category,
    list_categories,
    update_category,
    delete_category,
)

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/", response_model=PageResult[CategoryOut])
async def list_categories_api(db: AsyncSession = Depends(get_db)):
    return await list_categories(db)


@router.post("/", response_model=CategoryOut, status_code=201)
async def create_category_api(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await create_category(db, data)


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category_api(
    category_id: int, data: CategoryUpdate, db: AsyncSession = Depends(get_db)
):
    cat = await update_category(db, category_id, data)
    if cat is None:
        raise HTTPException(status_code=404, detail="分类不存在")
    return cat


@router.delete("/{category_id}", status_code=204)
async def delete_category_api(category_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_category(db, category_id)
    if not ok:
        raise HTTPException(status_code=404, detail="分类不存在")
