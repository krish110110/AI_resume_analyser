from datetime import datetime
from app.core.database import get_database


class Report:
    collection_name = "reports"

    def __init__(self, **kwargs):
        _id = kwargs.get("_id")
        self.id = str(_id) if _id else None
        self.user_id = kwargs.get("user_id")
        self.resume_id = kwargs.get("resume_id")
        self.analysis_id = kwargs.get("analysis_id")
        self.filename = kwargs.get("filename")
        self.ats_score = kwargs.get("ats_score")
        self.similarity_score = kwargs.get("similarity_score")
        self.skill_match_percentage = kwargs.get("skill_match_percentage")
        self.skills = kwargs.get("skills", [])
        self.missing_keywords = kwargs.get("missing_keywords", [])
        self.recommendations = kwargs.get("recommendations", [])
        self.parsed_data = kwargs.get("parsed_data", {})
        self.features = kwargs.get("features", {})
        self.classification = kwargs.get("classification", {})
        self.scores = kwargs.get("scores", {})
        self.interview_questions = kwargs.get("interview_questions", [])
        self.created_at = kwargs.get("created_at", datetime.utcnow())

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "resume_id": self.resume_id,
            "analysis_id": self.analysis_id,
            "filename": self.filename,
            "ats_score": self.ats_score,
            "similarity_score": self.similarity_score,
            "skill_match_percentage": self.skill_match_percentage,
            "skills": self.skills,
            "missing_keywords": self.missing_keywords,
            "recommendations": self.recommendations,
            "parsed_data": self.parsed_data,
            "features": self.features,
            "classification": self.classification,
            "scores": self.scores,
            "interview_questions": self.interview_questions,
            "created_at": self.created_at,
        }

    @classmethod
    async def get_by_id(cls, report_id: str):
        from bson import ObjectId
        db = get_database()
        doc = await db[cls.collection_name].find_one({"_id": ObjectId(report_id)})
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
        result = await db[cls.collection_name].insert_one(kwargs)
        kwargs["_id"] = result.inserted_id
        return cls(**kwargs)

    async def save(self):
        from bson import ObjectId
        db = get_database()
        self.updated_at = datetime.utcnow()
        await db[self.collection_name].update_one({"_id": ObjectId(self.id)}, {"$set": self.to_dict()})
