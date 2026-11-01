from datetime import datetime
from typing import List, Optional

from app.core.database import get_database
from app.data.interview_bank import question_records
from app.core.skill_catalog import SKILL_CATALOG

DIFFICULTY_ORDER = {"hard": 0, "medium": 1, "easy": 2}


class InterviewQuestion:
    collection_name = "interview_questions"

    def __init__(self, **kwargs):
        _id = kwargs.get("_id")
        self.id = str(_id) if _id else None
        self.skill = kwargs.get("skill")
        self.category = kwargs.get("category")
        self.question = kwargs.get("question")
        self.answer = kwargs.get("answer")
        self.difficulty = kwargs.get("difficulty", "medium")
        self.created_at = kwargs.get("created_at", datetime.utcnow())

    def to_dict(self):
        return {
            "skill": self.skill,
            "category": self.category,
            "question": self.question,
            "answer": self.answer,
            "difficulty": self.difficulty,
            "created_at": self.created_at,
        }

    @staticmethod
    async def count() -> int:
        db = get_database()
        return await db[InterviewQuestion.collection_name].count_documents({})

    @staticmethod
    async def seed(force: bool = False) -> int:
        """Insert the question bank into MongoDB if it is not already present.

        Returns the number of questions inserted.
        """
        db = get_database()
        collection = db[InterviewQuestion.collection_name]

        existing = await collection.count_documents({})
        records = question_records()
        if existing >= len(records) and not force:
            return 0

        if force:
            await collection.delete_many({})
        else:
            # Only insert questions that are missing, keyed by skill + question.
            seen = set()
            async for doc in collection.find({}, {"skill": 1, "question": 1}):
                seen.add((doc.get("skill"), doc.get("question")))

        pending = [
            record
            for record in records
            if (record["skill"], record["question"]) not in seen
        ]
        if not pending:
            return 0

        for record in pending:
            record["created_at"] = datetime.utcnow()

        await collection.insert_many(pending)
        await collection.create_index([("skill", 1)])
        await collection.create_index([("difficulty", 1)])
        return len(pending)

    @classmethod
    async def get_for_skills(cls, skills: List[str], per_skill: int = 2) -> List[dict]:
        """Return interview questions for the given skills.

        Each skill contributes at most ``per_skill`` questions, and at least one
        hard question is included per skill when the bank has one, so the
        analytics page always surfaces the harder material.
        """
        if not skills:
            return []

        db = get_database()
        cursor = db[cls.collection_name].find({"skill": {"$in": list(skills)}})
        docs = [cls(**doc) async for doc in cursor]

        grouped = {}
        for doc in docs:
            grouped.setdefault(doc.skill, []).append(doc)

        results = []
        for skill in skills:
            skill_questions = grouped.get(skill)
            if not skill_questions:
                continue
            selected = cls._select_questions(skill_questions, per_skill)
            results.append(
                {
                    "skill": skill,
                    "category": SKILL_CATALOG.get(skill, "Other"),
                    "questions": [q.to_dict() for q in selected],
                }
            )
        return results

    @staticmethod
    def _select_questions(questions: List["InterviewQuestion"], per_skill: int) -> List["InterviewQuestion"]:
        """Pick per_skill questions, guaranteeing one hard question is included."""
        if len(questions) <= per_skill:
            return sorted(questions, key=lambda q: DIFFICULTY_ORDER.get(q.difficulty, 3))

        hard = [q for q in questions if q.difficulty == "hard"]
        others = [q for q in questions if q.difficulty != "hard"]

        selected = []
        if hard:
            selected.append(hard[0])

        remaining_slots = per_skill - len(selected)
        if remaining_slots > 0:
            # Fill the rest with the hardest remaining questions available.
            pool = hard[1:] + others
            pool.sort(key=lambda q: DIFFICULTY_ORDER.get(q.difficulty, 3))
            selected.extend(pool[:remaining_slots])

        return selected

    @classmethod
    async def list_by_skill(cls, skill: str) -> List[dict]:
        db = get_database()
        cursor = db[cls.collection_name].find({"skill": skill})
        questions = [cls(**doc) async for doc in cursor]
        questions.sort(key=lambda q: DIFFICULTY_ORDER.get(q.difficulty, 3))
        return [q.to_dict() for q in questions]

    @classmethod
    async def list_all(cls, limit: int = 1000) -> List[dict]:
        db = get_database()
        cursor = db[cls.collection_name].find({}).limit(limit)
        return [cls(**doc).to_dict() async for doc in cursor]

    @classmethod
    async def skills_covered(cls) -> List[str]:
        db = get_database()
        return await db[cls.collection_name].distinct("skill")

    @classmethod
    async def stats(cls) -> dict:
        db = get_database()
        collection = db[cls.collection_name]
        total = await collection.count_documents({})
        by_difficulty = {}
        for difficulty in ("easy", "medium", "hard"):
            by_difficulty[difficulty] = await collection.count_documents({"difficulty": difficulty})
        return {
            "total_questions": total,
            "skills_covered": len(await cls.skills_covered()),
            "by_difficulty": by_difficulty,
        }
