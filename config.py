import os
from pathlib import Path

from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)


MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "employee_management")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_EXPIRE_MINUTES = int(
    os.getenv("JWT_EXPIRE_MINUTES", "30")
)


if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in .env")

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is not set in .env")