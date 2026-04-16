"""
Authentication functionality for the Databricks MCP server.
"""

import logging
import os
from typing import Dict, Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.core.config import settings

logger = logging.getLogger(__name__)

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

_VALID_API_KEY: Optional[str] = os.environ.get("MCP_API_KEY")


async def validate_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> Dict[str, str]:
    """
    Validate the API key provided in the X-API-Key request header.

    Requires the MCP_API_KEY environment variable to be set. If it is not set,
    the server will refuse all requests to protected endpoints at startup time.

    Raises:
        HTTPException 401: If the key is missing or does not match MCP_API_KEY.
        HTTPException 500: If MCP_API_KEY is not configured in the environment.
    """
    if not _VALID_API_KEY:
        logger.error("MCP_API_KEY environment variable is not set — rejecting all requests")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server authentication is not configured. Set the MCP_API_KEY environment variable.",
        )

    if not api_key:
        logger.warning("Authentication failed: missing API key in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if api_key != _VALID_API_KEY:
        logger.warning("Authentication failed: invalid API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return {"authenticated": True}
