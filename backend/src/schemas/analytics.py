from pydantic import BaseModel


class OverviewOut(BaseModel):
    total_questions: int
    total_reviews: int
    total_interviews: int
    mastered_count: int
    error_count: int
    due_today: int


class TrendPoint(BaseModel):
    date: str
    count: int
    avg_rating: float | None = None


class CategoryStatOut(BaseModel):
    category_id: int | None
    category_name: str
    count: int
    mastered: int


class DifficultyStatOut(BaseModel):
    difficulty: int
    count: int
    mastered: int


class HeatmapPoint(BaseModel):
    date: str
    count: int
