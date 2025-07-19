from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from bson import ObjectId

from app.database import get_collection
from app.models import (
    ProductCreate, 
    ProductResponse, 
    ProductInDB, 
    ListProductsResponse, 
    Page,
    Size
)

router = APIRouter()

# Product endpoints
@router.get("/", response_model=ListProductsResponse)
async def get_products(
    name: Optional[str] = Query(None, description="Product name for partial search (case-insensitive)"),
    size: Optional[str] = Query(None, description="Filter products that have this size"),
    limit: int = Query(10, ge=1, le=100, description="Number of documents to return"),
    offset: int = Query(0, ge=0, description="Number of documents to skip for pagination")
):
    """
    Get all products with filtering and pagination.
    
    Args:
        name: Optional regex/partial search for product name (case-insensitive)
        size: Optional filter for products with specific size
        limit: Number of documents to return
        offset: Number of documents to skip for pagination
        
    Returns:
        ListProductsResponse containing data (list of products with id, name, price) 
        and pagination metadata
        
    Raises:
        HTTPException: If database operation fails
    """
    try:
        collection = get_collection("products")
        
        # Build query
        query = {}
        
        # Add name filter (case-insensitive regex search)
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        
        # Add size filter for products that have this specific size
        if size:
            query["sizes.size"] = size
        
        # Get total count for pagination
        total_count = await collection.count_documents(query)
        
        # Project only the required fields (_id, name, price) for efficiency
        projection = {
            "_id": 1,
            "name": 1,
            "price": 1
        }
        
        # Get products with sorting by _id and pagination
        products = []
        async for product in collection.find(query, projection).sort("_id", 1).skip(offset).limit(limit):
            # Create ProductResponse with only id, name, price (no sizes)
            product_response = ProductResponse(
                id=str(product["_id"]),
                name=product["name"],
                price=product["price"]
            )
            products.append(product_response)
        
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
        
        return ListProductsResponse(data=products, page=page)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch products"
        )

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """
    Get a specific product by ID.
    """
    collection = get_collection("products")
    
    try:
        product = await collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Return only the required fields for ProductResponse
        return ProductResponse(
            id=str(product["_id"]),
            name=product["name"],
            price=product["price"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """
    Create a new product.
    
    Args:
        product: Product creation data using ProductCreate model
        
    Returns:
        Dictionary containing the created product ID
        
    Raises:
        HTTPException: If database operation fails
    """
    try:
        collection = get_collection("products")
        
        # Convert to ProductInDB for storage
        product_in_db = ProductInDB(
            name=product.name,
            price=product.price,
            sizes=product.sizes
        )
        
        # Convert to dict for MongoDB insertion
        product_data = product_in_db.dict(by_alias=True)
        
        # Insert the product data into the 'products' collection
        result = await collection.insert_one(product_data)
        
        # Return the string representation of the newly created MongoDB document's _id
        return {"id": str(result.inserted_id)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )

 