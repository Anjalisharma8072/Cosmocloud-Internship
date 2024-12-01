from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class Database:
    client:AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_database(cls):
        cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
        cls.db = cls.client[settings.DATABASE_NAME]
        return cls.db
    
    @classmethod
    async def close_database(cls):
        if cls.client:
            cls.client.close()