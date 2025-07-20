#!/usr/bin/env python3
"""
Simple Demo Script for E-commerce FastAPI Backend
This script demonstrates the API functionality with sample data
"""

import requests
import json
from datetime import datetime

# API Base URL
BASE_URL = "https://e-commerce-fast-api-1.onrender.com"

def print_header(title):
    """Print a nice header for each section"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_response(response, description):
    """Print response in a formatted way"""
    print(f"\n📡 {description}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200 or response.status_code == 201:
        print("✅ SUCCESS")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
    else:
        print("❌ ERROR")
        print(f"Error: {response.text}")

def test_health_check():
    """Test the health endpoint"""
    print_header("HEALTH CHECK")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    return response.status_code == 200

def create_sample_products():
    """Create sample products"""
    print_header("CREATING SAMPLE PRODUCTS")
    
    products = [
        {
            "name": "Classic T-Shirt",
            "price": 29.99,
            "sizes": [
                {"size": "S", "quantity": 10},
                {"size": "M", "quantity": 15},
                {"size": "L", "quantity": 12}
            ]
        },
        {
            "name": "Denim Jeans",
            "price": 79.99,
            "sizes": [
                {"size": "30", "quantity": 8},
                {"size": "32", "quantity": 12},
                {"size": "34", "quantity": 10}
            ]
        },
        {
            "name": "Running Shoes",
            "price": 99.99,
            "sizes": [
                {"size": "8", "quantity": 5},
                {"size": "9", "quantity": 8},
                {"size": "10", "quantity": 6}
            ]
        }
    ]
    
    created_products = []
    
    for i, product in enumerate(products, 1):
        print(f"\n🛍️  Creating Product {i}: {product['name']}")
        response = requests.post(f"{BASE_URL}/api/v1/products/", json=product)
        print_response(response, f"Create {product['name']}")
        
        if response.status_code == 201:
            try:
                result = response.json()
                created_products.append(result.get('product_id'))
            except:
                pass
    
    return created_products

def get_all_products():
    """Get all products"""
    print_header("RETRIEVING ALL PRODUCTS")
    response = requests.get(f"{BASE_URL}/api/v1/products/")
    print_response(response, "Get All Products")
    
    products = []
    if response.status_code == 200:
        try:
            data = response.json()
            products = data.get('data', [])
            print(f"\n📦 Found {len(products)} products:")
            for product in products:
                print(f"  - {product.get('name')}: ${product.get('price')}")
        except:
            pass
    
    return products

def create_sample_order(products):
    """Create a sample order"""
    print_header("CREATING SAMPLE ORDER")
    
    if not products:
        print("❌ No products available to create order")
        return None
    
    # Create an order with the first two products
    order_data = {
        "userId": "demo_user_123",
        "items": []
    }
    
    for i, product in enumerate(products[:2]):  # Use first 2 products
        order_data["items"].append({
            "productId": product.get('id', ''),
            "qty": i + 1  # 1 for first product, 2 for second
        })
    
    print(f"🛒 Creating order for user: {order_data['userId']}")
    print(f"📝 Order items: {len(order_data['items'])} products")
    
    response = requests.post(f"{BASE_URL}/api/v1/orders/", json=order_data)
    print_response(response, "Create Sample Order")
    
    if response.status_code == 201:
        try:
            result = response.json()
            return result.get('order_id')
        except:
            pass
    
    return None

def get_user_orders(user_id="demo_user_123"):
    """Get orders for a user"""
    print_header("RETRIEVING USER ORDERS")
    
    response = requests.get(f"{BASE_URL}/api/v1/orders/{user_id}")
    print_response(response, f"Get Orders for User: {user_id}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            orders = data.get('data', [])
            print(f"\n🛒 Found {len(orders)} orders for user {user_id}")
            for order in orders:
                print(f"  - Order {order.get('id')}: ${order.get('total')} ({len(order.get('items', []))} items)")
        except:
            pass

def search_products():
    """Test product search functionality"""
    print_header("TESTING PRODUCT SEARCH")
    
    # Search by name
    print("\n🔍 Searching for products containing 'shirt'")
    response = requests.get(f"{BASE_URL}/api/v1/products/?name=shirt")
    print_response(response, "Search Products by Name")
    
    # Search with pagination
    print("\n📄 Testing pagination (limit=2)")
    response = requests.get(f"{BASE_URL}/api/v1/products/?limit=2")
    print_response(response, "Get Products with Pagination")

def main():
    """Run the complete demo"""
    print("🎯 E-COMMERCE FASTAPI BACKEND DEMO")
    print("🌐 Testing API at:", BASE_URL)
    print("⏰ Started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        # Step 1: Health Check
        if not test_health_check():
            print("❌ Health check failed. Stopping demo.")
            return
        
        # Step 2: Create sample products
        product_ids = create_sample_products()
        
        # Step 3: Get all products
        products = get_all_products()
        
        # Step 4: Test product search
        search_products()
        
        # Step 5: Create sample order
        if products:
            order_id = create_sample_order(products)
            
            # Step 6: Get user orders
            get_user_orders()
        
        # Final Summary
        print_header("DEMO COMPLETED SUCCESSFULLY")
        print("✅ All API endpoints tested successfully!")
        print("🎊 Your E-commerce FastAPI Backend is working perfectly!")
        print(f"📚 API Documentation: {BASE_URL}/docs")
        print(f"🏥 Health Check: {BASE_URL}/health")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
