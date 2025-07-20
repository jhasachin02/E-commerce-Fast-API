#!/usr/bin/env python3
"""
Simple MongoDB connection test - Fixed version
"""

import os
import asyncio
import dns.resolver
from motor.motor_asyncio import AsyncIOMotorClient

async def simple_mongodb_test():
    """Simple test that actually works"""
    
    print("🧪 Simple MongoDB Test")
    print("=" * 30)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    mongo_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DATABASE_NAME", "ecommerce")
    
    if not mongo_url:
        print("❌ MONGODB_URL not found")
        return False
    
    # Configure DNS to use Google DNS (fixes the timeout issue)
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    
    try:
        print("🔍 Connecting to MongoDB...")
        
        # Create client
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=10000)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Test database
        db = client[db_name]
        
        # Test collection operations
        products = db.products
        
        # Try to find products
        product_count = await products.count_documents({})
        print(f"📊 Products collection has {product_count} documents")
        
        # Test insert
        test_doc = {"name": "Test Product", "price": 99.99, "sizes": [{"size": "M", "quantity": 10}]}
        result = await products.insert_one(test_doc)
        print(f"✅ Insert successful: {result.inserted_id}")
        
        # Test find
        found_doc = await products.find_one({"_id": result.inserted_id})
        print(f"✅ Find successful: {found_doc['name']}")
        
        # Clean up test document
        await products.delete_one({"_id": result.inserted_id})
        print("✅ Cleanup successful")
        
        # Properly close client
        client.close()
        print("✅ Connection closed properly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_api_endpoints():
    """Test that the actual API can connect to MongoDB"""
    
    print("\n🔧 Testing API Database Functions")
    print("=" * 35)
    
    try:
        # Import your actual database module
        from app.database import get_collection
        
        # Test getting a collection
        products_collection = await get_collection("products")
        print("✅ Products collection accessible")
        
        # Test basic operations
        count = await products_collection.count_documents({})
        print(f"📊 Current products in database: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ API database test failed: {e}")
        return False

async def main():
    """Run tests"""
    
    print("🚀 MongoDB Connection Status Check")
    print("=" * 50)
    
    # Test 1: Direct connection
    test1 = await simple_mongodb_test()
    
    # Test 2: API functions
    test2 = await test_api_endpoints()
    
    # Summary
    print("\n📊 FINAL RESULTS")
    print("=" * 20)
    print(f"Direct Connection: {'✅ WORKING' if test1 else '❌ FAILED'}")
    print(f"API Functions:     {'✅ WORKING' if test2 else '❌ FAILED'}")
    
    overall_status = test1 and test2
    print(f"\n🎯 MONGODB STATUS: {'✅ FULLY WORKING' if overall_status else '❌ ISSUES DETECTED'}")
    
    if overall_status:
        print("\n🎉 Your API can successfully connect to MongoDB!")
        print("🚀 Product creation, orders, and all database operations should work!")
    else:
        print("\n🔧 There are connection issues that need to be resolved.")
    
    return overall_status

if __name__ == "__main__":
    result = asyncio.run(main())
