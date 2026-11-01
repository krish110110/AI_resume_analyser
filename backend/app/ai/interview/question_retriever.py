from typing import List

from app.services.interview_service import InterviewService


class QuestionRetriever:
    """Retrieves database-backed interview questions for resume skills."""

    async def retrieve(self, skills: List[str], per_skill: int = 2) -> List[dict]:
        return await InterviewService.generate_for_skills(skills, per_skill=per_skill)
