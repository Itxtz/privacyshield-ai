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
