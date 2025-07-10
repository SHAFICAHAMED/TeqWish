import urllib.parse
from pymongo import MongoClient

username = urllib.parse.quote_plus("anusha")
password = urllib.parse.quote_plus("anusha@43")
uri = f"mongodb+srv://{username}:{password}@cluster0.q66bcnr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection = MongoClient(uri)
db = connection["teq_wish_db"]
table = db["student_datas"]