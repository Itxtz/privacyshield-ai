from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.models.file import File

from app.core.exceptions import (
    ForbiddenException,
    InactiveAccountException
)


def create_user(db: Session, user: UserCreate):

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(
            user.password
        ),
        role="user",
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def authenticate_user(
        db: Session,
        email: str,
        password: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
            password,
            user.hashed_password
    ):
        return None
    
    if not user.is_active:

        raise InactiveAccountException()

    return user

def verify_file_access(

    db_file: File,

    current_user: User

):
    if (
        db_file.uploaded_by != current_user.id
        and current_user.role != "admin"
    ):
        raise ForbiddenException(
            "Access denied"
        )