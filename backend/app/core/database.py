from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from app.core.config import settings
from typing import Optional


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    sync_client: Optional[MongoClient] = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Create database connection"""
    mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongodb.sync_client = MongoClient(settings.MONGODB_URL)
    print("Connected to MongoDB")


async def close_mongo_connection():
    """Close database connection"""
    if mongodb.client:
        mongodb.client.close()
    if mongodb.sync_client:
        mongodb.sync_client.close()


def get_database():
    """Get MongoDB database instance"""
    if mongodb.client is None:
        mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
        mongodb.sync_client = MongoClient(settings.MONGODB_URL)
    return mongodb.client[settings.MONGODB_DB_NAME]


def get_sync_database():
    """Get synchronous MongoDB database instance"""
    if mongodb.sync_client is None:
        mongodb.sync_client = MongoClient(settings.MONGODB_URL)
    return mongodb.sync_client[settings.MONGODB_DB_NAME]


# For backward compatibility with existing code
def get_db():
    """Dependency for getting database (async)"""
    return get_database()
