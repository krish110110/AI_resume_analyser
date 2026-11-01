from typing import Optional
from pydantic import BaseModel
from app.core.constants import ResumeStatus, AnalysisType, FileType


class ResumeUpload(BaseModel):
    analysis_type: AnalysisType = AnalysisType.FULL


class ResumeOut(BaseModel):
    id: str
    filename: str
    file_type: FileType
    status: ResumeStatus
    ats_score: Optional[float] = None
    similarity_score: Optional[float] = None
    skill_match_percentage: Optional[float] = None
    created_at: str
    user_id: str

    model_config = {"from_attributes": True}
