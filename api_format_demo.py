#!/usr/bin/env python3
"""
Demo script showing EXACT input/output format for product creation
This demonstrates the API behavior without needing MongoDB
"""

def show_api_format():
    """Show the exact API input/output format"""
    
    print("🚀 E-Commerce FastAPI - Product Creation Demo")
    print("=" * 55)
    
    # Exact input format
    input_example = {
        "name": "Classic T-Shirt",
        "price": 100.0,
        "sizes": [
            {
                "size": "M",
                "quantity": 15
            }
        ]
    }
    
    # Exact output format (what you get back)
    output_example = {
        "id": "676d0f8b12a1b23c4d567890"  # MongoDB ObjectId as string
    }
    
    print("📤 INPUT FORMAT:")
    print("POST /api/v1/products/")
    print("Content-Type: application/json")
    print()
    import json
    print(json.dumps(input_example, indent=2))
    
    print("\n📤 OUTPUT FORMAT:")
    print("Status: 201 Created")
    print("Content-Type: application/json")
    print()
    print(json.dumps(output_example, indent=2))
    
    print("\n✅ RESPONSE DETAILS:")
    print(f"• Status Code: 201 (Created)")
    print(f"• Response Body: JSON object with 'id' field")
    print(f"• ID Format: 24-character MongoDB ObjectId as string")
    print(f"• Example ID: {output_example['id']}")
    
    print("\n🔗 ENDPOINT URLs:")
    print("• Render:  https://e-commerce-fast-api-1.onrender.com/api/v1/products/")
    print("• Railway: https://web-production-5d772.up.railway.app/api/v1/products/")
    
    print("\n📝 CURL EXAMPLE:")
    curl_command = f"""curl -X POST https://e-commerce-fast-api-1.onrender.com/api/v1/products/ \\
  -H "Content-Type: application/json" \\
  -d '{json.dumps(input_example)}'"""
    print(curl_command)
    
    print("\n🎯 POWERSHELL EXAMPLE:")
    powershell_command = f"""Invoke-RestMethod -Uri "https://e-commerce-fast-api-1.onrender.com/api/v1/products/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{json.dumps(input_example)}'"""
    print(powershell_command)
    
    print("\n🔧 FIELD SPECIFICATIONS:")
    print("• name: string (1-200 chars, required)")
    print("• price: decimal (> 0, 2 decimal places, required)")
    print("• sizes: array (1-50 items, required)")
    print("  └─ size: string (1-10 chars, e.g., 'S', 'M', 'L')")
    print("  └─ quantity: integer (0-10000, available stock)")
    
    print("\n🎉 THIS IS EXACTLY WHAT YOUR API RETURNS!")

if __name__ == "__main__":
    show_api_format()
