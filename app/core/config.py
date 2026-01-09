import os
from dotenv  import load_dotenv

load_dotenv()

FAST_API_BASE_URL = os.getenv("FAST_API_BASE_URL", "http://localhost:8000")

MONGO_DB_URI = os.getenv("MONGO_DB_URI", "localhost:27017")
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME", "")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD", "")
MONGO_DB_DATABASE = os.getenv("MONGO_DB_DATABASE", "fastapi_api_hub_db")
if MONGO_DB_USERNAME and MONGO_DB_PASSWORD:
    MONGO_DB_DETAILS = f"mongodb://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@{MONGO_DB_URI}"
else:
    MONGO_DB_DETAILS = f"mongodb://{MONGO_DB_URI}"