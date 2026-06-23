from fastapi import FastAPI

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
    }