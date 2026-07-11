from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.schemas.user import UserLogin
from app.schemas.token import Token

from app.core.security import create_access_token

from app.services.auth_service import (
    create_user,
    authenticate_user
)

from app.core.security import get_current_user
from app.models.user import User

from app.db.database import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse
)

from app.services.auth_service import create_user

from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import InvalidCredentialsException

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    return create_user(db, user)

@router.post(
    "/login",
    response_model=Token
)
def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):

    db_user = authenticate_user(
    db,
    form_data.username,
    form_data.password
    )

    if not db_user:
        raise InvalidCredentialsException()

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
        current_user: User = Depends(
            get_current_user
        )
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }