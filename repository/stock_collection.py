import os

from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from typing import List
from models import Stock

load_dotenv()

# Read env variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "mydatabase")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/?retryWrites=true&w=majority&appName=Cluster0"

STOCKS_COLLECTION = "stocks"

def find(symbol: str):
    client = None

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

        database = client[MONGO_DB]
        collection = database[STOCKS_COLLECTION]

        # start example code here
        doc = collection.find_one({"symbol": symbol})
        if doc:
            return Stock(**doc)

        return None
        # end example code here
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
    finally:
        if client:
            client.close()
