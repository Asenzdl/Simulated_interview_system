import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.import_service import parse_markdown, import_questions
from src.models import Category


SAMPLE_MD = """\
## 什么是闭包？

请解释 JavaScript 闭包的概念

答案:
闭包是函数和其词法环境的组合，可以访问外部函数的变量。

---

## Promise 和 async/await 的区别？

答案:
Promise 是异步编程的一种方案，async/await 是其语法糖。

---

## 简述 HTTP 缓存机制

答案:
包括强缓存和协商缓存两种机制。
"""


def test_parse_markdown_count():
    questions = parse_markdown(SAMPLE_MD)
    assert len(questions) == 3


def test_parse_markdown_first_question():
    questions = parse_markdown(SAMPLE_MD)
    q = questions[0]
    assert q["title"] == "什么是闭包？"
    assert "JavaScript 闭包" in q["content"]
    assert "词法环境" in q["answer"]


def test_parse_markdown_no_content():
    questions = parse_markdown(SAMPLE_MD)
    q = questions[1]
    assert q["title"] == "Promise 和 async/await 的区别？"
    assert q["content"] == ""
    assert "语法糖" in q["answer"]


def test_parse_markdown_empty():
    assert parse_markdown("") == []
    assert parse_markdown("   ") == []


def test_parse_markdown_no_separator():
    md = "## 单个问题\n\n答案:\n答案内容"
    questions = parse_markdown(md)
    assert len(questions) == 1


async def test_import_questions(db_session: AsyncSession, sample_category):
    result = await import_questions(db_session, SAMPLE_MD, category_id=sample_category.id, difficulty=3)
    assert result["imported"] == 3
    assert result["skipped"] == 0

    from src.services.question_service import list_questions
    list_result = await list_questions(db_session)
    assert list_result.total == 3
    for q in list_result.items:
        assert q.category_id == sample_category.id
        assert q.difficulty == 3


async def test_import_questions_default_category(db_session: AsyncSession):
    result = await import_questions(db_session, "## 测试\n\n答案:\n答案")
    assert result["imported"] == 1
    assert result["skipped"] == 0


def test_parse_with_tags():
    md = "## 带标签的题目 #js #闭包\n\n答案:\n答案"
    questions = parse_markdown(md)
    assert questions[0]["tags"] == ["js", "闭包"]
    assert questions[0]["title"] == "带标签的题目"
