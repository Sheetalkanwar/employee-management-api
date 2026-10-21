
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    require_admin,
)
from models.user import UserCreate
from database import engine

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register_user(user: UserCreate):
    hashed_password = hash_password(user.password)

    try:
        with engine.begin() as connection:
            result = connection.execute(
                text("""
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (:username, :email, :password_hash, 'user')
                    RETURNING id, username
                """),
                {
                    "username": user.username,
                    "email": user.email,
                    "password_hash": hashed_password,
                },
            )
            new_user = result.mappings().one()

        return {
            "message": "User registered successfully!",
            "user_id": str(new_user["id"]),
            "username": new_user["username"],
        }

    except IntegrityError:
        # A username or email may already exist.
        with engine.connect() as connection:
            existing = connection.execute(
                text("""
                    SELECT username, email FROM users
                    WHERE username = :username OR email = :email
                """),
                {"username": user.username, "email": user.email},
            ).mappings().first()

        if existing and existing["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")
        raise HTTPException(status_code=400, detail="Email already exists")


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    with engine.connect() as connection:
        existing_user = connection.execute(
            text("""
                SELECT id, username, password_hash, role
                FROM users
                WHERE username = :username
            """),
            {"username": form_data.username},
        ).mappings().first()

    if not existing_user or not verify_password(
        form_data.password,
        existing_user["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    access_token = create_access_token({
        "sub": existing_user["username"],
        "role": existing_user["role"],
    })

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", summary="Get all users")
def get_all_users(current_user: dict = Depends(require_admin)):
    with engine.connect() as connection:
        users = connection.execute(
            text("""
                SELECT id, username, email, role, created_at
                FROM users ORDER BY username
            """)
        ).mappings().all()

    return [dict(user) for user in users]


@router.get("/users/{username}", summary="Get user by username")
def get_user_by_username(
    username: str,
    current_user: dict = Depends(require_admin),
):
    with engine.connect() as connection:
        user = connection.execute(
            text("""
                SELECT id, username, email, role, created_at
                FROM users WHERE username = :username
            """),
            {"username": username},
        ).mappings().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return dict(user)


@router.delete("/users/{username}", summary="Delete a user")
def delete_user(
    username: str,
    current_user: dict = Depends(require_admin),
):
    if username == current_user["username"]:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot delete themselves",
        )

    with engine.begin() as connection:
        result = connection.execute(
            text("DELETE FROM users WHERE username = :username"),
            {"username": username},
        )

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully!"}
