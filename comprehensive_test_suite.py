#!/usr/bin/env python3
"""
Comprehensive Test Suite for E-commerce FastAPI Backend
Tests all functionality: local, database, API endpoints, and deployment
"""

import asyncio
import os
import requests
import json
import sys
from datetime import datetime
from dotenv import load_dotenv

# Configure DNS first
try:
    import dns.resolver
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    print("🔧 DNS configured for testing")
except Exception as e:
    print(f"⚠️  DNS config warning: {e}")

load_dotenv()

class EcommerceTestSuite:
    """Comprehensive test suite for the e-commerce backend"""
    
    def __init__(self):
        self.base_url = "https://e-commerce-fast-api-76pa.onrender.com"
        self.results = []
        
    def log_result(self, test_name, passed, message=""):
        """Log test result"""
        self.results.append((test_name, passed, message))
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
    
    async def test_database_connection(self):
        """Test MongoDB connection with DNS fixes"""
        print("\n🗄️ DATABASE CONNECTION TESTS")
        print("-" * 40)
        
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            from app.database import configure_dns
            
            configure_dns()
            
            mongo_url = os.getenv("MONGODB_URL")
            client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=15000)
            
            # Test ping
            await client.admin.command('ping')
            self.log_result("Database Ping", True, "MongoDB connection successful")
            
            # Test database access
            db = client.ecommerce
            collections = await db.list_collection_names()
            self.log_result("Database Access", True, f"Found {len(collections)} collections")
            
            # Test basic CRUD
            test_collection = db.test_suite
            test_doc = {"test": "comprehensive_test", "timestamp": datetime.now().isoformat()}
            
            # Insert
            result = await test_collection.insert_one(test_doc)
            self.log_result("Database Insert", True, f"Inserted doc ID: {result.inserted_id}")
            
            # Read
            found = await test_collection.find_one({"_id": result.inserted_id})
            self.log_result("Database Read", found is not None, "Document retrieved")
            
            # Update
            await test_collection.update_one(
                {"_id": result.inserted_id},
                {"$set": {"updated": True}}
            )
            updated = await test_collection.find_one({"_id": result.inserted_id})
            self.log_result("Database Update", updated.get("updated") is True, "Document updated")
            
            # Delete
            await test_collection.delete_one({"_id": result.inserted_id})
            deleted = await test_collection.find_one({"_id": result.inserted_id})
            self.log_result("Database Delete", deleted is None, "Document deleted")
            
            client.close()
            
        except Exception as e:
            self.log_result("Database Connection", False, f"Error: {str(e)[:100]}")
    
    def test_api_endpoints(self):
        """Test all API endpoints"""
        print("\n🌐 API ENDPOINT TESTS")
        print("-" * 40)
        
        # Test root endpoint
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            self.log_result("Root Endpoint", response.status_code == 200, 
                           f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Root Endpoint", False, f"Error: {e}")
        
        # Test health endpoint
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                health_ok = data.get('status') == 'healthy'
                self.log_result("Health Check", health_ok, f"Status: {data.get('status')}")
            else:
                self.log_result("Health Check", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Health Check", False, f"Error: {e}")
        
        # Test get products
        try:
            response = requests.get(f"{self.base_url}/api/v1/products/", timeout=15)
            if response.status_code == 200:
                data = response.json()
                products = data.get('data', [])
                self.log_result("Get Products", len(products) > 0, 
                               f"Found {len(products)} products")
            else:
                self.log_result("Get Products", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Get Products", False, f"Error: {e}")
        
        # Test create product
        try:
            test_product = {
                "name": f"Test Suite Product - {datetime.now().strftime('%H:%M:%S')}",
                "price": "199.99",
                "sizes": [{"size": "M", "quantity": 10}]
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/products/",
                json=test_product,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 201:
                data = response.json()
                product_id = data.get('id')
                self.log_result("Create Product", bool(product_id), 
                               f"Created product ID: {product_id}")
            else:
                self.log_result("Create Product", False, 
                               f"Status: {response.status_code}")
        except Exception as e:
            self.log_result("Create Product", False, f"Error: {e}")
        
        # Test API documentation
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=10)
            self.log_result("API Documentation", response.status_code == 200,
                           f"Docs accessible: {response.status_code == 200}")
        except Exception as e:
            self.log_result("API Documentation", False, f"Error: {e}")
    
    async def test_direct_functions(self):
        """Test direct function calls"""
        print("\n🔧 DIRECT FUNCTION TESTS")
        print("-" * 40)
        
        try:
            from app.database import get_collection, configure_dns
            from app.models import ProductCreate, Size
            
            configure_dns()
            
            # Test product creation function
            product = ProductCreate(
                name=f"Direct Function Test - {datetime.now().strftime('%H:%M:%S')}",
                price=299.99,
                sizes=[Size(size="XL", quantity=5)]
            )
            
            collection = await get_collection("products")
            
            # Convert to dict and insert
            product_dict = {
                "name": product.name,
                "price": float(product.price),
                "sizes": [{"size": s.size, "quantity": s.quantity} for s in product.sizes]
            }
            
            result = await collection.insert_one(product_dict)
            self.log_result("Direct Product Insert", bool(result.inserted_id),
                           f"Inserted ID: {result.inserted_id}")
            
            # Test retrieval
            found = await collection.find_one({"_id": result.inserted_id})
            self.log_result("Direct Product Retrieve", found is not None,
                           f"Retrieved: {found['name'] if found else 'None'}")
            
        except Exception as e:
            self.log_result("Direct Functions", False, f"Error: {str(e)[:100]}")
    
    def test_performance(self):
        """Test API performance"""
        print("\n⚡ PERFORMANCE TESTS")
        print("-" * 40)
        
        import time
        
        # Test response times
        endpoints = [
            ("/", "Root"),
            ("/health", "Health"),
            ("/api/v1/products/", "Products")
        ]
        
        for endpoint, name in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=15)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # ms
                
                # Consider under 2 seconds as acceptable
                performance_ok = response_time < 2000
                self.log_result(f"{name} Performance", performance_ok,
                               f"{response_time:.0f}ms")
                
            except Exception as e:
                self.log_result(f"{name} Performance", False, f"Error: {e}")
    
    def test_data_validation(self):
        """Test input validation"""
        print("\n🔍 DATA VALIDATION TESTS")
        print("-" * 40)
        
        # Test invalid product data
        invalid_products = [
            {"name": "", "price": "100", "sizes": []},  # Empty name, no sizes
            {"name": "Test", "price": "-50", "sizes": [{"size": "M", "quantity": 1}]},  # Negative price
            {"name": "Test", "price": "100", "sizes": [{"size": "", "quantity": -1}]}  # Invalid size
        ]
        
        for i, invalid_product in enumerate(invalid_products):
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/products/",
                    json=invalid_product,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                # Should return 422 for validation errors
                validation_ok = response.status_code == 422
                self.log_result(f"Validation Test {i+1}", validation_ok,
                               f"Status: {response.status_code}")
                
            except Exception as e:
                self.log_result(f"Validation Test {i+1}", False, f"Error: {e}")
    
    async def run_all_tests(self):
        """Run all test suites"""
        print("🧪 COMPREHENSIVE E-COMMERCE API TEST SUITE")
        print("=" * 50)
        print(f"🎯 Target: {self.base_url}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all test suites
        await self.test_database_connection()
        self.test_api_endpoints()
        await self.test_direct_functions()
        self.test_performance()
        self.test_data_validation()
        
        # Summary
        print("\n📊 TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for _, success, _ in self.results if success)
        total = len(self.results)
        
        for test_name, success, message in self.results:
            status = "✅" if success else "❌"
            print(f"{status} {test_name:<25} {message}")
        
        print(f"\n🎯 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Your API is production ready!")
        elif passed > total * 0.8:
            print("👍 MOST TESTS PASSED! Minor issues to address.")
        else:
            print("⚠️  SEVERAL ISSUES DETECTED. Review failed tests.")
        
        return passed == total

async def main():
    """Run the comprehensive test suite"""
    test_suite = EcommerceTestSuite()
    success = await test_suite.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
