from pathlib import Path
from dotenv import dotenv_values
import dns.resolver
from pymongo import MongoClient
from pymongo.server_api import ServerApi


# ==============================
# Load environment variables
# ==============================

env_path = Path(__file__).resolve().parent / ".env"
config = dotenv_values(env_path)

uri = config.get("MONGODB_URI")

if not uri:
    raise ValueError("MONGODB_URI is not set in .env")


# ==============================
# Configure DNS
# ==============================

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]


# ==============================
# Connect to MongoDB
# ==============================

client = MongoClient(
    uri,
    server_api=ServerApi("1")
)


try:
    client.admin.command("ping")

    print("SUCCESS! MongoDB connected!")

    # Database
    db = client["employee_management"]

    # Collection
    employees_collection = db["employees"]

    # Unique employee ID
    employees_collection.create_index(
        "id",
        unique=True
    )

    print("Unique index created on employee ID")
    print("Database:", db.name)
    print("Collection:", employees_collection.name)


except Exception as e:
    print("MongoDB connection failed:")
    print(e)