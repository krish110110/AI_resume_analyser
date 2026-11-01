from app.repositories.report_repository import ReportRepository


class ReportService:
    @staticmethod
    async def get_report(report_id: str):
        return await ReportRepository.get_by_id(report_id)

    @staticmethod
    async def get_by_resume_id(resume_id: str):
        return await ReportRepository.get_by_resume_id(resume_id)

    @staticmethod
    async def list_reports(user_id: str, limit: int = 50):
        return await ReportRepository.list_by_user(user_id, limit)
