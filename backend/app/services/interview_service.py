from typing import List, Optional

from app.models.interview_question import InterviewQuestion
from app.core.skill_catalog import SKILL_CATALOG, normalize_skill

# How many questions to surface per skill on the analytics page.
QUESTIONS_PER_SKILL = 2
# Cap the number of skills that get questions so the page stays usable.
MAX_SKILLS = 12


class InterviewService:
    @staticmethod
    def _resolve_skills(skills: List[str], limit: int = MAX_SKILLS) -> List[str]:
        """Map extracted skills onto canonical catalog skills, preserving order."""
        resolved = []
        seen = set()
        for skill in skills or []:
            canonical = normalize_skill(skill)
            if canonical and canonical in SKILL_CATALOG and canonical not in seen:
                seen.add(canonical)
                resolved.append(canonical)
            if len(resolved) >= limit:
                break
        return resolved

    @staticmethod
    async def generate_for_skills(
        skills: List[str],
        per_skill: int = QUESTIONS_PER_SKILL,
        max_skills: int = MAX_SKILLS,
    ) -> List[dict]:
        """Build grouped interview questions for the skills found in a resume."""
        resolved = InterviewService._resolve_skills(skills, max_skills)
        if not resolved:
            return []
        return await InterviewQuestion.get_for_skills(resolved, per_skill=per_skill)

    @staticmethod
    async def generate_for_resume(resume_id: str, per_skill: int = QUESTIONS_PER_SKILL) -> dict:
        """Build interview questions for an already analyzed resume."""
        from app.core.database import get_database

        db = get_database()
        report = await db["reports"].find_one({"resume_id": resume_id})
        if not report:
            return {"skills": [], "questions": [], "total_questions": 0}

        skills = report.get("skills") or (report.get("features") or {}).get("skills") or []
        questions = await InterviewService.generate_for_skills(skills, per_skill=per_skill)
        return {
            "resume_id": resume_id,
            "skills": [q["skill"] for q in questions],
            "questions": questions,
            "total_questions": sum(len(q["questions"]) for q in questions),
        }

    @staticmethod
    async def get_for_skills(skills: List[str], per_skill: int = QUESTIONS_PER_SKILL) -> dict:
        questions = await InterviewService.generate_for_skills(skills, per_skill=per_skill)
        return {
            "skills": [q["skill"] for q in questions],
            "questions": questions,
            "total_questions": sum(len(q["questions"]) for q in questions),
        }
