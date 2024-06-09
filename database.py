import os
import json
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import CollectionInvalid 
from pymongo import DeleteMany, InsertOne
from fastapi import HTTPException

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

db_config = config['db']

# Initialize MongoDB client
connection_string = f"mongodb://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}"

# for logging purpose
print(f"connection string is {connection_string}")

client = AsyncIOMotorClient(connection_string)
database = client[db_config['name']]

async def create_collection(collection_name: str):
    """Create a collection if it does not exist."""
    try:
        await database.create_collection(collection_name)
        print(f"Collection '{collection_name}' created successfully.")
    except CollectionInvalid:
        print(f"Collection '{collection_name}' already exists.")

async def delete_all_promotions(promotions: list):
    """Delete all promotions from the promotions collection."""
    try:
        await database['promotions'].delete_many({})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed in deleting promotions {str(e)}")

async def bulk_insert_promotion(promotions: list):
    """Inserting multiple promotions into the promotions collection."""
    try:
        await database['promotions'].insert_many(promotions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed in adding promotions {str(e)}")

async def delete_all_promotions():
    """Delete all promotions from the promotions collection."""
    try:
        await database['promotions'].delete_many({})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed in deleting promotions {str(e)}")

async def delete_and_insert_all_promotions(promotions: list):
    """Erase all existing promotions and insert new bulk promotions in the promotions collection."""
    try:
        bulk_operations = [DeleteMany({})]
        for promotion in promotions:
            bulk_operations.append(InsertOne(promotion))
        await database['promotions'].bulk_write(bulk_operations)
        # await database['promotions'].delete_many({})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed in erasing and adding promotions {str(e)}")
    
async def get_promotion(promotion_id: str):
    """Retrieve a promotion by its ID."""
    try:
        promotion = await database['promotions'].find_one({"id": promotion_id})
        if promotion is None:
            raise HTTPException(status_code=404, detail="Promotion not found")
        return promotion
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed in fetching promotion, Error: {str(e)}")

async def health_check():
    """Perform a health check on the database."""
    if database is None:
        raise HTTPException(status_code=500, detail="Database connection not established")
    try:
        # Simple query to check database connection
        await database.command("ping")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed, Error: {str(e)}")
    return {"status": "ok"}
