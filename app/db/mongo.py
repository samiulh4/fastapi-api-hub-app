from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_DB_DETAILS, MONGO_DB_DATABASE

#client = AsyncIOMotorClient(MONGO_DB_DETAILS)
#database = client[MONGO_DB_DATABASE]
#user_collection = database.get_collection("users")

client: AsyncIOMotorClient | None = None

async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGO_DB_DETAILS)

async def close_mongo_connection():
    client.close()

def get_database():
    if client is None:
        raise RuntimeError("MongoDB not connected")
    return client[MONGO_DB_DATABASE]