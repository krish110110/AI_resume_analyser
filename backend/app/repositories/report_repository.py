from app.models.report import Report
from app.core.database import get_database


class ReportRepository:
    @staticmethod
    async def get_by_id(report_id: str) -> Report | None:
        return await Report.get_by_id(report_id)

    @staticmethod
    async def get_by_resume_id(resume_id: str) -> Report | None:
        db = get_database()
        doc = await db[Report.collection_name].find_one({"resume_id": resume_id})
        return Report(**doc) if doc else None

    @staticmethod
    async def list_by_user(user_id: str, limit: int = 50):
        return await Report.list_by_user(user_id, limit)

    @staticmethod
    async def list_all(limit: int = 100):
        return await Report.list_all(limit)

    @staticmethod
    async def create(**kwargs) -> Report:
        return await Report.create(**kwargs)
