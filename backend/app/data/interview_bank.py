"""Aggregated interview question bank across every question module."""

from app.data.questions_programming import QUESTIONS as PROGRAMMING_QUESTIONS
from app.data.questions_web_backend import QUESTIONS as WEB_BACKEND_QUESTIONS
from app.data.questions_data_ai import QUESTIONS as DATA_AI_QUESTIONS
from app.data.questions_devops import QUESTIONS as DEVOPS_QUESTIONS

from app.core.skill_catalog import SKILL_CATALOG

_QUESTION_MODULES = (
    PROGRAMMING_QUESTIONS,
    WEB_BACKEND_QUESTIONS,
    DATA_AI_QUESTIONS,
    DEVOPS_QUESTIONS,
)


def all_questions() -> dict:
    """Return the full question bank keyed by canonical skill name."""
    bank = {}
    for module in _QUESTION_MODULES:
        for skill, questions in module.items():
            bank[skill] = questions
    return bank


def question_records() -> list:
    """Flatten the question bank into seedable documents."""
    records = []
    for skill, questions in all_questions().items():
        category = SKILL_CATALOG.get(skill, "Other")
        for difficulty, question, answer in questions:
            records.append(
                {
                    "skill": skill,
                    "category": category,
                    "question": question,
                    "answer": answer,
                    "difficulty": difficulty,
                }
            )
    return records
