#!/usr/bin/env python3
"""
Test script to demonstrate product creation API endpoint
Shows the exact input/output format
"""

import requests
import json

def test_create_product_api():
    """Test the product creation endpoint"""
    
    # API endpoint
    url = "https://e-commerce-fast-api-1.onrender.com/api/v1/products/"
    
    # Input data (exactly as you requested)
    input_data = {
        "name": "Sample T-Shirt",
        "price": 100.0,
        "sizes": [
            {
                "size": "M",
                "quantity": 15
            }
        ]
    }
    
    print("🚀 Testing Product Creation API")
    print("=" * 50)
    print(f"📍 Endpoint: {url}")
    print(f"📤 Input:")
    print(json.dumps(input_data, indent=2))
    print("-" * 50)
    
    try:
        # Make POST request
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=input_data, headers=headers)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Success!")
            print(f"📤 Output:")
            print(json.dumps(result, indent=2))
            print(f"🆔 Created Product ID: {result['id']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📤 Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_alternative_api():
    """Test with Railway deployment"""
    
    # Alternative API endpoint
    url = "https://web-production-5d772.up.railway.app/api/v1/products/"
    
    # Input data
    input_data = {
        "name": "Alternative Product",
        "price": 100.0,
        "sizes": [
            {
                "size": "L", 
                "quantity": 20
            }
        ]
    }
    
    print("\n🚀 Testing Alternative API (Railway)")
    print("=" * 50)
    print(f"📍 Endpoint: {url}")
    print(f"📤 Input:")
    print(json.dumps(input_data, indent=2))
    print("-" * 50)
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=input_data, headers=headers)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Success!")
            print(f"📤 Output:")
            print(json.dumps(result, indent=2))
            print(f"🆔 Created Product ID: {result['id']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📤 Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_create_product_api()
    test_alternative_api()
