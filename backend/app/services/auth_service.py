from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.constants import UserRole


class AuthService:
    @staticmethod
    def create_access_token(user_id: str, role: UserRole) -> str:
        payload = {"sub": user_id, "role": role.value}
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        payload.update({"exp": expire})
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    def create_refresh_token(user_id: str, role: UserRole) -> str:
        payload = {"sub": user_id, "role": role.value, "type": "refresh"}
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        payload.update({"exp": expire})
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    async def authenticate(email: str, password: str):
        user = await UserRepository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def register(name: str, email: str, password: str) -> User:
        existing = await UserRepository.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        hashed = get_password_hash(password)
        return await UserRepository.create(name=name, email=email, hashed_password=hashed, role=UserRole.USER)
