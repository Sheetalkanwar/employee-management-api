from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    require_admin
)
from models.user import UserCreate
from database import users_collection



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
        "role": "user"
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
@router.get(
    "/users",
    summary="Get all users"
)
def get_all_users(
    current_user: dict = Depends(require_admin)
):

    users = list(
        users_collection.find(
            {},
            {
                "_id": 0,
                "password": 0
            }
        )
    )

    return users

@router.get(
    "/users/{username}",
    summary="Get user by username"
)
def get_user_by_username(
    username: str,
    current_user: dict = Depends(require_admin)
):

    user = users_collection.find_one(
        {"username": username},
        {
            "_id": 0,
            "password": 0
        }
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.delete(
    "/users/{username}",
    summary="Delete a user"
)
def delete_user(
    username: str,
    current_user: dict = Depends(require_admin)
):

    # Prevent admin from accidentally deleting themselves
    if username == current_user["username"]:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot delete themselves"
        )

    result = users_collection.delete_one(
        {"username": username}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully!"
    }