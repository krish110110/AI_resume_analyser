from app.models.user import User
from app.core.constants import UserRole
from app.core.database import get_database


class UserRepository:
    @staticmethod
    async def get_by_email(email: str) -> User | None:
        return await User.get_by_email(email)

    @staticmethod
    async def get_by_id(user_id: str) -> User | None:
        return await User.get_by_id(user_id)

    @staticmethod
    async def create(name: str, email: str, hashed_password: str, role: UserRole = UserRole.USER) -> User:
        return await User.create(name=name, email=email, hashed_password=hashed_password, role=role)

    @staticmethod
    async def update(user: User, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
        await user.save()

    @staticmethod
    async def delete(user_id: str) -> None:
        from bson import ObjectId
        from app.core.database import get_database
        await get_database()[User.collection_name].delete_one({"_id": ObjectId(user_id)})

    @staticmethod
    async def list_all(limit: int = 100):
        db = get_database()
        cursor = db[User.collection_name].find().sort("created_at", -1).limit(limit)
        return [User(**doc) async for doc in cursor]
