#!/usr/bin/env python3
"""
MongoDB Connection Test Script
Tests MongoDB Atlas connection using Motor
"""

import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

async def test_mongodb_connection():
    """Test MongoDB Atlas connection"""
    print("🔍 Testing MongoDB Atlas Connection...")
    print("=" * 50)
    
    # Get connection details
    mongo_uri = os.getenv("MONGODB_URL")
    database_name = os.getenv("DATABASE_NAME", "ecommerce")
    
    if not mongo_uri:
        print("❌ MONGODB_URL not found in environment variables")
        return False
    
    print(f"📡 MongoDB URI: {mongo_uri[:20]}...")
    print(f"🗄️  Database: {database_name}")
    
    try:
        # Create client with timeouts
        client = AsyncIOMotorClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000
        )
        
        print("🔌 Connecting to MongoDB Atlas...")
        
        # Test connection
        result = await client.admin.command('ping')
        print(f"✅ Connection successful! Ping result: {result}")
        
        # Get database and test basic operations
        db = client[database_name]
        
        # Test collections access
        collections = await db.list_collection_names()
        print(f"📁 Available collections: {collections}")
        
        # Test products collection
        products_collection = db.products
        product_count = await products_collection.count_documents({})
        print(f"📦 Products in database: {product_count}")
        
        # Test orders collection
        orders_collection = db.orders
        order_count = await orders_collection.count_documents({})
        print(f"🛒 Orders in database: {order_count}")
        
        # Test inserting a sample document
        test_doc = {"test": "connection", "timestamp": "2025-07-19"}
        result = await db.test_collection.insert_one(test_doc)
        print(f"📝 Test document inserted with ID: {result.inserted_id}")
        
        # Clean up test document
        await db.test_collection.delete_one({"_id": result.inserted_id})
        print("🧹 Test document cleaned up")
        
        client.close()
        print("✅ MongoDB Atlas connection test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        print(f"🔍 Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mongodb_connection())
