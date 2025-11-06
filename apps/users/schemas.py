"""
Pydantic schemas for User API.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=150)
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str = Field(default='employee')


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=6)

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        allowed_roles = ['admin', 'manager', 'sales', 'employee']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserChangePassword(BaseModel):
    """Schema for changing password."""
    old_password: str
    new_password: str = Field(..., min_length=6)


class UserRead(UserBase):
    """Schema for reading user data."""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema for login request."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Schema for login response."""
    success: bool
    token: str
    user: UserRead
    message: str = "Login successful"


class TokenResponse(BaseModel):
    """Schema for token validation response."""
    success: bool
    user: UserRead


# Aliases for API compatibility
LoginSchema = LoginRequest
TokenSchema = LoginResponse
UserSchema = UserRead
PasswordChangeSchema = UserChangePassword
