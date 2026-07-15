from fastapi import APIRouter

from app.api.v1.endpoints import auth

from app.api.v1.endpoints import (
    auth,
    file_upload
)

from app.api.v1.endpoints import (
    auth,
    file_upload,
    document_analysis
)

from app.api.v1.endpoints import (
    auth,
    file_upload,
    document_analysis,
    redaction
)

from app.api.v1.endpoints import audit

from app.api.v1.endpoints import dashboard

from app.api.v1.endpoints import admin

from app.api.v1.endpoints import health

from app.api.v1.endpoints import metrics



api_router = APIRouter()

api_router.include_router(
    auth.router
)

api_router.include_router(
    file_upload.router
)

api_router.include_router(
    document_analysis.router
)

api_router.include_router(
    redaction.router
)

api_router.include_router(
    audit.router
)

api_router.include_router(
    dashboard.router
)

api_router.include_router(
    admin.router
)

api_router.include_router(
    health.router
)

api_router.include_router(
    metrics.router
)