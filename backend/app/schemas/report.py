from typing import Optional
from pydantic import BaseModel


class ReportOut(BaseModel):
    id: str
    resume_id: str
    analysis_id: str
    filename: str
    ats_score: Optional[float]
    similarity_score: Optional[float]
    skill_match_percentage: Optional[float]
    skills: list[str]
    missing_keywords: list[str]
    recommendations: list[str]
    created_at: str

    model_config = {"from_attributes": True}
