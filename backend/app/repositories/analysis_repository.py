from app.models.analysis import Analysis


class AnalysisRepository:
    @staticmethod
    async def get_by_id(analysis_id: str) -> Analysis | None:
        return await Analysis.get_by_id(analysis_id)

    @staticmethod
    async def list_by_resume(resume_id: str):
        return await Analysis.list_by_resume(resume_id)

    @staticmethod
    async def create(**kwargs) -> Analysis:
        return await Analysis.create(**kwargs)
