import os
from dotenv  import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "fastapi_api_hub_db")

#client = AsyncIOMotorClient(MONGO_DETAILS)
#database = client[MONGO_DB_NAME]
#user_collection = database.get_collection("users")

client: AsyncIOMotorClient | None = None

async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGO_DETAILS)

async def close_mongo_connection():
    client.close()

def get_database():
    if client is None:
        raise RuntimeError("MongoDB not connected")
    return client[MONGO_DB_NAME]