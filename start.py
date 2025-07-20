#!/usr/bin/env python3
"""
Minimal startup script for Render deployment
This ensures the app starts even if there are MongoDB connection issues
"""

import os
import sys
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("🚀 Starting E-commerce FastAPI application...")
        
        # Import here to catch any import errors
        from main import app
        
        # Get port from environment
        port = int(os.getenv("PORT", 8000))
        host = "0.0.0.0"
        
        logger.info(f"📡 Server will bind to {host}:{port}")
        
        # Import uvicorn here to ensure it's available
        import uvicorn
        
        # Start the server with minimal configuration
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
