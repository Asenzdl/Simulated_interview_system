from datetime import datetime
from typing import TypeVar, Generic

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class QuestionBase(BaseModel):
    title: str
    content: str | None = None
    answer: str | None = None
    category_id: int | None = None
    difficulty: int = Field(default=1, ge=1, le=5)
    question_type: str = "theory"
    is_active: bool = True


class QuestionCreate(QuestionBase):
    tags: list[str] = []


class QuestionUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    answer: str | None = None
    category_id: int | None = None
    difficulty: int | None = Field(default=None, ge=1, le=5)
    question_type: str | None = None
    is_active: bool | None = None
    tags: list[str] | None = None


class QuestionOut(QuestionBase):
    id: int
    chroma_id: str | None = None
    created_at: datetime
    updated_at: datetime
    category: CategoryOut | None = None
    tags: list[TagOut] = []

    model_config = {"from_attributes": True}


# Avoid circular import
from .category import CategoryOut  # noqa: E402

QuestionOut.model_rebuild()
