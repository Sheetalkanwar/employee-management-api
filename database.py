import os
from pathlib import Path
from dotenv import dotenv_values
import dns.resolver
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGODB_URI, DB_NAME


# ==============================
# Load environment variables
# ==============================

env_path = Path(__file__).resolve().parent / ".env"
config = dotenv_values(env_path)

MONGODB_URI = config.get("MONGODB_URI")

# ==============================
# Configure DNS
# ==============================

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]


# ==============================
# Connect to MongoDB
# ==============================

client = MongoClient(
    MONGODB_URI,
    server_api=ServerApi("1")
)
db = client[DB_NAME]

employees_collection = db["employees"]
users_collection = db["users"]


try:
    client.admin.command("ping")

    print("SUCCESS! MongoDB connected!")

    # Database
    DB_NAME = os.getenv(
      "DB_NAME",
      config.get("DB_NAME", "employee_management")
)

    db = client[DB_NAME]

    # Collection
    employees_collection = db["employees"]
    users_collection = db["users"]

    # Unique employee ID
    employees_collection.create_index(
        "id",
        unique=True
    )
    users_collection.create_index(
    "username",
    unique=True
   )

    print("Unique index created on employee ID")
    print("Database:", db.name)
    print("Collection:", employees_collection.name)


except Exception as e:
    print("MongoDB connection failed:")
    print(e)