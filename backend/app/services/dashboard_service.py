from sqlalchemy.orm import Session

from app.models.file import File
from app.models.analysis import AnalysisResult
from app.models.audit_log import AuditLog



def get_dashboard_summary(db: Session):

    total_files = db.query(File).count()

    total_analysis = db.query(AnalysisResult).count()

    total_audit_logs = db.query(AuditLog).count()

    high_risk = db.query(
        AnalysisResult
    ).filter(
        AnalysisResult.risk_level == "HIGH"
    ).count()

    return {

        "total_files": total_files,

        "total_analysis": total_analysis,

        "high_risk_documents": high_risk,

        "audit_events": total_audit_logs
    }

def risk_distribution(db: Session):

    low = db.query(
        AnalysisResult
    ).filter(
        AnalysisResult.risk_level == "LOW"
    ).count()

    medium = db.query(
        AnalysisResult
    ).filter(
        AnalysisResult.risk_level == "MEDIUM"
    ).count()

    high = db.query(
        AnalysisResult
    ).filter(
        AnalysisResult.risk_level == "HIGH"
    ).count()

    return {

        "LOW": low,

        "MEDIUM": medium,

        "HIGH": high
    }