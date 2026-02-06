"""FastAPI application setup for the execution server."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from taskweaver.ces.server.routes import router
from taskweaver.ces.server.session_manager import ServerSessionManager
from taskweaver.chat.web import chat_router
from taskweaver.chat.web.routes import chat_manager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifecycle (startup and shutdown)."""
    # Startup
    logger.info("Starting TaskWeaver Execution Server")

    # Initialize session manager from app state config
    work_dir = getattr(app.state, "work_dir", None) or os.getcwd()
    env_id = getattr(app.state, "env_id", None) or "server"
    app_dir = getattr(app.state, "app_dir", None)

    session_manager = ServerSessionManager(
        env_id=env_id,
        work_dir=work_dir,
    )
    app.state.session_manager = session_manager

    logger.info(f"Session manager initialized with work_dir={work_dir}")

    # Initialize chat session manager
    if app_dir:
        chat_manager.set_app_dir(app_dir)
    logger.info(f"Chat session manager initialized with app_dir={app_dir}")

    yield

    # Shutdown
    logger.info("Shutting down TaskWeaver Execution Server")
    session_manager.cleanup_all()
    chat_manager.cleanup_all()


def create_app(
    api_key: Optional[str] = None,
    work_dir: Optional[str] = None,
    env_id: Optional[str] = None,
    app_dir: Optional[str] = None,
    cors_origins: Optional[list[str]] = None,
    serve_frontend: bool = True,
) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        api_key: Optional API key for authentication. If not provided,
                 authentication is disabled for localhost.
        work_dir: Working directory for session data.
        env_id: Environment identifier.
        app_dir: TaskWeaver project directory for chat sessions.
        cors_origins: List of allowed CORS origins. Defaults to allowing all.

    Returns:
        Configured FastAPI application.
    """
    app = FastAPI(
        title="TaskWeaver Execution Server",
        description="HTTP API for remote code execution with Jupyter kernels",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Store configuration in app state for lifespan to use
    app.state.api_key = api_key or os.getenv("TASKWEAVER_SERVER_API_KEY")
    app.state.work_dir = work_dir or os.getenv("TASKWEAVER_SERVER_WORK_DIR")
    app.state.env_id = env_id or os.getenv("TASKWEAVER_ENV_ID")
    app.state.app_dir = app_dir or os.getenv("TASKWEAVER_APP_DIR")

    # Configure CORS
    if cors_origins is None:
        cors_origins = ["*"]  # Allow all origins by default for local dev

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router)
    app.include_router(chat_router)

    # Mount frontend static files (must be last, catches all unmatched routes)
    if serve_frontend:
        try:
            from taskweaver.web import mount_frontend

            mount_frontend(app)
        except ImportError:
            logger.debug("Frontend static files not available")

    return app


# Default app instance for uvicorn
app = create_app()
