#!/usr/bin/env python3
"""
Local Application Test
Tests the locally running FastAPI application
"""

import requests
import json
from datetime import datetime

def test_local_app():
    """Test the locally running application"""
    
    base_url = "http://localhost:8000"
    
    print("🏠 TESTING LOCAL APPLICATION")
    print("=" * 40)
    print(f"🔗 Base URL: {base_url}")
    print()
    
    results = []
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root: {data['message']}")
            results.append(True)
        else:
            print(f"❌ Root failed: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"❌ Root error: {e}")
        results.append(False)
    
    # Test 2: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health: {data['status']}")
            results.append(True)
        else:
            print(f"❌ Health failed: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"❌ Health error: {e}")
        results.append(False)
    
    # Test 3: Products endpoint (tests MongoDB connection)
    try:
        response = requests.get(f"{base_url}/api/v1/products/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', [])
            print(f"✅ Products: Found {len(products)} products")
            results.append(True)
        else:
            print(f"❌ Products failed: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"❌ Products error: {e}")
        results.append(False)
    
    # Test 4: Create product (tests full CRUD)
    try:
        test_product = {
            "name": f"Local Test Product - {datetime.now().strftime('%H:%M:%S')}",
            "price": "149.99",
            "sizes": [{"size": "S", "quantity": 5}]
        }
        
        response = requests.post(
            f"{base_url}/api/v1/products/",
            json=test_product,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Create Product: ID {data.get('id')}")
            results.append(True)
        else:
            print(f"❌ Create Product failed: {response.status_code}")
            results.append(False)
    except Exception as e:
        print(f"❌ Create Product error: {e}")
        results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Local Tests: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 Local application working perfectly!")
    else:
        print("⚠️  Some local tests failed")
    
    return passed == total

if __name__ == "__main__":
    test_local_app()
