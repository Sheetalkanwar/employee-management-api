
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in backend/.env")

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is not set in backend/.env")
