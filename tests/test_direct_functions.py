#!/usr/bin/env python3
"""
Direct test of the product creation function
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

async def test_product_creation():
    """Test product creation directly"""
    
    print("🧪 Testing Product Creation Function")
    print("=" * 40)
    
    try:
        # Import the fixed database function
        from app.database import get_collection, configure_dns
        from app.models import ProductCreate, Size
        
        # Configure DNS first
        configure_dns()
        
        # Test data
        product = ProductCreate(
            name="Direct Test Product",
            price=199.99,
            sizes=[Size(size="L", quantity=8)]
        )
        
        print(f"📊 Creating product: {product.name}")
        
        # Get collection (this should work now)
        collection = await get_collection("products")
        print("✅ Collection obtained successfully")
        
        # Create document for MongoDB insertion
        product_data = {
            "name": product.name,
            "price": float(product.price),  # Convert Decimal to float
            "sizes": [size.model_dump() for size in product.sizes]  # Use model_dump
        }
        
        print(f"📊 Product data: {product_data}")
        
        # Insert the product
        result = await collection.insert_one(product_data)
        print(f"✅ Product created successfully!")
        print(f"🆔 Product ID: {result.inserted_id}")
        
        # Verify the product was created
        created_product = await collection.find_one({"_id": result.inserted_id})
        print(f"✅ Verification: {created_product}")
        
        return str(result.inserted_id)
        
    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        return None

async def test_get_products():
    """Test getting products"""
    
    print("\n🧪 Testing Get Products Function")
    print("=" * 35)
    
    try:
        from app.database import get_collection
        
        collection = await get_collection("products")
        
        # Count products
        count = await collection.count_documents({})
        print(f"📊 Total products: {count}")
        
        # List first few products
        products = []
        async for product in collection.find({}).limit(3):
            products.append(product)
            
        print(f"✅ Sample products: {len(products)}")
        for product in products:
            print(f"   - {product['name']}: ${product['price']}")
            
    except Exception as e:
        print(f"❌ Error getting products: {e}")

async def main():
    """Run tests"""
    
    print("🚀 Direct Function Testing")
    print("=" * 50)
    
    # Test 1: Create product
    product_id = await test_product_creation()
    
    # Test 2: Get products
    await test_get_products()
    
    if product_id:
        print(f"\n🎉 SUCCESS! Product creation is working!")
        print(f"📦 Created product ID: {product_id}")
    else:
        print(f"\n❌ Product creation failed")
    
    return product_id is not None

if __name__ == "__main__":
    result = asyncio.run(main())
