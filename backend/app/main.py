from fastapi import FastAPI

from app.db.database import engine
from app.db.base import Base

from app.models.user import User

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Welcome to PrivacyShield AI"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
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