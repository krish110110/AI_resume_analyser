import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection
from app.repositories.user_repository import UserRepository
from app.core.constants import UserRole
from app.core.security import get_password_hash


async def main():
    await connect_to_mongo()
    existing = await UserRepository.get_by_email("admin@example.com")
    if existing:
        print("Admin already exists")
        await close_mongo_connection()
        return
    await UserRepository.create(
        name="Admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        role=UserRole.ADMIN,
    )
    print("Admin created")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
