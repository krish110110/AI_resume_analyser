import sys
import asyncio
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.database import connect_to_mongo, close_mongo_connection, get_database


async def main():
    await connect_to_mongo()
    db = get_database()
    await db["skills"].insert_many([
        {"name": "python", "category": "language"},
        {"name": "java", "category": "language"},
        {"name": "javascript", "category": "language"},
        {"name": "react", "category": "framework"},
        {"name": "node.js", "category": "framework"},
        {"name": "sql", "category": "database"},
        {"name": "aws", "category": "cloud"},
        {"name": "docker", "category": "devops"},
        {"name": "machine learning", "category": "ai"},
        {"name": "data analysis", "category": "ai"},
    ])
    print("Skills seeded")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
