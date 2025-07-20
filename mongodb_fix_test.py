#!/usr/bin/env python3
"""
MongoDB connection test with DNS workaround
"""

import os
import asyncio
import dns.resolver
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConfigurationError

async def test_mongodb_with_dns_fix():
    """Test MongoDB with DNS server configuration"""
    
    print("🔧 MongoDB Connection Test with DNS Fix")
    print("=" * 50)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    mongo_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DATABASE_NAME", "ecommerce")
    
    if not mongo_url:
        print("❌ MONGODB_URL not found")
        return False
    
    print(f"📡 MongoDB URI: {mongo_url[:20]}...")
    print(f"🗄️  Database: {db_name}")
    
    # Configure DNS resolver to use Google DNS
    print("\n🔧 Configuring DNS resolver...")
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    print("✅ DNS configured to use Google DNS (8.8.8.8, 8.8.4.4)")
    
    try:
        print("\n🔍 Testing connection...")
        
        # Create client with custom DNS timeout
        client = AsyncIOMotorClient(
            mongo_url, 
            serverSelectionTimeoutMS=15000,  # 15 seconds
            connectTimeoutMS=10000,          # 10 seconds
            socketTimeoutMS=10000            # 10 seconds
        )
        
        # Test connection
        print("📡 Attempting to ping MongoDB...")
        await asyncio.wait_for(client.admin.command('ping'), timeout=20)
        print("✅ MongoDB ping successful!")
        
        # Test database operations
        db = client[db_name]
        
        print("📊 Testing database operations...")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"✅ Collections found: {collections}")
        
        # Test insert
        test_collection = db.connection_test
        result = await test_collection.insert_one({
            "test": "connection_successful", 
            "timestamp": "2024-01-01",
            "status": "working"
        })
        print(f"✅ Insert successful, ID: {result.inserted_id}")
        
        # Test find
        document = await test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Find successful: {document}")
        
        # Clean up
        await test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Cleanup successful")
        
        await client.close()
        
        print("\n🎉 MongoDB is working perfectly!")
        return True
        
    except asyncio.TimeoutError:
        print("❌ Connection timeout - MongoDB Atlas may be unreachable")
    except ConfigurationError as e:
        print(f"❌ Configuration error: {str(e)[:100]}...")
    except Exception as e:
        print(f"❌ Connection failed: {str(e)[:100]}...")
    
    return False

async def test_alternative_connection():
    """Test with a direct connection string approach"""
    
    print("\n🔄 Trying alternative connection approach...")
    
    # Alternative: Use IP addresses directly if SRV fails
    try:
        # Get the actual server IPs from SRV records
        print("🔍 Resolving MongoDB server addresses...")
        
        srv_records = dns.resolver.resolve('_mongodb._tcp.cluster0.hdgbtcf.mongodb.net', 'SRV')
        servers = []
        
        for record in srv_records:
            server_name = str(record.target).rstrip('.')
            try:
                # Resolve A record for each server
                a_records = dns.resolver.resolve(server_name, 'A')
                for a_record in a_records:
                    servers.append(f"{a_record}:{record.port}")
                    print(f"   Found server: {a_record}:{record.port}")
            except:
                pass
        
        if servers:
            # Create direct connection string
            mongo_url = os.getenv("MONGODB_URL")
            # Extract credentials from original URL
            if "@" in mongo_url:
                credentials = mongo_url.split("://")[1].split("@")[0]
                db_params = mongo_url.split("?")[1] if "?" in mongo_url else ""
                
                # Build direct connection string
                server_list = ",".join(servers[:2])  # Use first 2 servers
                direct_url = f"mongodb://{credentials}@{server_list}/ecommerce"
                if db_params:
                    direct_url += f"?{db_params}"
                
                print(f"🔗 Direct connection: mongodb://{credentials.split(':')[0]}:***@{server_list}/...")
                
                # Test direct connection
                client = AsyncIOMotorClient(direct_url, serverSelectionTimeoutMS=10000)
                await client.admin.command('ping')
                print("✅ Direct connection successful!")
                await client.close()
                return True
                
    except Exception as e:
        print(f"❌ Alternative connection failed: {e}")
    
    return False

async def main():
    """Run all connection tests"""
    
    # Test 1: With DNS fix
    success1 = await test_mongodb_with_dns_fix()
    
    if not success1:
        # Test 2: Alternative approach
        success2 = await test_alternative_connection()
    else:
        success2 = True
    
    print("\n" + "=" * 50)
    if success1 or success2:
        print("🎉 RESULT: MongoDB connection is WORKING!")
        print("✅ Your API can connect to MongoDB Atlas")
    else:
        print("❌ RESULT: MongoDB connection FAILED")
        print("🔧 Check your internet connection and MongoDB Atlas settings")
    
    return success1 or success2

if __name__ == "__main__":
    asyncio.run(main())
