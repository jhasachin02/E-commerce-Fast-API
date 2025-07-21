#!/usr/bin/env python3
"""
Test script for deployed Render E-commerce API
Tests all endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime

def test_deployed_api():
    """Test the deployed Render API"""
    
    base_url = "https://e-commerce-fast-api-76pa.onrender.com"
    
    print("🌐 Testing Deployed E-commerce API on Render")
    print("=" * 50)
    print(f"🔗 Base URL: {base_url}")
    print()
    
    # Test results tracking
    results = []
    
    # Test 1: Root endpoint
    print("🧪 Test 1: Root Endpoint")
    print("-" * 25)
    
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📋 Response: {data}")
            results.append(("Root endpoint", True))
        else:
            print(f"❌ Status: {response.status_code}")
            results.append(("Root endpoint", False))
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Root endpoint", False))
    
    print()
    
    # Test 2: Health check
    print("🧪 Test 2: Health Check")
    print("-" * 25)
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"🏥 Health: {data['status']}")
            print(f"💬 Message: {data['message']}")
            results.append(("Health check", True))
        else:
            print(f"❌ Status: {response.status_code}")
            results.append(("Health check", False))
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Health check", False))
    
    print()
    
    # Test 3: Get Products
    print("🧪 Test 3: Get Products")
    print("-" * 25)
    
    try:
        response = requests.get(f"{base_url}/api/v1/products/", timeout=15)
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', [])
            print(f"✅ Status: {response.status_code}")
            print(f"📦 Products found: {len(products)}")
            print(f"📄 Pagination: {data.get('page', {})}")
            
            # Show first few products
            for i, product in enumerate(products[:3]):
                print(f"   {i+1}. {product['name']} - ${product['price']}")
            
            if len(products) > 3:
                print(f"   ... and {len(products) - 3} more products")
            
            results.append(("Get products", True))
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            results.append(("Get products", False))
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Get products", False))
    
    print()
    
    # Test 4: Create Product (POST)
    print("🧪 Test 4: Create Product")
    print("-" * 25)
    
    try:
        test_product = {
            "name": f"Render Test Product - {datetime.now().strftime('%H:%M:%S')}",
            "price": "129.99",
            "sizes": [
                {"size": "M", "quantity": 10},
                {"size": "L", "quantity": 5}
            ]
        }
        
        response = requests.post(
            f"{base_url}/api/v1/products/", 
            json=test_product,
            timeout=15,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"🆕 Created product: {data.get('name')}")
            print(f"🔑 Product ID: {data.get('id')}")
            results.append(("Create product", True))
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"📄 Response: {response.text[:200]}...")
            results.append(("Create product", False))
            
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Create product", False))
    
    print()
    
    # Test 5: API Documentation
    print("🧪 Test 5: API Documentation")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print(f"✅ Status: {response.status_code}")
            print("📚 API documentation is accessible")
            results.append(("API docs", True))
        else:
            print(f"❌ Status: {response.status_code}")
            results.append(("API docs", False))
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("API docs", False))
    
    print()
    
    # Test 6: Response Time Test
    print("🧪 Test 6: Performance Test")
    print("-" * 30)
    
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/api/v1/products/", timeout=15)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        if response.status_code == 200:
            print(f"✅ Status: {response.status_code}")
            print(f"⚡ Response time: {response_time:.2f}ms")
            
            if response_time < 1000:
                print("🚀 Excellent response time!")
            elif response_time < 3000:
                print("👍 Good response time")
            else:
                print("⚠️  Slow response time")
                
            results.append(("Performance", True))
        else:
            print(f"❌ Status: {response.status_code}")
            results.append(("Performance", False))
            
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append(("Performance", False))
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, passed in results if passed)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print()
    print(f"🎯 Overall Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Your API is working perfectly on Render!")
        print("\n💡 Your API endpoints:")
        print(f"   🌐 Root: {base_url}/")
        print(f"   🏥 Health: {base_url}/health")
        print(f"   📦 Products: {base_url}/api/v1/products/")
        print(f"   📚 Docs: {base_url}/docs")
        
    elif passed_tests > total_tests * 0.7:
        print("👍 MOST TESTS PASSED! Your API is mostly working well.")
        
    else:
        print("⚠️  SOME ISSUES DETECTED. Check the failed tests above.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = test_deployed_api()
    if success:
        print("\n🚀 Your E-commerce API is successfully deployed on Render!")
    else:
        print("\n🔧 Some issues need attention.")
