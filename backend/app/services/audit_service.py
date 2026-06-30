from sqlalchemy.orm import Session

from app.models.audit_log import (
    AuditLog
)


def log_event(
        db: Session,
        user_id: int,
        action: str,
        resource: str,
        details: str
):

    event = AuditLog(

        user_id=user_id,

        action=action,

        resource=resource,

        details=details
    )

    db.add(event)

    db.commit()