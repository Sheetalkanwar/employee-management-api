from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.user import UserCreate
from database import users_collection
from auth import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(user: UserCreate):

    existing_user = users_collection.find_one({
        "username": user.username
    })

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "role": user.role
    }

    result = users_collection.insert_one(user_data)

    return {
        "message": "User registered successfully!",
        "user_id": str(result.inserted_id)
    }


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    existing_user = users_collection.find_one({
        "username": form_data.username
    })

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        existing_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token({
        "sub": existing_user["username"],
        "role": existing_user.get("role", "user")
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }