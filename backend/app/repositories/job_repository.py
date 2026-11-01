from app.models.job_description import JobDescription


class JobRepository:
    @staticmethod
    async def get_by_id(job_id: str) -> JobDescription | None:
        return await JobDescription.get_by_id(job_id)

    @staticmethod
    async def list_all(limit: int = 100):
        return await JobDescription.list_all(limit)

    @staticmethod
    async def create(**kwargs) -> JobDescription:
        return await JobDescription.create(**kwargs)
