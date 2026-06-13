from __future__ import annotations

from datetime import datetime
from typing import Literal, TypeVar, Generic

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


QuestionType = Literal["theory", "coding", "scenario", "behavioral"]

class QuestionBase(BaseModel):
    title: str = Field(..., max_length=500)
    content: str | None = Field(default=None, max_length=50000)
    answer: str | None = Field(default=None, max_length=50000)
    category_id: int | None = None
    difficulty: int = Field(default=1, ge=1, le=5)
    question_type: QuestionType = "theory"
    is_active: bool = True


class QuestionCreate(QuestionBase):
    tags: list[str] = []


class QuestionUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=500)
    content: str | None = Field(default=None, max_length=50000)
    answer: str | None = Field(default=None, max_length=50000)
    category_id: int | None = None
    difficulty: int | None = Field(default=None, ge=1, le=5)
    question_type: QuestionType | None = None
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
