from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
def connect_db(app):
    app.config['MONGODB_URI'] = os.getenv("MONGODB_URI")
    client = MongoClient(app.config['MONGODB_URI'])
    db = client['test']
    return db