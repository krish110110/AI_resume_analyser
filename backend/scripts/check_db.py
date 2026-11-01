import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection, get_database

async def main():
    await connect_to_mongo()
    db = get_database()
    collections = await db.list_collection_names()
    print("Collections:", collections)
    for name in collections:
        count = await db[name].count_documents({})
        print(f"  {name}: {count} documents")
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(main())
