from pydantic import BaseModel, EmailStr
from enum import Enum


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


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