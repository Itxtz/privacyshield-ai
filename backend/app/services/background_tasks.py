from app.db.database import SessionLocal

from app.services.audit_service import log_event

def background_log_event(

    user_id: int,

    action: str,

    resource: str,

    details: str

):
    db = SessionLocal()

    try:

        log_event(

            db=db,

            user_id=user_id,

            action=action,

            resource=resource,

            details=details

        )
    
    finally:
        db.close()