"""
Main application entry point for Moemou - Breakoutlabs AI Skincare Agent.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import settings
from src.api import router
from src.utils.logging_config import setup_logging

# Setup logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("🚀 Starting Moemou - Breakoutlabs AI Skincare Agent")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"Agent Type: {settings.agent_type}")
    yield
    logger.info("👋 Shutting down Moemou")


# Create FastAPI application
app = FastAPI(
    title="Moemou - Breakoutlabs AI Skincare Agent",
    description="""
    Field-specific AI agent for skincare, dermatology, and acne treatment.

    ## Features

    * **Biomarker Analysis**: Intelligent analysis of skin health indicators
    * **Expert Assessment**: AI-powered skin condition evaluation
    * **Personalized Recommendations**: Tailored product and treatment suggestions
    * **Treatment Plans**: Comprehensive skincare routines
    * **Chat Support**: Conversational dermatology expertise

    ## About Breakoutlabs

    Breakoutlabs helps customers achieve clear, healthy skin through
    science-backed skincare solutions and AI-powered support.
    """,
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Moemou - Breakoutlabs AI Skincare Agent",
        "version": "0.1.0",
        "status": "active",
        "message": "Welcome to Breakoutlabs AI skincare support!",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on {settings.api_host}:{settings.api_port}")

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
