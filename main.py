import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import connect_to_mongo, close_mongo_connection
from app.routers import products, orders
from app.middleware import LoggingMiddleware, ErrorHandlingMiddleware

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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

# Startup event - Connect to MongoDB (non-blocking)
@app.on_event("startup")
async def startup_db_client():
    logger.info("🚀 Starting FastAPI E-commerce application...")
    logger.info(f"🔧 MongoDB URL configured: {'✅' if os.getenv('MONGODB_URL') else '❌'}")
    logger.info("🔄 Database connection will be established on first request")
    logger.info("✅ Application startup completed")

# Shutdown event - Disconnect from MongoDB
@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Shutting down FastAPI application...")
    await close_mongo_connection()
    logger.info("Application shutdown completed")

# Include routers
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["orders"])

@app.get("/")
async def root():
    """Root endpoint with basic API information"""
    return {
        "message": "Welcome to E-Commerce Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint that works regardless of database status"""
    return {
        "status": "healthy",
        "message": "API is running",
        "timestamp": "2025-07-19",
        "database": "connection will be tested on first request"
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 