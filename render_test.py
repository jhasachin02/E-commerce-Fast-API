#!/usr/bin/env python3
"""
Render-specific MongoDB connection test
Optimized for cloud deployment environments like Render
"""

import os
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError
import socket
import ssl

async def test_mongodb_render():
    """Test MongoDB connection optimized for Render deployment"""
    
    print("🚀 Render MongoDB Connection Test")
    print("=" * 40)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    mongo_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DATABASE_NAME", "ecommerce")
    
    if not mongo_url:
        print("❌ MONGODB_URL not found in environment")
        return False
    
    print(f"📡 MongoDB URI: {mongo_url[:30]}...")
    print(f"🗄️  Database: {db_name}")
    print()
    
    # Test with optimized settings for cloud deployment
    print("🧪 Testing MongoDB Connection (Cloud Optimized)")
    print("-" * 40)
    
    try:
        # Use longer timeout and better error handling for cloud environments
        client = AsyncIOMotorClient(
            mongo_url, 
            serverSelectionTimeoutMS=30000,  # 30 seconds
            connectTimeoutMS=20000,          # 20 seconds
            maxPoolSize=10,
            retryWrites=True,
            ssl=True,
            ssl_cert_reqs=ssl.CERT_NONE
        )
        
        print("📡 Attempting connection...")
        
        # Test connection with ping
        await client.admin.command('ping')
        print("✅ MongoDB ping successful")
        
        # Test database access
        db = client[db_name]
        
        # Check if we can list collections
        try:
            collections = await db.list_collection_names()
            print(f"✅ Database accessible")
            print(f"📂 Collections found: {len(collections)}")
            for col in collections[:5]:  # Show first 5 collections
                print(f"   - {col}")
            if len(collections) > 5:
                print(f"   ... and {len(collections) - 5} more")
        except Exception as e:
            print(f"⚠️  Could not list collections: {e}")
            
        # Test basic CRUD operations
        test_collection = db.test_connection
        
        # Insert test document
        test_doc = {
            "test": "render_deployment", 
            "timestamp": "2024-01-01",
            "environment": "render"
        }
        
        result = await test_collection.insert_one(test_doc)
        print(f"✅ Insert operation successful")
        print(f"📄 Document ID: {result.inserted_id}")
        
        # Read test document
        found_doc = await test_collection.find_one({"_id": result.inserted_id})
        if found_doc:
            print("✅ Read operation successful")
        
        # Update test document
        await test_collection.update_one(
            {"_id": result.inserted_id},
            {"$set": {"updated": True}}
        )
        print("✅ Update operation successful")
        
        # Delete test document
        await test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Delete operation successful")
        
        # Test collections that should exist for ecommerce
        expected_collections = ['products', 'orders', 'users']
        for col_name in expected_collections:
            try:
                count = await db[col_name].count_documents({})
                print(f"📊 {col_name} collection: {count} documents")
            except Exception as e:
                print(f"ℹ️  {col_name} collection not accessible: {e}")
        
        await client.close()
        print("\n🎯 MongoDB connection test: ✅ SUCCESS")
        return True
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ Server selection timeout: {str(e)[:100]}...")
        print("💡 This might be a network connectivity issue")
    except ConfigurationError as e:
        print(f"❌ Configuration error: {str(e)[:100]}...")
        print("💡 Check MongoDB connection string format")
    except ConnectionFailure as e:
        print(f"❌ Connection failure: {str(e)[:100]}...")
        print("💡 Check MongoDB server availability")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)[:100]}...")
        print(f"🔍 Error type: {type(e).__name__}")
    
    print("\n🎯 MongoDB connection test: ❌ FAILED")
    return False

def test_environment_variables():
    """Test environment variables setup"""
    
    print("\n🧪 Environment Variables Test")
    print("-" * 30)
    
    required_vars = ['MONGODB_URL']
    optional_vars = ['DATABASE_NAME']
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Show partial value for security
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
            all_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"ℹ️  {var}: Not set (using default)")
    
    return all_good

def test_package_imports():
    """Test that all required packages can be imported"""
    
    print("\n🧪 Package Import Test")
    print("-" * 20)
    
    packages = [
        ('motor', 'motor.motor_asyncio'),
        ('pymongo', 'pymongo'),
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('pydantic', 'pydantic'),
        ('dotenv', 'python-dotenv')
    ]
    
    all_imports_ok = True
    
    for package_name, import_name in packages:
        try:
            __import__(package_name)
            print(f"✅ {import_name}")
        except ImportError as e:
            print(f"❌ {import_name}: {e}")
            all_imports_ok = False
    
    return all_imports_ok

async def main():
    """Run comprehensive test for Render deployment"""
    
    print("🌐 Render Deployment Test Suite")
    print("=" * 40)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test 1: Environment variables
    env_ok = test_environment_variables()
    
    # Test 2: Package imports
    imports_ok = test_package_imports()
    
    # Test 3: MongoDB connection
    mongo_ok = await test_mongodb_render()
    
    # Summary
    print("\n📊 Render Deployment Test Summary")
    print("=" * 40)
    print(f"Environment Variables: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Package Imports:       {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"MongoDB Connection:    {'✅ PASS' if mongo_ok else '❌ FAIL'}")
    
    overall = env_ok and imports_ok and mongo_ok
    print(f"\n🎯 Overall Status: {'✅ READY FOR RENDER' if overall else '❌ NEEDS ATTENTION'}")
    
    if not overall:
        print("\n💡 Troubleshooting Tips:")
        if not env_ok:
            print("   - Check environment variables in Render dashboard")
        if not imports_ok:
            print("   - Verify requirements.txt has all dependencies")
        if not mongo_ok:
            print("   - Check MongoDB Atlas network access settings")
            print("   - Verify MongoDB connection string is correct")
            print("   - Ensure MongoDB cluster is running")
    
    return overall

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
