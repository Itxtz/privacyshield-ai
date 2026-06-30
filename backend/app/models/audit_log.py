from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from datetime import datetime

from app.db.base import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    action = Column(
        String
    )

    resource = Column(
        String
    )

    details = Column(
        String
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )