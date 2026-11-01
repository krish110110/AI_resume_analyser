from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_active_user
from app.services.report_service import ReportService

router = APIRouter()


@router.get("/")
async def list_reports(current_user: dict = Depends(get_current_active_user)):
    reports = await ReportService.list_reports(current_user["user_id"])
    return [{"id": r.id, "resume_id": r.resume_id, "filename": r.filename, "ats_score": r.ats_score, "created_at": r.created_at.isoformat()} for r in reports]


@router.get("/by-resume/{resume_id}")
async def get_report_by_resume(resume_id: str, current_user: dict = Depends(get_current_active_user)):
    report = await ReportService.get_by_resume_id(resume_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {
        "id": report.id,
        "filename": report.filename,
        "ats_score": report.ats_score,
        "similarity_score": report.similarity_score,
        "skill_match_percentage": report.skill_match_percentage,
        "skills": report.skills,
        "missing_keywords": report.missing_keywords,
        "recommendations": report.recommendations,
        "parsed_data": report.parsed_data,
        "features": report.features,
        "classification": report.classification,
        "scores": report.scores,
        "interview_questions": report.interview_questions,
        "created_at": report.created_at.isoformat(),
    }


@router.get("/{report_id}")
async def get_report(report_id: str, current_user: dict = Depends(get_current_active_user)):
    report = await ReportService.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {
        "id": report.id,
        "filename": report.filename,
        "ats_score": report.ats_score,
        "similarity_score": report.similarity_score,
        "skill_match_percentage": report.skill_match_percentage,
        "skills": report.skills,
        "missing_keywords": report.missing_keywords,
        "recommendations": report.recommendations,
        "parsed_data": report.parsed_data,
        "features": report.features,
        "classification": report.classification,
        "scores": report.scores,
        "interview_questions": report.interview_questions,
        "created_at": report.created_at.isoformat(),
    }
