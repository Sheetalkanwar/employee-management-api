
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import JWT_SECRET_KEY, JWT_EXPIRE_MINUTES

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = JWT_EXPIRE_MINUTES


# Load .env

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
      minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )


# JWT authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role", "user")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        return {
            "username": username,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
def require_admin(
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user