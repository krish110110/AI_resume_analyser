from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    @staticmethod
    async def get_profile(user_id: str):
        return await UserRepository.get_by_id(user_id)

    @staticmethod
    async def update_profile(user_id: str, payload: UserUpdate):
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if payload.name is not None:
            user.name = payload.name
        if payload.new_password:
            if not payload.current_password:
                raise ValueError("Current password is required")
            from app.core.security import verify_password
            if not verify_password(payload.current_password, user.hashed_password):
                raise ValueError("Current password is incorrect")
            from app.core.security import get_password_hash
            user.hashed_password = get_password_hash(payload.new_password)
        await user.save()
        return user
