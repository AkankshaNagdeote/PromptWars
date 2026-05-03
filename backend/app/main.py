import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router
from app.core.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

def create_app() -> FastAPI:
    """
    Application factory pattern for modularity and testing.
    """
    app = FastAPI(
        title=settings.app_name,
        description="Backend API for the Election Assistant Hackathon Project",
        version="1.0.0"
    )

    # Security: CORS Middleware configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, restrict this to the frontend domain
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
