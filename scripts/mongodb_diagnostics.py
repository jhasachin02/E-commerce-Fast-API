#!/usr/bin/env python3
"""
Comprehensive MongoDB connection test
Tests various aspects of MongoDB connectivity
"""

import os
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError
import dns.resolver
from urllib.parse import urlparse
import socket

async def test_mongodb_connection():
    """Test MongoDB connection with detailed diagnostics"""
    
    print("🔍 MongoDB Connection Diagnostics")
    print("=" * 50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    mongo_url = os.getenv("MONGODB_URL")
    db_name = os.getenv("DATABASE_NAME", "ecommerce")
    
    if not mongo_url:
        print("❌ MONGODB_URL not found in environment")
        return False
    
    print(f"📡 MongoDB URI: {mongo_url[:20]}...")
    print(f"🗄️  Database: {db_name}")
    print()
    
    # Test 1: Basic connectivity test
    print("🧪 Test 1: Basic Connection Test")
    print("-" * 30)
    
    try:
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=10000)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB ping successful")
        
        # Test database access
        db = client[db_name]
        collections = await db.list_collection_names()
        print(f"✅ Database accessible, collections: {collections}")
        
        # Test basic operation
        test_collection = db.test
        result = await test_collection.insert_one({"test": "connection", "timestamp": "2024-01-01"})
        print(f"✅ Insert test successful, ID: {result.inserted_id}")
        
        # Clean up test document
        await test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Cleanup successful")
        
        await client.close()
        return True
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ Server selection timeout: {e}")
    except ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
    except ConnectionFailure as e:
        print(f"❌ Connection failure: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return False

def test_dns_resolution():
    """Test DNS resolution for MongoDB Atlas"""
    
    print("\n🧪 Test 2: DNS Resolution Test")
    print("-" * 30)
    
    try:
        mongo_url = os.getenv("MONGODB_URL")
        if not mongo_url:
            print("❌ No MongoDB URL to test")
            return False
            
        # Extract hostname from MongoDB URL
        if mongo_url.startswith("mongodb+srv://"):
            # Parse SRV record
            parsed = urlparse(mongo_url)
            hostname = parsed.hostname
            
            print(f"🔍 Testing SRV record for: {hostname}")
            
            try:
                # Test SRV record resolution
                srv_records = dns.resolver.resolve(f"_mongodb._tcp.{hostname}", 'SRV')
                print(f"✅ SRV records found: {len(list(srv_records))}")
                
                for record in srv_records:
                    print(f"   - {record.target}:{record.port}")
                    
            except dns.resolver.NXDOMAIN:
                print("❌ SRV record not found (NXDOMAIN)")
            except dns.resolver.Timeout:
                print("❌ DNS timeout resolving SRV record")
            except Exception as e:
                print(f"❌ DNS error: {e}")
                
        else:
            print("ℹ️  Not an SRV connection string")
            
    except Exception as e:
        print(f"❌ DNS test error: {e}")
        return False
    
    return True

def test_network_connectivity():
    """Test basic network connectivity"""
    
    print("\n🧪 Test 3: Network Connectivity Test")
    print("-" * 30)
    
    test_hosts = [
        ("8.8.8.8", 53, "Google DNS"),
        ("1.1.1.1", 53, "Cloudflare DNS"),
        ("mongodb.com", 443, "MongoDB Website")
    ]
    
    for host, port, description in test_hosts:
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            print(f"✅ {description} ({host}:{port}) - Connected")
        except Exception as e:
            print(f"❌ {description} ({host}:{port}) - Failed: {e}")

def test_pymongo_sync():
    """Test synchronous PyMongo connection"""
    
    print("\n🧪 Test 4: Synchronous PyMongo Test")
    print("-" * 30)
    
    try:
        mongo_url = os.getenv("MONGODB_URL")
        if not mongo_url:
            print("❌ No MongoDB URL")
            return False
            
        # Test sync connection
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        
        # Test ping
        client.admin.command('ping')
        print("✅ Sync connection successful")
        
        # List databases
        dbs = client.list_database_names()
        print(f"✅ Databases: {dbs}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Sync connection failed: {e}")
        return False

async def main():
    """Run all tests"""
    
    print("🧪 MongoDB Connection Test Suite")
    print("=" * 50)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run tests
    test_results = []
    
    # Test async connection
    result1 = await test_mongodb_connection()
    test_results.append(("Async MongoDB", result1))
    
    # Test DNS
    result2 = test_dns_resolution()
    test_results.append(("DNS Resolution", result2))
    
    # Test network
    test_network_connectivity()
    
    # Test sync connection
    result3 = test_pymongo_sync()
    test_results.append(("Sync MongoDB", result3))
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    overall = all(result for _, result in test_results)
    print(f"\n🎯 Overall Status: {'✅ HEALTHY' if overall else '❌ ISSUES DETECTED'}")
    
    return overall

if __name__ == "__main__":
    asyncio.run(main())
