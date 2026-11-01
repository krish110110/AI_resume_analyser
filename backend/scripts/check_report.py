import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection, get_database
from bson import ObjectId

async def main():
    await connect_to_mongo()
    db = get_database()
    
    report_id = "6a81aebd5a245f16f717ba8d"
    doc = await db["reports"].find_one({"_id": ObjectId(report_id)})
    print("Report doc:", doc)
    
    if doc:
        print("User ID:", doc.get("user_id"))
        print("Resume ID:", doc.get("resume_id"))
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
