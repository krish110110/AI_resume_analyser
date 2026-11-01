import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection, get_database

async def main():
    await connect_to_mongo()
    db = get_database()
    cursor = db["users"].find()
    users = await cursor.to_list(length=20)
    print("Users in DB:")
    for u in users:
        print(u)
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
