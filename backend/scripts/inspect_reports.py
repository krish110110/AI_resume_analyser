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
    print("Reports in DB:")
    for r in reports:
        print("---")
        print("ID:", r.get("_id"))
        print("user_id:", r.get("user_id"))
        print("resume_id:", r.get("resume_id"))
        print("filename:", r.get("filename"))
        print("ats_score:", r.get("ats_score"))
        print("similarity_score:", r.get("similarity_score"))
        print("skill_match_percentage:", r.get("skill_match_percentage"))
        print("skills:", r.get("skills"))
        print("missing_keywords:", r.get("missing_keywords"))
        print("recommendations:", r.get("recommendations"))
        print("classification:", r.get("classification"))
        print("scores:", r.get("scores"))
        print("features:", r.get("features"))
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
