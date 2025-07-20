from fastapi import APIRouter, HTTPException, status, Query, Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError
from bson import ObjectId, errors as bson_errors
from datetime import datetime
import logging

from app.database import get_collection
from app.models import (
    OrderCreate, 
    OrderResponse, 
    ListOrdersResponse, 
    Page,
    ProductDetailsInOrder,
    OrderItemWithProductDetails
)

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Custom exceptions
class OrderNotFoundError(HTTPException):
    def __init__(self, order_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )

class ProductNotFoundError(HTTPException):
    def __init__(self, product_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )

class InvalidObjectIdError(HTTPException):
    def __init__(self, field_name: str, value: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name} format: {value}"
        )

# Helper functions
def validate_object_id(object_id: str, field_name: str = "ID") -> ObjectId:
    """Validate and convert string to ObjectId"""
    try:
        return ObjectId(object_id)
    except (bson_errors.InvalidId, TypeError):
        raise InvalidObjectIdError(field_name, object_id)

async def fetch_product_details_batch(product_ids: List[str]) -> Dict[str, ProductDetailsInOrder]:
    """Fetch multiple product details in a single query for efficiency"""
    try:
        products_collection = await get_collection("products")
        
        # Convert string IDs to ObjectIds
        object_ids = []
        for product_id in product_ids:
            try:
                object_ids.append(ObjectId(product_id))
            except (bson_errors.InvalidId, TypeError):
                continue
        
        if not object_ids:
            return {}
        
        # Batch query with projection for efficiency
        projection = {"_id": 1, "name": 1}
        products = {}
        
        async for product in products_collection.find(
            {"_id": {"$in": object_ids}}, 
            projection
        ):
            products[str(product["_id"])] = ProductDetailsInOrder(
                id=str(product["_id"]),
                name=product["name"]
            )
        
        return products
    except Exception as e:
        logger.error(f"Error fetching product details batch: {str(e)}")
        return {}

async def fetch_product_details(product_id: str) -> Optional[ProductDetailsInOrder]:
    """Fetch single product details from database"""
    try:
        products_collection = await get_collection("products")
        product = await products_collection.find_one(
            {"_id": validate_object_id(product_id, "product ID")},
            {"_id": 1, "name": 1}  # Projection for efficiency
        )
        
        if product:
            return ProductDetailsInOrder(
                id=product_id,
                name=product["name"]
            )
        return None
    except InvalidObjectIdError:
        return None

async def calculate_order_total(items: List[Dict[str, Any]]) -> float:
    """Calculate total order amount"""
    total = 0.0
    for item in items:
        total += item["price"] * item["qty"]
    return round(total, 2)

