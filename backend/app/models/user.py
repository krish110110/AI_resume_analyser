from datetime import datetime
from app.core.database import get_database
from app.core.constants import UserRole


class User:
    collection_name = "users"

    def __init__(self, **kwargs):
        _id = kwargs.get("_id")
        self.id = str(_id) if _id else None
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.hashed_password = kwargs.get("hashed_password")
        role = kwargs.get("role", UserRole.USER)
        if isinstance(role, str):
            role = UserRole(role)
        self.role = role
        self.is_active = kwargs.get("is_active", True)
        self.created_at = kwargs.get("created_at", datetime.utcnow())
        self.updated_at = kwargs.get("updated_at", datetime.utcnow())

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "role": self.role.value if isinstance(self.role, UserRole) else self.role,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    async def get_by_email(cls, email: str):
        db = get_database()
        doc = await db[cls.collection_name].find_one({"email": email})
        return cls(**doc) if doc else None

    @classmethod
    async def get_by_id(cls, user_id: str):
        from bson import ObjectId
        db = get_database()
        doc = await db[cls.collection_name].find_one({"_id": ObjectId(user_id)})
        return cls(**doc) if doc else None

    @classmethod
    async def create(cls, **kwargs):
        db = get_database()
        result = await db[cls.collection_name].insert_one(kwargs)
        kwargs["_id"] = result.inserted_id
        return cls(**kwargs)

    async def save(self):
        from bson import ObjectId
        db = get_database()
        self.updated_at = datetime.utcnow()
        await db[self.collection_name].update_one({"_id": ObjectId(self.id)}, {"$set": self.to_dict()})
