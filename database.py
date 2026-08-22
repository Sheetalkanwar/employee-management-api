from pymongo import MongoClient
from pymongo.server_api import ServerApi

from config import MONGODB_URI, DB_NAME


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


# ==============================
# Test MongoDB connection
# ==============================

try:
    client.admin.command("ping")

    print("SUCCESS! MongoDB connected!")

    # Create unique indexes
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