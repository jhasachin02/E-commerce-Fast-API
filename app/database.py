import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from dotenv import load_dotenv
import dns.resolver

# Load environment variables
load_dotenv()

# Global database client
database_client: Optional[AsyncIOMotorClient] = None
database_name: Optional[str] = None

def configure_dns():
    """
    Configure DNS resolver to use reliable DNS servers (Google DNS).
    This fixes MongoDB Atlas SRV record resolution timeouts.
    """
    try:
        dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
        dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
        print("🔧 DNS configured to use Google DNS for MongoDB Atlas SRV resolution")
    except Exception as e:
        print(f"⚠️  DNS configuration warning: {e}")

async def connect_to_mongo():
    """
    Connect to MongoDB using Motor async driver.
    Connection details are loaded from environment variables.
    """
    global database_client, database_name
    
    # Configure DNS first to avoid SRV record resolution timeouts
    configure_dns()
    
    # Get MongoDB connection details from environment variables
    mongo_uri = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name = os.getenv("DATABASE_NAME", "ecommerce")
    
    try:
        # Create Motor client with extended timeout settings for cloud deployment
        database_client = AsyncIOMotorClient(
            mongo_uri,
            serverSelectionTimeoutMS=30000,  # 30 second timeout for cloud environments
            connectTimeoutMS=10000,          # 10 second connection timeout
            socketTimeoutMS=10000            # 10 second socket timeout
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

async def get_database():
    """
    Get the database instance with lazy connection.
    Returns the database object for use in routers.
    """
    global database_client, database_name
    
    if database_client is None:
        await connect_to_mongo()
    
    if database_client is None:
        raise RuntimeError("Database client not available. MongoDB connection failed.")
    
    return database_client[database_name]

async def get_collection(collection_name: str):
    """
    Get a specific collection from the database with lazy connection.
    
    Args:
        collection_name (str): Name of the collection to retrieve
        
    Returns:
        Collection object
    """
    try:
        database = await get_database()
        return database[collection_name]
    except Exception as e:
        print(f"❌ Failed to get collection {collection_name}: {e}")
        raise e 