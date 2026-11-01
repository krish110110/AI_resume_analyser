from app.models.resume import Resume


class ResumeRepository:
    @staticmethod
    async def get_by_id(resume_id: str) -> Resume | None:
        return await Resume.get_by_id(resume_id)

    @staticmethod
    async def list_by_user(user_id: str, limit: int = 50):
        return await Resume.list_by_user(user_id, limit)

    @staticmethod
    async def list_all(limit: int = 100):
        return await Resume.list_all(limit)

    @staticmethod
    async def create(**kwargs) -> Resume:
        return await Resume.create(**kwargs)

    @staticmethod
    async def update(resume: Resume, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(resume, k):
                setattr(resume, k, v)
        await resume.save()

    @staticmethod
    async def delete(resume_id: str) -> None:
        from bson import ObjectId
        from app.core.database import get_database
        await get_database()[Resume.collection_name].delete_one({"_id": ObjectId(resume_id)})
