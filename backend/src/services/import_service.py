from __future__ import annotations

import re
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.question_service import create_question
from src.schemas import QuestionCreate


def parse_markdown(text: str) -> list[dict]:
    text = text.strip()
    if not text:
        return []

    blocks = re.split(r"\n---\n", text)
    questions = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split("\n")
        title_line = lines[0].strip()

        # 去掉 ## 前缀
        if title_line.startswith("## "):
            title_line = title_line[3:]
        elif title_line.startswith("##"):
            title_line = title_line[2:]
        title_line = title_line.strip()

        # 提取内联标签 #tag
        tags = re.findall(r"(?<!\w)#(\w+)", title_line)
        title = re.sub(r"\s*#\w+", "", title_line).strip()

        if not title:
            continue

        # 分割内容和答案
        remaining = "\n".join(lines[1:]).strip()
        answer_marker = re.search(r"^答案[:：]\s*$", remaining, re.MULTILINE)

        if answer_marker:
            content = remaining[: answer_marker.start()].strip()
            answer = remaining[answer_marker.end() :].strip()
        else:
            content = remaining
            answer = ""

        questions.append({
            "title": title,
            "content": content,
            "answer": answer,
            "tags": tags,
        })

    return questions


async def import_questions(
    db: AsyncSession,
    text: str,
    category_id: int | None = None,
    difficulty: int = 1,
) -> dict[str, int]:
    parsed = parse_markdown(text)
    imported = 0
    skipped = 0

    for item in parsed:
        data = QuestionCreate(
            title=item["title"],
            content=item["content"] or None,
            answer=item["answer"] or None,
            category_id=category_id,
            difficulty=difficulty,
            tags=item["tags"],
        )
        try:
            await create_question(db, data)
            imported += 1
        except ValueError:
            skipped += 1

    return {"imported": imported, "skipped": skipped}
