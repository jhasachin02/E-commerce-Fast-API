#!/usr/bin/env python3
"""
Production startup script for deployment (Render/Railway)
Includes DNS fixes for MongoDB Atlas connectivity
Force Railway deployment update - 2024
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure DNS for MongoDB Atlas SRV resolution (Cloud deployment fix)
try:
    import dns.resolver
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '1.0.0.1']
    print("🔧 DNS configured for MongoDB Atlas SRV resolution")
except Exception as e:
    print(f"⚠️  DNS configuration warning: {e}")

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
