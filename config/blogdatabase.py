from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

client=MongoClient(f"mongodb+srv://{username}:{password}@cluster0.9yxaavh.mongodb.net/?retryWrites=true&w=majority")
db=client.blog_db

collection_name = db.blog_collection