from __future__ import annotations

import re
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.question_service import create_question
from src.schemas import QuestionCreate

_TAG_RE = re.compile(r"(?<!\w)#(\w+)")


def clean_title(raw: str) -> tuple[str, list[str]]:
    """清洗标题：去 # 前缀、去编号、提标签。返回 (标题, 标签列表)。"""
    title = raw.strip()

    # 去掉 # / ## 前缀
    title = re.sub(r"^#{1,2}\s*", "", title)

    # 去掉编号：从前往后找 . 或 、，在合理范围内就截断
    for ch in (".", "、"):
        pos = title.find(ch)
        if 0 < pos <= 10:
            title = title[pos + 1:].strip()
            break

    # 提取内联标签 #tag
    tags = _TAG_RE.findall(title)
    title = re.sub(r"\s*#\w+", "", title).strip()

    return title, tags


def split_content_answer(remaining: str) -> tuple[str, str]:
    """将题目正文按「答案:」分隔符拆分为 content 和 answer。"""
    remaining = remaining.strip()
    answer_marker = re.search(r"^答案[:：]\s*$", remaining, re.MULTILINE)

    if answer_marker:
        content = remaining[: answer_marker.start()].strip()
        answer = remaining[answer_marker.end() :].strip()
    else:
        content = ""
        answer = remaining

    return content, answer


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
        title, tags = clean_title(lines[0])

        if not title:
            continue

        content, answer = split_content_answer("\n".join(lines[1:]))

        # 跳过标题和内容都为空的条目
        if not content and not answer:
            continue

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
