class SkillMatcher:
    async def calculate_match_percentage(self, skills: list[str], job_skills: list[str]) -> float:
        if not job_skills:
            return 0.0
        matches = len(set(skills) & set(job_skills))
        return round((matches / len(job_skills)) * 100, 1)
