from app.repositories.user_repository import UserRepository
from app.repositories.resume_repository import ResumeRepository
from app.repositories.report_repository import ReportRepository
from app.core.database import get_database


class DashboardService:
    @staticmethod
    async def get_user_stats(user_id: str):
        resumes = await ResumeRepository.list_by_user(user_id)
        total = len(resumes)
        avg = sum(r.ats_score or 0 for r in resumes) / total if total else 0
        matches = sum(1 for r in resumes if (r.similarity_score or 0) > 0.5)
        return {"total_resumes": total, "avg_ats_score": round(avg, 1), "total_matches": matches}

    @staticmethod
    async def get_admin_stats():
        users = await UserRepository.list_all()
        reports = await ReportRepository.list_all()
        total_users = len(users)
        total_reports = len(reports)
        avg = sum(r.ats_score or 0 for r in reports) / total_reports if total_reports else 0
        return {
            "total_users": total_users,
            "total_reports": total_reports,
            "avg_ats_score": round(avg, 1),
            "system_health": "OK",
        }
