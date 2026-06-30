from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.audit_log import (
    AuditLog
)

from app.core.security import (
    get_current_user
)

from app.models.user import User

router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)


@router.get("/history")
def get_audit_history(

        current_user: User =
        Depends(get_current_user),

        db: Session =
        Depends(get_db)
):

    logs = db.query(
        AuditLog
    ).filter(

        AuditLog.user_id ==
        current_user.id

    ).all()

    return logs