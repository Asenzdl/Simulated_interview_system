from fastapi import APIRouter

router = APIRouter(prefix="/api/interview", tags=["interview"])


@router.post("/start")
async def start_interview():
    return {"message": "TODO"}


@router.post("/{session_id}/message")
async def send_message(session_id: int):
    return {"message": "TODO"}


@router.post("/{session_id}/end")
async def end_interview(session_id: int):
    return {"message": "TODO"}


@router.get("/sessions")
async def list_sessions():
    return {"items": [], "total": 0}


@router.get("/sessions/{session_id}")
async def get_session(session_id: int):
    return {"message": "TODO"}
