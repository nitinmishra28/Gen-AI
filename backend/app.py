# # Working code ----------------------------------
# import logging
# from datetime import datetime, timezone
# from flask import Flask, jsonify
# from flask_cors import CORS
# from openai import RateLimitError

# from src.api.routes import api_blueprint
# from src.config import config

# def create_app():
#     """Create and configure the Flask application."""
#     app = Flask(__name__)
#     CORS(app)

#     # Configure logging
#     logging.basicConfig(level=config.LOG_LEVEL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
#     # Register blueprints
#     app.register_blueprint(api_blueprint)

#     # Register error handlers
#     register_error_handlers(app)

#     @app.route('/health', methods=['GET'])
#     def health_check():
#         return jsonify({
#             'status': 'healthy', 
#             'service': 'CV Analysis API',
#             'timestamp': datetime.now(timezone.utc).isoformat()
#         })

#     return app

# def register_error_handlers(app):
#     """Register custom error handlers for the application."""
#     @app.errorhandler(ValueError)
#     def handle_validation_error(e):
#         logging.error(f"Validation error: {e}", exc_info=True)
#         return jsonify({"success": False, "error": "validation_error", "message": str(e)}), 400

#     @app.errorhandler(RateLimitError)
#     def handle_rate_limit_error(e):
#         logging.error(f"Rate limit exceeded: {e}", exc_info=True)
#         return jsonify({"success": False, "error": "rate_limit_exceeded", "message": "API rate limit exceeded."}), 429

#     @app.errorhandler(Exception)
#     def handle_generic_error(e):
#         logging.error(f"Unhandled exception: {e}", exc_info=True)
#         return jsonify({"success": False, "error": "internal_error", "message": "An unexpected error occurred."}), 500

# if __name__ == '__main__':
#     app = create_app()
#     try:
#         # A simple check to ensure analyzer can initialize
#         from src.serivces.analyzer import CVAnalyzer  # Note: Directory is actually misspelled in the filesystem
#         CVAnalyzer()
#         app.run(debug=True, host='0.0.0.0', port=5000)
#     except ValueError as e:
#         logging.critical(f"FATAL: Application cannot start. {e}")





import logging
from datetime import datetime, timezone
from typing import Optional
import traceback
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import RateLimitError

from src.api.routes import api_router
from src.config import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    logger = logging.getLogger(__name__)
    logger.info("Starting CV Analysis API...")
    
    try:
        # Simple check to ensure analyzer can initialize
        from src.serivces.analyzer import CVAnalyzer
        analyzer = CVAnalyzer()
        logger.info("CVAnalyzer initialized successfully")
        
        # Store analyzer in app state for dependency injection
        app.state.analyzer = analyzer
        
    except Exception as e:
        logger.critical(f"FATAL: Application cannot start. {e}")
        if not config.USE_MOCK:
            sys.exit(1)
        else:
            logger.warning("Running in mock mode, continuing startup...")
    
    yield  # Application is running
    
    # Shutdown
    logger.info("Shutting down CV Analysis API...")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="CV Analysis API",
        description="API for CV analysis and processing",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this based on your needs
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Include routers
    app.include_router(api_router)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.get('/health', tags=["health"])
    async def health_check():
        """Health check endpoint to verify service status."""
        return {
            'status': 'healthy', 
            'service': 'CV Analysis API',
            'version': '1.0.0',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'available_models': config.all_available_models,
            'api_keys_configured': {
                'openai': bool(config.OPENAI_API_KEY),
                'gemini': bool(config.GEMINI_API_KEY),
                'ollama': True
            }
        }
    
    return app

def register_error_handlers(app: FastAPI):
    """Register custom error handlers for the application."""
    
    @app.exception_handler(ValueError)
    async def handle_validation_error(request: Request, exc: ValueError):
        logging.error(f"Validation error at {request.url}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=400,
            content={
                "success": False, 
                "error": "validation_error", 
                "message": str(exc),
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(RateLimitError)
    async def handle_rate_limit_error(request: Request, exc: RateLimitError):
        logging.error(f"Rate limit exceeded at {request.url}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=429,
            content={
                "success": False, 
                "error": "rate_limit_exceeded", 
                "message": "API rate limit exceeded. Please try again later.",
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        """Handle FastAPI HTTPExceptions."""
        logging.warning(f"HTTP exception at {request.url}: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": "http_error",
                "message": exc.detail,
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(ConnectionError)
    async def handle_connection_error(request: Request, exc: ConnectionError):
        """Handle connection errors (e.g., Ollama server down)."""
        logging.error(f"Connection error at {request.url}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "error": "service_unavailable",
                "message": "External service is currently unavailable. Please try again later.",
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(Exception)
    async def handle_generic_error(request: Request, exc: Exception):
        logging.error(f"Unhandled exception at {request.url}: {exc}", exc_info=True)
        logging.error(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False, 
                "error": "internal_error", 
                "message": "An unexpected error occurred.",
                "path": str(request.url.path)
            }
        )

# Create the FastAPI app instance
app = create_app()

if __name__ == '__main__':
    try:
        logging.info(f"Starting server on 0.0.0.0:5000")
        logging.info(f"Debug mode: {config.DEBUG}")
        logging.info(f"Available models: {config.all_available_models}")
        
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=5000,
            reload=config.DEBUG,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.critical(f"Failed to start server: {e}")
        sys.exit(1)
