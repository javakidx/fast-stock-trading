import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

# Read env variables
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "mydatabase")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/?retryWrites=true&w=majority&appName=Cluster0"

def db_connect():
    uri = "mongodb+srv://app-user:p4ssw0rd123@cluster0.deys8ga.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        print(e)
    
def insert_one():
    client = None
    try:
        # uri = "mongodb+srv://app-user:p4ssw0rd123@cluster0.deys8ga.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

        database = client[MONGO_DB]
        collection = database["stocks"]

        # start example code here
        result = collection.insert_one({ "symbols" : "2882" })
        # end example code here
        return result.inserted_id

    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)
    finally:
        if client:
            client.close()