from fastapi import APIRouter
from app.api.v1 import auth, users, admin, resume, job_description, analysis, reports, dashboard, health, interview

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(resume.router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(job_description.router, prefix="/jobs", tags=["Job Descriptions"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(interview.router, prefix="/interview-questions", tags=["Interview Questions"])
api_router.include_router(health.router, tags=["Health"])
