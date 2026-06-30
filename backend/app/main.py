from fastapi import FastAPI

from app.core.config import settings

from app.db.database import engine
from app.db.base import Base

from app.models.user import User

from app.api.v1.api import api_router

from app.models.file import File

from app.models.analysis import AnalysisResult

from app.models.audit_log import AuditLog

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
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