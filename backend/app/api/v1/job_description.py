from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_active_user
from app.schemas.job_description import JobDescriptionCreate, JobDescriptionOut
from app.services.job_service import JobService

router = APIRouter()


@router.post("/", response_model=JobDescriptionOut)
async def create_job(payload: JobDescriptionCreate, current_user: dict = Depends(get_current_active_user)):
    job = await JobService.create_job(payload.title, payload.company, payload.description)
    return JobDescriptionOut(id=job.id, title=job.title, company=job.company, description=job.description, created_at=job.created_at.isoformat())


@router.get("/")
async def list_jobs(current_user: dict = Depends(get_current_active_user)):
    jobs = await JobService.list_jobs()
    return [{"id": j.id, "title": j.title, "company": j.company, "created_at": j.created_at.isoformat()} for j in jobs]


@router.get("/{job_id}")
async def get_job(job_id: str, current_user: dict = Depends(get_current_active_user)):
    job = await JobService.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"id": job.id, "title": job.title, "company": job.company, "description": job.description}
