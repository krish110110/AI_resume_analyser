from datetime import datetime
from app.core.database import get_database
from app.core.constants import ResumeStatus, FileType


class Resume:
    collection_name = "resumes"

    def __init__(self, **kwargs):
        _id = kwargs.get("_id")
        self.id = str(_id) if _id else None
        self.user_id = kwargs.get("user_id")
        self.filename = kwargs.get("filename")
        self.file_path = kwargs.get("file_path")
        self.file_type = kwargs.get("file_type")
        self.file_size = kwargs.get("file_size")
        self.status = kwargs.get("status", ResumeStatus.PENDING)
        self.ats_score = kwargs.get("ats_score")
        self.similarity_score = kwargs.get("similarity_score")
        self.skill_match_percentage = kwargs.get("skill_match_percentage")
        self.missing_keywords = kwargs.get("missing_keywords", [])
        self.raw_text = kwargs.get("raw_text", "")
        self.created_at = kwargs.get("created_at", datetime.utcnow())
        self.updated_at = kwargs.get("updated_at", datetime.utcnow())

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "filename": self.filename,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "status": self.status.value if isinstance(self.status, ResumeStatus) else self.status,
            "ats_score": self.ats_score,
            "similarity_score": self.similarity_score,
            "skill_match_percentage": self.skill_match_percentage,
            "missing_keywords": self.missing_keywords,
            "raw_text": self.raw_text,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    async def get_by_id(cls, resume_id: str):
        from bson import ObjectId
        db = get_database()
        doc = await db[cls.collection_name].find_one({"_id": ObjectId(resume_id)})
        return cls(**doc) if doc else None

    @classmethod
    async def list_by_user(cls, user_id: str, limit: int = 50):
        db = get_database()
        cursor = db[cls.collection_name].find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        return [cls(**doc) async for doc in cursor]

    @classmethod
    async def list_all(cls, limit: int = 100):
        db = get_database()
        cursor = db[cls.collection_name].find().sort("created_at", -1).limit(limit)
        return [cls(**doc) async for doc in cursor]

    @classmethod
    async def create(cls, **kwargs):
        db = get_database()
        kwargs["created_at"] = kwargs.get("created_at", datetime.utcnow())
        kwargs["updated_at"] = kwargs.get("updated_at", datetime.utcnow())
        result = await db[cls.collection_name].insert_one(kwargs)
        kwargs["_id"] = result.inserted_id
        return cls(**kwargs)

    async def save(self):
        from bson import ObjectId
        db = get_database()
        self.updated_at = datetime.utcnow()
        await db[self.collection_name].update_one({"_id": ObjectId(self.id)}, {"$set": self.to_dict()})
