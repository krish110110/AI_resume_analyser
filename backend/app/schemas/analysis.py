from typing import Optional
from pydantic import BaseModel


class AnalysisCreate(BaseModel):
    resume_id: str
    job_description_id: Optional[str] = None


class AnalysisOut(BaseModel):
    id: str
    resume_id: str
    job_description_id: Optional[str]
    parsed_data: dict
    features: dict
    classification: dict
    scores: dict
    recommendations: list[str]
    created_at: str

    model_config = {"from_attributes": True}
