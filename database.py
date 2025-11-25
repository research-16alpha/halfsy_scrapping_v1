#%%

from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def test_connection():

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()  # Force connection check

        print("🚀 MongoDB connection successful!")

        db = client[DATABASE_NAME]
        print(f"📦 Databases: {client.list_database_names()}")
        print(f"📁 Collections in {DATABASE_NAME}: {db.list_collection_names()}")

    except Exception as e:
        print("❌ MongoDB connection failed!")
        print(e)

test_connection()


client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db["products"]

def insert_data(product_list):
    try:
        #product_list = json.load(open("DoversStreet_products.json"))

        # Insertion
        new_count = 0
        updated_count = 0

        for product in product_list:
            result = collection.update_one(
                {"product_link": product["product_link"]},
                {"$set": product},
                upsert=True
            )
            
            if result.upserted_id:  
                # This means a new document was inserted
                new_count += 1
            else:
                # If matched_count == 1 and upserted_id is None → document existed
                updated_count += 1

        print("Products Inserted Successfully")
        print("New inserts:", new_count)
        print("Updated existing:", updated_count)
        
    except Exception as e:
        print(f"Error inserting data: {e}")

def count_products(brand_name):
    count = collection.count_documents({
        "product_link": {"$regex": brand_name, "$options": "i"}
    })
    print(f"Number of products for {brand_name}: {count}")



