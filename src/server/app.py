"""
FastAPI application for Databricks API.

This is a stub module that provides compatibility with existing tests.
The actual implementation uses the MCP protocol directly.
"""

from fastapi import Depends, FastAPI

from src.api import clusters, dbfs, jobs, notebooks, sql
from src.core.auth import validate_api_key
from src.core.config import settings


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    All endpoints require a valid X-API-Key header (validated via validate_api_key).
    """
    app = FastAPI(
        title="Databricks API",
        description="API for interacting with Databricks services",
        version=settings.VERSION,
    )

    auth = Depends(validate_api_key)

    @app.get("/api/2.0/clusters/list", dependencies=[auth])
    async def list_clusters():
        """List all clusters."""
        return await clusters.list_clusters()

    @app.get("/api/2.0/clusters/get/{cluster_id}", dependencies=[auth])
    async def get_cluster(cluster_id: str):
        """Get cluster details."""
        return await clusters.get_cluster(cluster_id)

    @app.post("/api/2.0/clusters/create", dependencies=[auth])
    async def create_cluster(request_data: dict):
        """Create a new cluster."""
        return await clusters.create_cluster(request_data)

    @app.post("/api/2.0/clusters/delete", dependencies=[auth])
    async def terminate_cluster(request_data: dict):
        """Terminate a cluster."""
        return await clusters.terminate_cluster(request_data.get("cluster_id"))

    @app.post("/api/2.0/clusters/start", dependencies=[auth])
    async def start_cluster(request_data: dict):
        """Start a cluster."""
        return await clusters.start_cluster(request_data.get("cluster_id"))

    @app.post("/api/2.0/clusters/resize", dependencies=[auth])
    async def resize_cluster(request_data: dict):
        """Resize a cluster."""
        return await clusters.resize_cluster(
            request_data.get("cluster_id"),
            request_data.get("num_workers"),
        )

    @app.post("/api/2.0/clusters/restart", dependencies=[auth])
    async def restart_cluster(request_data: dict):
        """Restart a cluster."""
        return await clusters.restart_cluster(request_data.get("cluster_id"))

    return app
