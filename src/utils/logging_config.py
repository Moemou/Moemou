"""
Logging configuration for Moemou application.
"""

import logging
import sys
from loguru import logger

from src.config import settings


def setup_logging():
    """Configure application logging."""

    # Remove default loguru handler
    logger.remove()

    # Add custom handler with formatting
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True
    )

    # Add file handler for production
    if settings.app_env == "production":
        logger.add(
            "logs/moemou_{time}.log",
            rotation="500 MB",
            retention="10 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"
        )

    # Intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    # Intercept uvicorn logs
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]

    logger.info(f"Logging configured - Level: {settings.log_level}, Environment: {settings.app_env}")

    return logger
