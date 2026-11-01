from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_active_user
from app.services.analysis_service import AnalysisService
from app.schemas.analysis import AnalysisCreate

router = APIRouter()


@router.post("/")
async def create_analysis(payload: AnalysisCreate, current_user: dict = Depends(get_current_active_user)):
    analysis = await AnalysisService.get_analysis(payload.resume_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"id": analysis.id, "resume_id": analysis.resume_id, "scores": analysis.scores}


@router.get("/{analysis_id}")
async def get_analysis(analysis_id: str, current_user: dict = Depends(get_current_active_user)):
    analysis = await AnalysisService.get_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"id": analysis.id, "resume_id": analysis.resume_id, "scores": analysis.scores, "classification": analysis.classification}
