
from sqlalchemy import create_engine, text
from config import DATABASE_URL

# Support standard PostgreSQL URLs with the psycopg driver.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Verify the database connection.
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("SUCCESS! PostgreSQL connected!")
except Exception as exc:
    print(f"PostgreSQL connection failed: {exc}")
