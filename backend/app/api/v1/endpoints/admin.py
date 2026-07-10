from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks



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

from typing import Optional
from fastapi import Query

from sqlalchemy import or_

from app.schemas.user import UserRole

from app.services.background_tasks import background_log_event

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users", response_model=list[AdminUserResponse])


def get_all_users(

    search: Optional[str] = Query(
        None,
        description="Search by username or email"
    ),

    role: Optional[UserRole] = Query(
        None,
        description="Filter users by role"
    ),

    sort: Optional[str] = Query(
        "id",
        description="Sort by: id, username, email, role"
    ),

    order: Optional[str] = Query(
        "asc",
        description="Sort order: asc or desc"
    ),

    page: int = Query(
        1,
        ge=1,
        description="Page number"
    ),

    size: int = Query(
        10,
        ge=1,
        le=100,
        description="Items per page"
    ),

    current_user: User = Depends(require_admin),

    db: Session = Depends(get_db)
):

    query = db.query(User)

    if search:

        query = query.filter(

            or_(

                User.username.ilike(f"%{search}%"),

                User.email.ilike(f"%{search}%")

            )

        )
    if role:

        query = query.filter(
            User.role == role.value
        )

    sort_columns = {
        "id": User.id,
        "username": User.username,
        "email": User.email,
        "role": User.role,
    }

    sort_column = sort_columns.get(
        sort.lower(),
        User.id
    )

    if order.lower() == "desc":

        query = query.order_by(
            sort_column.desc()
        )

    else:

        query = query.order_by(
            sort_column.asc()
        )

    offset = (page - 1) * size

    users = (
        query
        .offset(offset)
        .limit(size)
        .all()
    )

    return users

@router.patch(
    "/users/{user_id}/role",
    response_model=AdminUserResponse
)
def update_user_role(

    user_id: int,

    role_update: RoleUpdate,

    background_tasks: BackgroundTasks,

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

    background_tasks.add_task(
        background_log_event,
        user_id=current_user.id,
        action="UPDATE_ROLE",
        resource=user.username,
        details=f"Changed role to {user.role}"
    )

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

    search: Optional[str] = Query(
        None,
        description="Search by resource or details"
    ),

    action: Optional[str] = Query(
        None,
        description="Filter by audit action"
    ),

    sort: Optional[str] = Query(
        "timestamp",
        description="Sort by: timestamp, action, resource"
    ),

    order: Optional[str] = Query(
        "desc",
        description="Sort order: asc or desc"
    ),

    page: int = Query(
        1,
        ge=1,
        description="Page number"
    ),

    size: int = Query(
        10,
        ge=1,
        le=100,
        description="Items per page"
    ),

    current_user: User = Depends(require_admin),

    db: Session = Depends(get_db)
):
    query = (
        db.query(AuditLog, User)
        .join(User, AuditLog.user_id == User.id)
    )

    if search:

        query = query.filter(

            or_(

                User.username.ilike(f"%{search}%"),

                AuditLog.resource.ilike(f"%{search}%"),

                AuditLog.details.ilike(f"%{search}%")

            )

        )
    if action:

        query = query.filter(
            AuditLog.action == action.upper()
        )

    sort_columns = {

        "timestamp": AuditLog.timestamp,

        "action": AuditLog.action,

        "resource": AuditLog.resource

    }

    sort_column = sort_columns.get(

        sort.lower(),

        AuditLog.timestamp

    )

    if order.lower() == "desc":

        query = query.order_by(
            sort_column.desc()
        )

    else:

        query = query.order_by(
            sort_column.asc()
        )

    offset = (page - 1) * size

    audit_logs = (

        query

        .offset(offset)

        .limit(size)

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

@router.patch(
    "/users/{user_id}/disable",
    response_model=AdminUserResponse
)
def disable_user(

    user_id: int,

    background_tasks: BackgroundTasks,

    current_user: User = Depends(require_admin),

    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if user.id == current_user.id:

        raise HTTPException(
            status_code=400,
            detail="You cannot disable your own account."
        )
    
    user.is_active = False

    db.commit()

    db.refresh(user)

    background_tasks.add_task(
        background_log_event,
        user_id=current_user.id,
        action="DISABLE_USER",
        resource=user.username,
        details="User account disabled"
    )

    return user

@router.patch(
    "/users/{user_id}/enable",
    response_model=AdminUserResponse
)
def enable_user(

    user_id: int,

    background_tasks: BackgroundTasks,

    current_user: User = Depends(require_admin),

    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if user.id == current_user.id:

        raise HTTPException(
            status_code=400,
            detail="You cannot disable your own account."
        )
    
    user.is_active = True

    db.commit()

    db.refresh(user)

    background_tasks.add_task(
        background_log_event,
        user_id=current_user.id,
        action="ENABLE_USER",
        resource=user.username,
        details="User account enabled"
    )

    return user
