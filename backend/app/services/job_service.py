from typing import Optional
from app.repositories.job_repository import JobRepository


class JobService:
    @staticmethod
    async def create_job(title: str, company: Optional[str], description: str):
        return await JobRepository.create(title=title, company=company, description=description)

    @staticmethod
    async def list_jobs(limit: int = 100):
        return await JobRepository.list_all(limit)

    @staticmethod
    async def get_job(job_id: str):
        return await JobRepository.get_by_id(job_id)
