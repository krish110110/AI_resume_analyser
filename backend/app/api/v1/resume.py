from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
import os
import uuid
from typing import Optional
from app.api.dependencies import get_current_active_user
from app.services.resume_service import ResumeService

router = APIRouter()


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    analysis_type: str = Form("full"),
    current_user: dict = Depends(get_current_active_user),
):
    ext = ResumeService.validate_file(file)
    os.makedirs("storage/uploads/resumes", exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = f"storage/uploads/resumes/{filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    resume = await ResumeService.create_resume(
        user_id=current_user["user_id"],
        filename=file.filename,
        file_path=file_path,
        file_type=ext,
        file_size=os.path.getsize(file_path),
    )
    resume, analysis, report = await ResumeService.process_resume(resume.id, job_description)
    return {"id": resume.id, "report_id": report.id, "status": resume.status}


@router.get("/")
async def list_resumes(current_user: dict = Depends(get_current_active_user)):
    resumes = await ResumeService.list_resumes(current_user["user_id"])
    return [{"id": r.id, "filename": r.filename, "status": r.status, "ats_score": r.ats_score, "created_at": r.created_at.isoformat()} for r in resumes]


@router.get("/{resume_id}")
async def get_resume(resume_id: str, current_user: dict = Depends(get_current_active_user)):
    resume = await ResumeService.get_resume(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"id": resume.id, "filename": resume.filename, "status": resume.status, "ats_score": resume.ats_score}


@router.delete("/{resume_id}")
async def delete_resume(resume_id: str, current_user: dict = Depends(get_current_active_user)):
    await ResumeService.delete_resume(resume_id)
    return {"message": "Deleted"}
