from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from src.enums.user_enum import UserRole

class UserCreate(BaseModel):
        first_name: str
        last_name:str | None = None
        email: EmailStr
        password: str
        # role: UserRole = UserRole.USER

class UserUpdate(BaseModel):
        first_name: str | None = None
        last_name: str | None = None
        email: EmailStr | None = None
        password: str | None = None
        role: UserRole | None = None
        is_active: bool | None = None

class UserResponse(BaseModel):

        model_config = ConfigDict(
            from_attributes=True
        )
        id: int
        first_name: str
        last_name: str
        email: EmailStr
        # role: UserRole
        is_active: bool
        created_at: datetime
        updated_at: datetime

class UserLogin(BaseModel):

    email: EmailStr

    password: str