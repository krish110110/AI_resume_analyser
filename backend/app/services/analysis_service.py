from app.repositories.analysis_repository import AnalysisRepository


class AnalysisService:
    @staticmethod
    async def get_analysis(analysis_id: str):
        return await AnalysisRepository.get_by_id(analysis_id)

    @staticmethod
    async def list_analyses_by_resume(resume_id: str):
        return await AnalysisRepository.list_by_resume(resume_id)
