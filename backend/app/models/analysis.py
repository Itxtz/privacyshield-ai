from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.db.base import Base


class AnalysisResult(Base):

    __tablename__ = "analysis_results"

    id = Column(
        Integer,
        primary_key=True
    )

    file_id = Column(
        Integer,
        ForeignKey("files.id")
    )

    risk_score = Column(Integer)

    risk_level = Column(String)

    findings_count = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )