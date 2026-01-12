from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from starlette.authentication import AuthenticationError
from app.db.mongo import get_database
from app.schemas.user import UserCreate, UserResponse, TokenResponse, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
import jwt
from jwt.exceptions import InvalidTokenError
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db = get_database()
    user_collection = db.get_collection("users")
    db_user = await user_collection.find_one({"email": email})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user["id"] = str(db_user["_id"])
    db_user["avatar_img_id"] = str(db_user["avatar_img_id"]) if db_user.get("avatar_img_id") else None
    #del db_user["password"]
    #del db_user["_id"]
    
    return UserResponse(**db_user)

@router.post("/sign-up", response_model=UserResponse)
async def signup(user: UserCreate):
    db = get_database()
    user_collection = db.get_collection("users")
    
    try:
        existing_user = await user_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered!")
        
        user_model_dump = user.model_dump()
        user_model_dump['identity'] = user.email
        user_model_dump['password'] = get_password_hash(user.password)
        user_model_dump['avatar_img_id'] = ObjectId(user_model_dump['avatar_img_id']) if user_model_dump.get('avatar_img_id') else None
        result = await user_collection.insert_one(user_model_dump)
        
        user_model_dump["id"] = str(result.inserted_id)
        user_model_dump["avatar_img_id"] = (
            str(user_model_dump["avatar_img_id"]) if user_model_dump.get("avatar_img_id") else None
        )
        #del user_model_dump["password"]

        return UserResponse(**user_model_dump)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@router.post("/sign-in", response_model=TokenResponse)
async def signin(user: UserLogin):
    db = get_database()
    user_collection = db.get_collection("users")
    db_user = await user_collection.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials!")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token}

@router.get("/user", response_model=UserResponse)
async def read_current_user(user: UserResponse = Depends(get_current_user)):
    return user

