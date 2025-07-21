#!/usr/bin/env python3
"""
Simple MongoDB connection test that should work on Render
"""

import os
import asyncio
from dotenv import load_dotenv

# DNS fix for cloud environments
try:
    import dns.resolver
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1']
    print("🔧 DNS resolver configured with public DNS servers")
except Exception as e:
    print(f"⚠️  DNS warning: {e}")

async def quick_mongo_test():
    """Quick MongoDB test for Render"""
    
    load_dotenv()
    
    from motor.motor_asyncio import AsyncIOMotorClient
    from pymongo.errors import ServerSelectionTimeoutError
    
    mongo_url = os.getenv("MONGODB_URL")
    if not mongo_url:
        print("❌ MONGODB_URL not set")
        return False
    
    print(f"🔗 Connecting to MongoDB...")
    
    try:
        client = AsyncIOMotorClient(
            mongo_url,
            serverSelectionTimeoutMS=15000,
            ssl=True
        )
        
        # Simple ping test
        await client.admin.command('ping')
        print("✅ MongoDB connected successfully!")
        
        # Test database access
        db = client.ecommerce
        collections = await db.list_collection_names()
        print(f"📂 Found {len(collections)} collections")
        
        # Close connection properly
        if client:
            client.close()
        return True
        
    except ServerSelectionTimeoutError:
        print("❌ Connection timeout - DNS or network issue")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Quick MongoDB Test for Render")
    result = asyncio.run(quick_mongo_test())
    if result:
        print("🎉 Ready for Render deployment!")
    else:
        print("⚠️  May have issues on deployment")
