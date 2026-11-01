class SuggestionGenerator:
    async def generate(self, scores: dict, features: dict) -> list[str]:
        suggestions = []
        if scores.get("ats_score", 0) < 70:
            suggestions.append("Use standard section headings like Experience, Education, Skills.")
        if scores.get("similarity_score", 0) < 60:
            suggestions.append("Mirror keywords from the job description in your resume.")
        if not suggestions:
            suggestions.append("Your resume is well optimized.")
        return suggestions
