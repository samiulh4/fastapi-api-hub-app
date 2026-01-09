from fastapi import FastAPI
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.api.auth import router as auth_router

app = FastAPI(title="FastAPI API Hub App", version="1.0.0")

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI API Hub App!"}

app.include_router(auth_router)

