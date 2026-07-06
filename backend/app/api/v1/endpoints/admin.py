from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.db.database import get_db
from app.models.user import User
from app.core.security import require_admin
from app.schemas.user import AdminUserResponse
from app.schemas.user import RoleUpdate

from app.models.file import File
from app.models.analysis import AnalysisResult
from app.models.audit_log import AuditLog

from app.schemas.user import SystemStatsResponse

from app.schemas.audit import AuditLogResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users", response_model=list[AdminUserResponse])
def get_all_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users

@router.patch(
    "/users/{user_id}/role",
    response_model=AdminUserResponse
)
def update_user_role(

    user_id: int,

    role_update: RoleUpdate,

    current_user: User = Depends(require_admin),

    db: Session = Depends(get_db)
):
    # Find the target user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    
    # Prevent an admin from removing their own admin role
    if (
        current_user.id == user.id
        and role_update.role == "user"
    ):

        raise HTTPException(
            status_code=400,
            detail="You cannot remove your own admin role."
        )
    # Update the user's role
    user.role = role_update.role.value

    db.commit()
    db.refresh(user)

    return user

@router.get(
    "/system-stats",
    response_model=SystemStatsResponse
)
def get_system_stats(

    current_user: User = Depends(require_admin),

    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()

    total_admins = db.query(User).filter(
        User.role == "admin"
    ).count()
    
    total_regular_users = db.query(User).filter(
        User.role == "user"
    ).count()

    total_files = db.query(File).count()

    total_analyses = db.query(
        AnalysisResult
    ).count()

    total_audit_logs = db.query(
        AuditLog
    ).count()

    return SystemStatsResponse(
        total_users=total_users,
        total_admins=total_admins,
        total_regular_users=total_regular_users,
        total_files=total_files,
        total_analyses=total_analyses,
        total_audit_logs=total_audit_logs,
    )

@router.get(
    "/audit-logs",
    response_model=list[AuditLogResponse]
)
def get_all_audit_logs(

    current_user: User = Depends(require_admin),

    db: Session = Depends(get_db)
):
    audit_logs = (
        db.query(AuditLog, User)
        .join(User, AuditLog.user_id == User.id)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )

    return [

        AuditLogResponse(

            id=log.id,

            user_id=user.id,

            username=user.username,

            action=log.action,

            resource=log.resource,

            details=log.details,

            timestamp=log.timestamp

        )

        for log, user in audit_logs

    ]