import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

async def main():
    await connect_to_mongo()
    user = await UserRepository.get_by_email("admin@example.com")
    print("role:", user.role, type(user.role))
    print("token:", AuthService.create_access_token(user.id, user.role))
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
