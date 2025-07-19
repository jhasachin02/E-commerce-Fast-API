import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import connect_to_mongo, close_mongo_connection
from app.routers import products, orders
from app.middleware import LoggingMiddleware, ErrorHandlingMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app instance
app = FastAPI(
    title="E-Commerce Backend API",
    description="A FastAPI backend for e-commerce application with MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add middleware in order (last added = first executed)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event - Connect to MongoDB
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

# Shutdown event - Disconnect from MongoDB
@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Include routers
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])

@app.get("/")
async def root():
    return {"message": "Welcome to E-Commerce Backend API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 