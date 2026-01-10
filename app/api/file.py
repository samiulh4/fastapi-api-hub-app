from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from datetime import datetime
from pathlib import Path
import os
import uuid
import shutil
import aiofiles
from bson import ObjectId
from app.db.mongo import get_database
from app.core.config import FAST_API_BASE_URL
from app.schemas.file import FileResponse

router = APIRouter(prefix="/file", tags=['File'])

@router.post("/upload", response_model=FileResponse)
async def file_upload(
    file: UploadFile = File(...)
    ):
    current_date = datetime.now()
    year_month_path = Path("uploads") / str(current_date.year) / f"{current_date.month:02d}"
    year_month_path.mkdir(parents=True, exist_ok=True)
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = year_month_path / file_name
    file_url = f"/uploads/{current_date.year}/{current_date.month:02d}/{file_name}"
    
    full_url = FAST_API_BASE_URL + file_url

    # with file_path.open("wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)

    # ASYNC FILE WRITE
    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(1024 * 1024):  # 1MB chunks
            await out_file.write(content)

    db = get_database()
    file_collection = db.get_collection("files")
    file_record = {
        "file_name": file.filename.rsplit(".", 1)[0],
        "file_ext": file_ext,
        "file_url": full_url,
        "file_status": "inactive",
        "created_by": None,
        "uploaded_by": None,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }        
    result = await file_collection.insert_one(file_record)
    
    return FileResponse(
        file_id=str(result.inserted_id),
        file_name=file_record["file_name"],
        file_url=full_url,
        file_status=file_record["file_status"]
    )

@router.get("/view/{file_id}", response_model=FileResponse)
async def file_view(file_id: str):
    db = get_database()
    file_collection = db.get_collection("files")
    try:
        file_record = await file_collection.find_one({"_id": ObjectId(file_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid file ID format")
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
     
    return FileResponse(
        file_id=str(file_record["_id"]),
        file_name=file_record["file_name"],
        file_url=file_record["file_url"],
        file_status=file_record["file_status"]
    )

async def file_status_update(file_id: str, status: str, updated_by: str = None) -> bool:
    db = get_database()
    file_collection = db.get_collection("files")

    try:
        object_id = ObjectId(file_id)
        result = await file_collection.update_one(
            {"_id": object_id},
            {"$set": 
             {"file_status": status, "updated_by": updated_by, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            }
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Error updating file status")
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="File not found")
    
    return True 