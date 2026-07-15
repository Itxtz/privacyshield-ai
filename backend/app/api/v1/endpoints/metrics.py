from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.models.file import File

from app.models.analysis import AnalysisResult

from app.models.audit_log import AuditLog

from app.core.security import get_current_admin

from app.schemas.user import (
    MetricsResponse,
    UserMetrics,
    DocumentMetrics,
    AnalysisMetrics,
    SecurityMetrics
)

from app.core.config import settings

from datetime import datetime, timezone

from fastapi import Request

router = APIRouter()


@router.get(
    "/admin/metrics",
    response_model=MetricsResponse,
    tags=["Metrics"]
)
def get_metrics(
    request: Request,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    uptime = str(
        datetime.now(timezone.utc) - request.app.state.start_time
    )

    user_metrics = UserMetrics(
        total=db.query(User).count(),

        admins=db.query(User).filter(
            User.role == "admin"
        ).count(),

        active=db.query(User).filter(
            User.is_active == True
        ).count(),

        disabled=db.query(User).filter(
            User.is_active == False
        ).count()
    )

    document_metrics = DocumentMetrics(
        uploaded=db.query(File).count()
    )

    analysis_metrics = AnalysisMetrics(
        completed=db.query(
            AnalysisResult
        ).count()
    )

    security_metrics = SecurityMetrics(
        audit_logs=db.query(
            AuditLog
        ).count()
    )

    return MetricsResponse(

        app_name=settings.APP_NAME,

        version=settings.APP_VERSION,

        uptime=uptime,

        users=user_metrics,

        documents=document_metrics,

        analysis=analysis_metrics,

        security=security_metrics
    )

