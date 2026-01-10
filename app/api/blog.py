from fastapi import APIRouter, HTTPException, Depends
from app.api.auth import get_current_user
from app.schemas.blog import BlogCreate, BlogResponse
from app.api.auth import get_current_user
from app.db.mongo import get_database
from datetime import datetime
from app.api.file import file_status_update

router = APIRouter(prefix="/blog", tags=["Blog"])

@router.post("/create", response_model=BlogResponse)
async def create_blog(blog: BlogCreate, current_user = Depends(get_current_user)):
    try:
        db = get_database()
        blog_collection = db.get_collection("blogs")
        blog_dict = blog.dict()
        blog_dict["blog_author_id"] = current_user.id
        blog_dict["blog_status"] = "active"
        blog_dict["created_by"] = current_user.id
        blog_dict["updated_by"] = current_user.id
        blog_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        blog_dict["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = await blog_collection.insert_one(blog_dict)
        if not result.acknowledged:
            raise HTTPException(status_code=500, detail="Failed to create blog post")
        if blog.blog_img_id:
            await file_status_update(blog.blog_img_id, "active", blog_dict["blog_author_id"])
        blog_dict["id"] = str(result.inserted_id)
        return BlogResponse(**blog_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))