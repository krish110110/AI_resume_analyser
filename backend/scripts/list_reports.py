import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection, get_database

async def main():
    await connect_to_mongo()
    db = get_database()
    cursor = db["reports"].find().sort("created_at", -1)
    reports = await cursor.to_list(length=10)
    print("All reports:")
    for r in reports:
        print("ID:", r.get("_id"), "| user_id:", r.get("user_id"), "| resume_id:", r.get("resume_id"), "| filename:", r.get("filename"))
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
