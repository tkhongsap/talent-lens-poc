from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import get_settings

settings = get_settings()


class MongoDB:
    client: AsyncIOMotorClient = None
    db = None


db = MongoDB()


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(
        settings.DATABASE_URL,
        maxPoolSize=settings.MONGODB_MAX_CONNECTIONS,
        minPoolSize=settings.MONGODB_MIN_CONNECTIONS
    )
    db.db = db.client.talent_lens


async def close_mongo_connection():
    if db.client:
        db.client.close()


# Database collections
def get_collection(collection_name: str):
    return db.db[collection_name]


# Collection names
USERS_COLLECTION = "users"
RESUMES_COLLECTION = "resumes"
JOBS_COLLECTION = "jobs"
ANALYTICS_COLLECTION = "analytics" 