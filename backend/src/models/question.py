from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .tag import question_tags


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    content: Mapped[str | None] = mapped_column(Text)
    answer: Mapped[str | None] = mapped_column(Text)
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("categories.id"), index=True)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    question_type: Mapped[str] = mapped_column(String(20), default="theory")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    chroma_id: Mapped[str | None] = mapped_column(String(36))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    category = relationship("Category", back_populates="questions")
    tags = relationship("Tag", secondary=question_tags, back_populates="questions")
    card_state = relationship("CardState", back_populates="question", uselist=False)
    review_logs = relationship("ReviewLog", back_populates="question")
    error_records = relationship("ErrorRecord", back_populates="question")
