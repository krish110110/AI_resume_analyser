import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection, get_database
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password

async def main():
    await connect_to_mongo()
    user = await UserRepository.get_by_email("admin@example.com")
    if not user:
        print("User not found")
        await close_mongo_connection()
        return
    print(f"Found user: {user.email}")
    print(f"Hashed password: {user.hashed_password[:50]}...")
    ok = verify_password("admin123", user.hashed_password)
    print(f"Password matches: {ok}")
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
