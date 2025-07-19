from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Annotated
from bson import ObjectId
from decimal import Decimal

# Simple string type for ObjectId to avoid OpenAPI issues
ObjectIdStr = Annotated[str, Field(min_length=24, max_length=24, description="MongoDB ObjectId as string")]

class Size(BaseModel):
    """Model for product sizes"""
    size: str = Field(..., min_length=1, max_length=10, description="Product size (e.g., 'S', 'M', 'L', 'XL')")
    quantity: int = Field(..., ge=0, le=10000, description="Available quantity for this size")

class ProductCreate(BaseModel):
    """Model for POST /products request body"""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Product price")
    sizes: List[Size] = Field(..., min_items=1, max_items=50, description="Available sizes and quantities")

class ProductResponse(BaseModel):
    """Model for GET /products response data items"""
    id: ObjectIdStr = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    price: Decimal = Field(..., description="Product price")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class ProductInDB(BaseModel):
    """Model for storing in MongoDB"""
    id: ObjectIdStr = Field(..., description="Product ID")
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Product price")
    sizes: List[Size] = Field(..., min_items=1, max_items=50, description="Available sizes and quantities")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class Page(BaseModel):
    """Model for pagination metadata"""
    next: Optional[str] = Field(None, max_length=50, description="Next page cursor")
    limit: int = Field(..., gt=0, le=1000, description="Number of items per page")
    previous: Optional[str] = Field(None, max_length=50, description="Previous page cursor")

class ListProductsResponse(BaseModel):
    """Model for the full GET /products response"""
    data: List[ProductResponse] = Field(..., description="List of products")
    page: Page = Field(..., description="Pagination metadata")

# Order-related models
class OrderItem(BaseModel):
    """Model for individual items in an order"""
    productId: str = Field(..., min_length=24, max_length=24, description="Product ID (24-character ObjectId)")
    qty: int = Field(..., gt=0, le=1000, description="Quantity of the product")

class OrderCreate(BaseModel):
    """Model for POST /orders request body"""
    userId: str = Field(..., min_length=1, max_length=100, description="User ID")
    items: List[OrderItem] = Field(..., min_items=1, max_items=100, description="List of order items")

class ProductDetailsInOrder(BaseModel):
    """Model for nested product details when listing orders"""
    id: str = Field(..., min_length=24, max_length=24, description="Product ID")
    name: str = Field(..., min_length=1, max_length=200, description="Product name")

class OrderItemWithProductDetails(BaseModel):
    """Model for items in the GET /orders response"""
    productDetails: ProductDetailsInOrder = Field(..., description="Product details")
    qty: int = Field(..., gt=0, le=1000, description="Quantity of the product")

class OrderResponse(BaseModel):
    """Model for the GET /orders response data items"""
    id: ObjectIdStr = Field(..., description="Order ID")
    userId: str = Field(..., min_length=1, max_length=100, description="User ID")
    items: List[OrderItemWithProductDetails] = Field(..., min_items=1, description="Order items with product details")
    total: Decimal = Field(..., ge=0, decimal_places=2, description="Total order amount")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class ListOrdersResponse(BaseModel):
    """Model for the full GET /orders response"""
    data: List[OrderResponse] = Field(..., description="List of orders")
    page: Page = Field(..., description="Pagination metadata") 