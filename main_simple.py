"""
Minimal FastAPI app for testing Render deployment
This version will work without any database dependencies
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI(
    title="E-Commerce Backend API - Test",
    description="Minimal version for Render deployment testing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🎉 E-Commerce FastAPI Backend is running!",
        "status": "success",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is running perfectly",
        "deployment": "render",
        "port": os.getenv("PORT", "8000")
    }

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify deployment"""
    return {
        "test": "success",
        "message": "Render deployment is working!",
        "environment": {
            "PORT": os.getenv("PORT"),
            "PYTHON_VERSION": os.getenv("PYTHON_VERSION", "unknown")
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
