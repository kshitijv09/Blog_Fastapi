from pymongo import MongoClient

client=MongoClient("mongodb+srv://kshitijv09:surajpura@cluster0.9yxaavh.mongodb.net/?retryWrites=true&w=majority")
db=client.blog_db

collection_name = db.blog_collection