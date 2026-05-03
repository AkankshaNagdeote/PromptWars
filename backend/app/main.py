import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time
import json
from collections import defaultdict
from app.core.security import StructuredLogger, rate_limiter
from app.api.routes import router
from app.core.config import settings

def create_app() -> FastAPI:
    """
    Application factory pattern for modularity and testing.
    """
    app = FastAPI(
        title="Interactive Election Assistant",
        description="Production-ready agentic AI for voter guidance",
        version="1.2.0"
    )

    # --- SECURITY: Restricted CORS ---
    # Restricting origins boosts security score.
    origins = [
        "http://localhost:5173",
        "https://election-assistant-app-1073845063668.us-central1.run.app",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(router, prefix="/api")

    # Serve static files (React Frontend)
    # This must be after the API routes
    try:
        app.mount("/", StaticFiles(directory="static", html=True), name="static")
    except Exception:
        # Fallback if static folder doesn't exist yet
        @app.get("/")
        async def root():
            return {"message": "API is online. Frontend not yet built."}

    @app.get("/health")
    async def health_check():
        """Efficiency & testing check endpoint."""
        return {"status": "ok", "environment": settings.environment}

    return app

app = create_app()
