from fastapi import FastAPI,HTTPException

from datetime import datetime, timezone

from app.core.config import settings

from app.db.database import engine
from app.db.base import Base

from app.models.user import User

from app.api.v1.api import api_router

from app.models.file import File

from app.models.analysis import AnalysisResult

from app.models.audit_log import AuditLog

from fastapi.exceptions import RequestValidationError

from app.core.error_handlers import (

    http_exception_handler,

    validation_exception_handler,

    rate_limit_exception_handler

)

from app.core.middleware import RequestLoggingMiddleware

from app.core.rate_limiter import limiter

from slowapi.errors import RateLimitExceeded

from app.core.security_headers import SecurityHeadersMiddleware

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.state.start_time = datetime.now(timezone.utc)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    rate_limit_exception_handler
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

Base.metadata.create_all(bind=engine)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to PrivacyShield AI"
    }

'''from fastapi import FastAPI

app = FastAPI(
    title="PrivacyShield AI",
    description="AI Governance and Data Privacy Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to PrivacyShield AI"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }'''