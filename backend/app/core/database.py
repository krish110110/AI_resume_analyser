from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


class MongoDB:
    client: AsyncIOMotorClient = None
    database = None


db = MongoDB()


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongo_url)
    db.database = db.client[settings.mongo_db_name]


async def close_mongo_connection():
    if db.client:
        db.client.close()


def get_database():
    return db.database
