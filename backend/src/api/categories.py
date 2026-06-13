from fastapi import APIRouter

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/")
async def list_categories():
    return {"items": [], "total": 0}


@router.post("/")
async def create_category():
    return {"message": "TODO"}


@router.put("/{category_id}")
async def update_category(category_id: int):
    return {"message": "TODO"}


@router.delete("/{category_id}")
async def delete_category(category_id: int):
    return {"message": "TODO"}
