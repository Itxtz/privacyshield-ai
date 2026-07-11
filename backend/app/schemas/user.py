from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)
from enum import Enum


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        min_length=4,
        max_length=128
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):

        if not value.strip():

            raise ValueError(
                "Username cannot be empty."
            )

        return value
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if not value.strip():

            raise ValueError(
                "Password cannot be empty."
            )

        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class AdminUserResponse(BaseModel):

    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class RoleUpdate(BaseModel):
    role: UserRole

class SystemStatsResponse(BaseModel):

    total_users: int

    total_admins: int

    total_regular_users: int

    total_files: int

    total_analyses: int

    total_audit_logs: int