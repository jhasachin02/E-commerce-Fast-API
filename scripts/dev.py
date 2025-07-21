#!/usr/bin/env python3
"""
Development server runner
Starts the FastAPI application in development mode
"""

import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🚀 Starting development server...")
    print(f"📁 Working directory: {project_root}")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🏥 Health check: http://localhost:8000/health")
    print("\n" + "="*50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
