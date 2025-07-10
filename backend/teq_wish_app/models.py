import urllib.parse
from pymongo import MongoClient

# Safely encode credentials
username = urllib.parse.quote_plus("anusha")
password = urllib.parse.quote_plus("anusha@43")

# ✅ Mongo URI with tls=true to fix SSL handshake
uri = f"mongodb+srv://{username}:{password}@cluster0.q66bcnr.mongodb.net/?retryWrites=true&w=majority&tls=true"

# ✅ Connect to MongoDB Atlas
connection = MongoClient(uri)

# ✅ Select DB and Collection
db = connection["teq_wish_db"]
table = db["student_datas"]
