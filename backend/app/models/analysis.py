from datetime import datetime
from app.core.database import get_database


class Analysis:
    collection_name = "analyses"

    def __init__(self, **kwargs):
        _id = kwargs.get("_id")
        self.id = str(_id) if _id else None
        self.resume_id = kwargs.get("resume_id")
        self.job_description_id = kwargs.get("job_description_id")
        self.parsed_data = kwargs.get("parsed_data", {})
        self.features = kwargs.get("features", {})
        self.classification = kwargs.get("classification", {})
        self.scores = kwargs.get("scores", {})
        self.recommendations = kwargs.get("recommendations", [])
        self.interview_questions = kwargs.get("interview_questions", [])
        self.created_at = kwargs.get("created_at", datetime.utcnow())

    def to_dict(self):
        return {
            "resume_id": self.resume_id,
            "job_description_id": self.job_description_id,
            "parsed_data": self.parsed_data,
            "features": self.features,
            "classification": self.classification,
            "scores": self.scores,
            "recommendations": self.recommendations,
            "interview_questions": self.interview_questions,
            "created_at": self.created_at,
        }

    @classmethod
    async def get_by_id(cls, analysis_id: str):
        from bson import ObjectId
        db = get_database()
        doc = await db[cls.collection_name].find_one({"_id": ObjectId(analysis_id)})
        return cls(**doc) if doc else None

    @classmethod
    async def list_by_resume(cls, resume_id: str):
        db = get_database()
        cursor = db[cls.collection_name].find({"resume_id": resume_id}).sort("created_at", -1)
        return [cls(**doc) async for doc in cursor]

    @classmethod
    async def create(cls, **kwargs):
        db = get_database()
        kwargs["created_at"] = kwargs.get("created_at", datetime.utcnow())
        result = await db[cls.collection_name].insert_one(kwargs)
        kwargs["_id"] = result.inserted_id
        return cls(**kwargs)

    async def save(self):
        from bson import ObjectId
        db = get_database()
        self.updated_at = datetime.utcnow()
        await db[self.collection_name].update_one({"_id": ObjectId(self.id)}, {"$set": self.to_dict()})
