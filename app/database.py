import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global database client
database_client: Optional[AsyncIOMotorClient] = None
database_name: Optional[str] = None

async def connect_to_mongo():
    """
    Connect to MongoDB using Motor async driver.
    Connection details are loaded from environment variables.
    """
    global database_client, database_name
    
    # Get MongoDB connection details from environment variables
    mongo_uri = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name = os.getenv("DATABASE_NAME", "ecommerce")
    
    try:
        # Create Motor client with timeout settings
        database_client = AsyncIOMotorClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        # Test the connection
        await database_client.admin.command('ping')
        print(f"✅ Successfully connected to MongoDB at {mongo_uri}")
        print(f"📁 Using database: {database_name}")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("⚠️  API will continue to run but database operations will fail")
        # Don't raise the exception - let the API start without MongoDB
        database_client = None

async def close_mongo_connection():
    """
    Close the MongoDB connection.
    """
    global database_client
    
    if database_client:
        database_client.close()
        print("🔌 MongoDB connection closed")

def get_database():
    """
    Get the database instance.
    Returns the database object for use in routers.
    """
    if database_client is None:
        raise RuntimeError("Database client not available. MongoDB connection failed during startup.")
    
    return database_client[database_name]

def get_collection(collection_name: str):
    """
    Get a specific collection from the database.
    
    Args:
        collection_name (str): Name of the collection to retrieve
        
    Returns:
        Collection object
    """
    database = get_database()
    return database[collection_name] 