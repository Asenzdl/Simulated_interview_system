from fastapi import APIRouter

router = APIRouter(prefix="/api/errors", tags=["errors"])


@router.get("/")
async def list_errors():
    return {"items": [], "total": 0}


@router.post("/")
async def create_error():
    return {"message": "TODO"}


@router.put("/{error_id}")
async def update_error(error_id: int):
    return {"message": "TODO"}


@router.delete("/{error_id}")
async def delete_error(error_id: int):
    return {"message": "TODO"}


@router.post("/{error_id}/master")
async def mark_mastered(error_id: int):
    return {"message": "TODO"}
