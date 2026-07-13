from fastapi import APIRouter

from app.core.config import settings

from datetime import datetime, timezone

from fastapi import Request

router = APIRouter()


@router.get(
    "/health",
    tags=["Health"]
)
def health_check(request: Request):

    uptime = (
        datetime.now(timezone.utc) - request.app.state.start_time
    )
    uptime_str = str(uptime).split(".")[0]

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "uptime": uptime_str
    }