import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection, get_database


async def main():
    await connect_to_mongo()
    db = get_database()
    collections = await db.list_collection_names()
    for name in ["users", "resumes", "job_descriptions", "analyses", "reports"]:
        if name not in collections:
            await db.create_collection(name)
    print("Database initialized")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
