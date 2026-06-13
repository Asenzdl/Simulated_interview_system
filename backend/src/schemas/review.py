from datetime import datetime

from pydantic import BaseModel, Field


class RateRequest(BaseModel):
    rating: int = Field(ge=1, le=4)  # 1=Again 2=Hard 3=Good 4=Easy


class CardStateOut(BaseModel):
    question_id: int
    due: datetime
    stability: float
    difficulty: float
    elapsed_days: int
    scheduled_days: int
    reps: int
    lapses: int
    state: int
    last_review: datetime | None = None

    model_config = {"from_attributes": True}


class ReviewStatsOut(BaseModel):
    total_reviewed: int
    again_count: int
    hard_count: int
    good_count: int
    easy_count: int
    due_count: int
