from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.api.auth import router as auth_router
from app.api.file import router as file_router
from app.api.blog import router as blog_router

app = FastAPI(title="FastAPI API Hub App", version="1.0.0")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

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
app.include_router(file_router)
app.include_router(blog_router)

