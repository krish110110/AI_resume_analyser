class ScoreExplainer:
    async def generate_feedback(self, scores: dict, candidate_name: str = None) -> list[str]:
        """Build feedback messages, addressed to the candidate when a name is known."""
        name = (candidate_name or "").strip()
        address = f"{name}, " if name else ""

        feedback = []
        if scores.get("ats_score", 0) < 70:
            feedback.append(f"{address}improve ATS compatibility by adding more relevant keywords.")
        if scores.get("similarity_score", 0) < 60:
            feedback.append(f"{address}tailor your resume to better match the job description.")
        if scores.get("skill_match_percentage", 0) < 50:
            feedback.append(f"{address}add missing skills to improve job match.")
        if not feedback:
            if name:
                feedback.append(f"Great work, {name}. Your resume looks strong.")
            else:
                feedback.append("Great job! Your resume looks strong.")
        return feedback