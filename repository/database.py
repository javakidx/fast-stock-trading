import os

from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from typing import List

load_dotenv()

# Read env variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "mydatabase")
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/?retryWrites=true&w=majority&appName=Cluster0"


def db_connect():
    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        print(e)


def insert_one(collection: str, document: BaseModel):
    client = None
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

        database = client[MONGO_DB]
        collection = database[collection]

        # start example code here
        result = collection.insert_one(document.model_dump())
        # end example code here
        return result.inserted_id

    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
    finally:
        if client:
            client.close()


def insert_many(collection_name: str, documents: List[BaseModel]) -> List[str]:
    client = None
    try:
        # Initialize MongoDB client
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[MONGO_DB]
        collection = db[collection_name]

        # Convert Pydantic models to dicts
        payload = [doc.model_dump(by_alias=True, exclude_none=True) for doc in documents]

        if not payload:
            raise ValueError("No documents to insert.")

        # Insert documents
        result = collection.insert_many(payload)
        return [str(_id) for _id in result.inserted_ids]

    except PyMongoError as e:
        raise RuntimeError(f"MongoDB insert_many failed: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"An error occurred: {str(e)}") from e
    finally:
        if client:
            client.close()


def drop_collection(collection_name: str):
    client = None
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[MONGO_DB]
        db.drop_collection(collection_name)
    except PyMongoError as e:
        raise RuntimeError(f"MongoDB drop_collection failed: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"An error occurred: {str(e)}") from e
    finally:
        if client:
            client.close()
