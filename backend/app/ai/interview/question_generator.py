from typing import List, Optional

from app.ai.extraction.skill_extractor import SkillExtractor


class QuestionGenerator:
    """Generates interview questions from the skills found in a resume.

    Questions come from the database-backed question bank, so no fixed or
    placeholder questions are ever returned.
    """

    async def generate(
        self,
        resume_text: str,
        job_description: Optional[str] = None,
        per_skill: int = 2,
    ) -> List[dict]:
        from app.services.interview_service import InterviewService

        skills = await SkillExtractor().extract(resume_text)
        if job_description:
            job_skills = await SkillExtractor().extract(job_description)
            known = set(skills)
            for skill in job_skills:
                if skill not in known:
                    skills.append(skill)
                    known.add(skill)

        return await InterviewService.generate_for_skills(skills, per_skill=per_skill)