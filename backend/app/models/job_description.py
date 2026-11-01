from datetime import datetime
from app.core.database import get_database


class JobDescription:
    collection_name = "job_descriptions"

    def __init__(self, **kwargs):
        _id = kwargs.get("_id")
        self.id = str(_id) if _id else None
        self.title = kwargs.get("title")
        self.company = kwargs.get("company")
        self.description = kwargs.get("description")
        self.created_at = kwargs.get("created_at", datetime.utcnow())
        self.updated_at = kwargs.get("updated_at", datetime.utcnow())

    def to_dict(self):
        return {
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    async def get_by_id(cls, job_id: str):
        from bson import ObjectId
        db = get_database()
        doc = await db[cls.collection_name].find_one({"_id": ObjectId(job_id)})
        return cls(**doc) if doc else None

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
