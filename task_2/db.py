from pymongo import MongoClient


def get_db_connection():
    client = MongoClient("localhost", 27017)
    db = client["cats_database"]
    return db.cats
