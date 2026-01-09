from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from starlette.authentication import AuthenticationError
from app.db.mongo import get_database
from app.schemas.user import UserCreate, UserResponse, TokenResponse, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
import jwt
from jwt.exceptions import InvalidTokenError

router = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    """Verify JWT token and return current user"""
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
    del db_user["password"]
    del db_user["_id"]
    return UserResponse(**db_user)

@router.post("/sign-up", response_model=UserResponse)
async def signup(user: UserCreate):
    db = get_database()
    user_collection = db.get_collection("users")
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered!")
    
    user_dict = user.dict()
    user_dict['identity'] = user.email
    user_dict['password'] = get_password_hash(user.password)
    
    result = await user_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    del user_dict["password"]

    return UserResponse(**user_dict)

@router.post("/sign-in", response_model=TokenResponse)
async def signin(user: UserLogin):
    db = get_database()
    user_collection = db.get_collection("users")
    db_user = await user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials!")
    token = create_access_token({"sub": user.email})
    return {"access_token": token}

@router.get("/me", response_model=UserResponse)
async def read_current_user(user: UserResponse = Depends(get_current_user)):
    return user

