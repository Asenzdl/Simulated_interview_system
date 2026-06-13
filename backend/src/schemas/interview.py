from datetime import datetime

from pydantic import BaseModel


class InterviewStartRequest(BaseModel):
    question_id: int | None = None
    title: str | None = None


class InterviewMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class InterviewSessionOut(BaseModel):
    id: int
    question_id: int | None = None
    status: str
    overall_score: float | None = None
    dimension_scores: str | None = None
    ai_feedback: str | None = None
    model_used: str | None = None
    started_at: datetime
    ended_at: datetime | None = None
    created_at: datetime
    messages: list[InterviewMessageOut] = []

    model_config = {"from_attributes": True}


class InterviewScoreOut(BaseModel):
    overall_score: float
    dimension_scores: dict
    ai_feedback: str
