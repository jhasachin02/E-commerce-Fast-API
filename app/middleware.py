import time
import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start time
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {response.status_code} "
                f"Process Time: {process_time:.3f}s"
            )
            
            # Add processing time to response headers
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log error
            process_time = time.time() - start_time
            logger.error(
                f"Error processing {request.method} {request.url.path}: {str(e)} "
                f"Process Time: {process_time:.3f}s"
            )
            
            # Return error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "detail": "An unexpected error occurred"
                }
            )

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for consistent error handling"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            # Log the error
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            
            # Return consistent error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "detail": "An unexpected error occurred. Please try again later."
                }
            ) 