from fastapi import APIRouter

from .schemas import HealthCheckResponse


router = APIRouter(prefix="/v1/health", tags=["Health"])


@router.get("/", summary="Health Check")
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint to verify the service is running.
    Returns a simple message indicating the service is healthy.
    """
    return HealthCheckResponse(status="ok")
