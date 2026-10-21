from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://sheetal2004shekhawat_db_user:shit420@cluster0.y6206ti.mongodb.net/?appName=Cluster0"

client = MongoClient(
    uri,
    server_api=ServerApi("1")
)

print("Trying to connect...")

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print("Connection failed:")
    print(e)