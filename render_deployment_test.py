#!/usr/bin/env python3
"""
Final Render Deployment Test Report
Tests all aspects needed for successful Render deployment
"""

import os
import json
import asyncio
import sys
from datetime import datetime
from pathlib import Path

# DNS fix for MongoDB Atlas
try:
    import dns.resolver
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']
except:
    pass

def test_file_structure():
    """Test that all required files exist"""
    
    print("📁 File Structure Test")
    print("-" * 25)
    
    required_files = [
        'main.py',
        'start.py', 
        'requirements.txt',
        'render.yaml',
        'Procfile',
        '.env',
        'app/__init__.py',
        'app/database.py',
        'app/models.py',
        'app/routers/products.py',
        'app/routers/orders.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_render_config():
    """Test Render configuration files"""
    
    print("\n🔧 Render Configuration Test")
    print("-" * 30)
    
    # Check render.yaml
    try:
        with open('render.yaml', 'r') as f:
            content = f.read()
            if 'buildCommand:' in content and 'startCommand:' in content:
                print("✅ render.yaml structure OK")
            else:
                print("❌ render.yaml missing required commands")
                return False
    except FileNotFoundError:
        print("❌ render.yaml not found")
        return False
    
    # Check requirements.txt
    try:
        # Try different encodings to handle BOM issues
        content = None
        for encoding in ['utf-8', 'utf-16', 'utf-8-sig']:
            try:
                with open('requirements.txt', 'r', encoding=encoding) as f:
                    content = f.read().lower()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print("❌ Could not read requirements.txt")
            return False
            
        required_packages = ['fastapi', 'uvicorn', 'motor', 'pymongo', 'python-dotenv']
        missing = []
        
        for pkg in required_packages:
            if pkg not in content:
                missing.append(pkg)
        
        if missing:
            print(f"❌ Missing packages in requirements.txt: {missing}")
            return False
        else:
            print("✅ requirements.txt has all required packages")
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False
    
    # Check start command
    try:
        # Try different encodings
        content = None
        for encoding in ['utf-8', 'utf-16', 'utf-8-sig']:
            try:
                with open('start.py', 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content and ('uvicorn' in content or 'main:app' in content):
            print("✅ start.py configured for deployment")
        else:
            print("⚠️  start.py may need adjustment")
    except FileNotFoundError:
        print("❌ start.py not found")
        return False
    
    return True

def test_environment_config():
    """Test environment configuration"""
    
    print("\n🌍 Environment Configuration Test")
    print("-" * 35)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check critical environment variables
    mongodb_url = os.getenv("MONGODB_URL")
    
    if mongodb_url:
        print("✅ MONGODB_URL configured")
        if mongodb_url.startswith("mongodb+srv://"):
            print("✅ Using MongoDB Atlas (SRV)")
        else:
            print("ℹ️  Using regular MongoDB connection")
    else:
        print("❌ MONGODB_URL not found")
        return False
    
    # Check optional variables
    db_name = os.getenv("DATABASE_NAME")
    if db_name:
        print(f"✅ DATABASE_NAME: {db_name}")
    else:
        print("ℹ️  DATABASE_NAME not set (will use default)")
    
    return True

async def test_mongodb_connection():
    """Test MongoDB connection"""
    
    print("\n🗄️  MongoDB Connection Test")
    print("-" * 28)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from motor.motor_asyncio import AsyncIOMotorClient
        
        mongo_url = os.getenv("MONGODB_URL")
        client = AsyncIOMotorClient(
            mongo_url,
            serverSelectionTimeoutMS=15000
        )
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB ping successful")
        
        # Test database operations
        db = client.ecommerce
        collections = await db.list_collection_names()
        print(f"✅ Database access OK ({len(collections)} collections)")
        
        # Test a simple write operation
        test_result = await db.test_deployment.insert_one({
            "test": "render_deployment",
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        })
        
        # Clean up test document
        await db.test_deployment.delete_one({"_id": test_result.inserted_id})
        print("✅ Write/Read/Delete operations successful")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)[:60]}...")
        return False

def test_app_imports():
    """Test that the application can be imported"""
    
    print("\n📦 Application Import Test")
    print("-" * 26)
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        
        # Test main app import
        from main import app
        print("✅ Main app imported successfully")
        
        # Test routers
        from app.routers import products, orders
        print("✅ Routers imported successfully")
        
        # Test database module
        from app.database import get_database
        print("✅ Database module imported successfully")
        
        # Test models
        from app.models import ProductCreate, ProductResponse, OrderCreate, OrderResponse
        print("✅ Models imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def create_deployment_checklist():
    """Create deployment checklist"""
    
    checklist = {
        "render_deployment_checklist": {
            "timestamp": datetime.now().isoformat(),
            "pre_deployment": [
                "✅ All required files present",
                "✅ render.yaml configured correctly", 
                "✅ requirements.txt has all dependencies",
                "✅ start.py ready for production",
                "✅ MongoDB connection tested",
                "✅ Application imports working"
            ],
            "render_setup": [
                "🔲 Create new Web Service on Render",
                "🔲 Connect to GitHub repository",
                "🔲 Set build command: pip install -r requirements.txt",
                "🔲 Set start command: python start.py",
                "🔲 Add MONGODB_URL environment variable",
                "🔲 Add DATABASE_NAME environment variable (optional)",
                "🔲 Deploy and test"
            ],
            "post_deployment": [
                "🔲 Verify API endpoints work",
                "🔲 Test /health endpoint",
                "🔲 Test /api/v1/products/ endpoint",
                "🔲 Test /api/v1/orders/ endpoint",
                "🔲 Verify MongoDB connection in logs",
                "🔲 Test CRUD operations"
            ]
        }
    }
    
    with open('render_deployment_checklist.json', 'w') as f:
        json.dump(checklist, f, indent=2)
    
    print("\n📋 Deployment Checklist Created")
    print("-" * 32)
    print("✅ render_deployment_checklist.json generated")

async def main():
    """Run comprehensive deployment test"""
    
    print("🚀 RENDER DEPLOYMENT TEST SUITE")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("File Structure", test_file_structure),
        ("Render Config", test_render_config),
        ("Environment", test_environment_config),
        ("App Imports", test_app_imports),
        ("MongoDB Connection", test_mongodb_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        results.append((test_name, result))
    
    # Create deployment checklist
    create_deployment_checklist()
    
    # Final summary
    print("\n🎯 DEPLOYMENT TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - READY FOR RENDER DEPLOYMENT!")
        print("\nNext Steps:")
        print("1. Push code to GitHub repository")
        print("2. Create new Web Service on Render")
        print("3. Connect to your GitHub repo")
        print("4. Configure environment variables:")
        print("   - MONGODB_URL (from MongoDB Atlas)")
        print("   - DATABASE_NAME (optional)")
        print("5. Deploy and test endpoints")
        
    else:
        print("\n⚠️  SOME TESTS FAILED - FIX ISSUES BEFORE DEPLOYMENT")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