# Order endpoints
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate) -> Dict[str, str]:
    """
    Create a new order.
    
    Args:
        order: Order creation data using OrderCreate model
        
    Returns:
        Dictionary containing the created order ID
        
    Raises:
        ProductNotFoundError: If any product in the order doesn't exist
        InvalidObjectIdError: If any product ID is invalid
    """
    try:
        orders_collection = await get_collection("orders")
        products_collection = await get_collection("products")
        
        # Calculate total price by fetching product prices
        order_items = []
        
        for item in order.items:
            # Validate product ID and fetch product details (especially price)
            try:
                product_id = validate_object_id(item.productId, "product ID")
                product = await products_collection.find_one({"_id": product_id})
                
                if not product:
                    raise ProductNotFoundError(item.productId)
                
                # Store order item with product details including price
                order_items.append({
                    "productId": item.productId,
                    "qty": item.qty,
                    "price": product["price"]  # Lookup product price for total calculation
                })
                
            except InvalidObjectIdError:
                raise ProductNotFoundError(item.productId)
        
        # Calculate total price for the entire order
        total = await calculate_order_total(order_items)
        
        # Create order document with hardcoded userId
        order_data = {
            "userId": "user_1",  # Hardcoded userId as specified
            "items": order_items,
            "total": total,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Store the order data in the 'orders' collection
        result = await orders_collection.insert_one(order_data)
        
        logger.info(f"Order created successfully: {result.inserted_id}")
        
        # Return the string representation of the newly created MongoDB document's _id
        return {"id": str(result.inserted_id)}
        
    except (ProductNotFoundError, InvalidObjectIdError):
        raise
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

@router.get("/order/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str = Path(..., description="Order ID")):
    """
    Get a specific order by ID.
    
    Args:
        order_id: The order ID to retrieve
        
    Returns:
        OrderResponse with complete order details
        
    Raises:
        OrderNotFoundError: If order doesn't exist
        InvalidObjectIdError: If order ID is invalid
    """
    try:
        collection = await get_collection("orders")
        
        # Validate order ID and fetch order
        order_object_id = validate_object_id(order_id, "order ID")
        order = await collection.find_one({"_id": order_object_id})
        
        if not order:
            raise OrderNotFoundError(order_id)
        
        # Convert order items to include product details
        items_with_details = []
        
        for item in order["items"]:
            # Fetch product details
            product_details = await fetch_product_details(item["productId"])
            
            if product_details:
                # Create order item with product details
                order_item = OrderItemWithProductDetails(
                    productDetails=product_details,
                    qty=item["qty"]
                )
                items_with_details.append(order_item)
            else:
                # Handle case where product no longer exists
                logger.warning(f"Product {item['productId']} not found for order {order_id}")
                # Create placeholder product details
                product_details = ProductDetailsInOrder(
                    id=item["productId"],
                    name="Product Not Available"
                )
                order_item = OrderItemWithProductDetails(
                    productDetails=product_details,
                    qty=item["qty"]
                )
                items_with_details.append(order_item)
        
        # Create OrderResponse
        return OrderResponse(
            id=str(order["_id"]),
            userId=order["userId"],
            items=items_with_details,
            total=order["total"]
        )
        
    except (OrderNotFoundError, InvalidObjectIdError):
        raise
    except Exception as e:
        logger.error(f"Error fetching order {order_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch order"
        )

@router.get("/{user_id}", response_model=ListOrdersResponse)
async def get_orders_by_user(
    user_id: str = Path(..., description="User ID"),
    limit: int = Query(10, ge=1, le=100, description="Number of documents to return"),
    offset: int = Query(0, ge=0, description="Number of documents to skip for pagination")
) -> ListOrdersResponse:
    """
    Get all orders for a specific user with pagination.
    
    Args:
        user_id: The user ID to filter orders by (URL parameter)
        limit: Number of documents to return (1-100)
        offset: Number of documents to skip for pagination
        
    Returns:
        ListOrdersResponse containing data (list of order details with productDetails) 
        and pagination metadata
        
    Raises:
        HTTPException: If database operation fails
    """
    try:
        orders_collection = await get_collection("orders")
        products_collection = await get_collection("products")
        
        # Query the 'orders' collection, filtering by user_id
        query = {"userId": user_id}
        
        # Get total count for pagination
        total_count = await orders_collection.count_documents(query)
        
        # Get orders with sorting by _id and pagination
        orders = []
        async for order in orders_collection.find(query).sort("_id", 1).skip(offset).limit(limit):
            # Process each order item to include product details
            items_with_details = []
            
            for item in order["items"]:
                # Perform a lookup/join to get the productDetails from the 'products' collection
                product_details = await fetch_product_details(item["productId"])
                
                if product_details:
                    # Create order item with product details (id and name)
                    order_item = OrderItemWithProductDetails(
                        productDetails=product_details,
                        qty=item["qty"]
                    )
                    items_with_details.append(order_item)
                else:
                    # Handle missing products gracefully
                    logger.warning(f"Product {item['productId']} not found for order {order['_id']}")
                    # Create placeholder product details
                    product_details = ProductDetailsInOrder(
                        id=item["productId"],
                        name="Product Not Available"
                    )
                    order_item = OrderItemWithProductDetails(
                        productDetails=product_details,
                        qty=item["qty"]
                    )
                    items_with_details.append(order_item)
            
            # Create OrderResponse with complete order details
            order_response = OrderResponse(
                id=str(order["_id"]),
                userId=order["userId"],
                items=items_with_details,  # Each item includes productDetails joined from products collection
                total=order["total"]
            )
            orders.append(order_response)
        
        # Calculate pagination metadata
        has_next = offset + limit < total_count
        has_previous = offset > 0
        
        next_offset = offset + limit if has_next else None
        previous_offset = offset - limit if has_previous else None
        
        page = Page(
            next=str(next_offset) if has_next else None,
            limit=limit,
            previous=str(previous_offset) if has_previous else None
        )
        
        logger.info(f"Retrieved {len(orders)} orders for user {user_id}")
        
        return ListOrdersResponse(data=orders, page=page)
        
    except Exception as e:
        logger.error(f"Error fetching orders for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch orders"
        )

 