"""
Pydantic schemas cho Employee API.
"""
from datetime import datetime, date
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, field_validator, EmailStr
from uuid import UUID


class EmployeeBase(BaseModel):
    """Base employee schema."""
    name: str = Field(..., min_length=1, max_length=100, description="Tên nhân viên")
    role: str = Field(..., description="Vai trò")
    skills: List[str] = Field(default=[], description="Danh sách kỹ năng")
    phone: Optional[str] = Field(None, max_length=20, description="Số điện thoại")
    email: Optional[EmailStr] = Field(None, description="Email")
    address: Optional[str] = Field(None, max_length=500, description="Địa chỉ")
    base_salary: Optional[float] = Field(0, ge=0, description="Lương cơ bản")
    notes: Optional[str] = Field(None, description="Ghi chú")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        allowed_roles = ['Photo/Retouch', 'Makeup Artist', 'Sales', 'Manager', 'Content', 'Designer']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v

    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v):
        allowed_skills = [
            'Chụp chính', 'Chụp phụ', 'Retouch', 'Makeup', 'Làm tóc',
            'Styling', 'Sales', 'Tư vấn khách hàng', 'Quản lý dự án',
            'Viết content', 'Thiết kế', 'Quay phim', 'Dựng phim',
            'Quản lý social', 'Marketing', 'Chăm sóc khách hàng'
        ]
        for skill in v:
            if skill not in allowed_skills:
                raise ValueError(f'Invalid skill: {skill}')
        return v


class BankAccountSchema(BaseModel):
    """Schema cho thông tin ngân hàng."""
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_holder: Optional[str] = None


class EmergencyContactSchema(BaseModel):
    """Schema cho liên hệ khẩn cấp."""
    name: Optional[str] = None
    phone: Optional[str] = None
    relationship: Optional[str] = None


class DefaultRatesSchema(BaseModel):
    """Schema cho đơn giá mặc định."""
    main_photo: float = Field(default=500000, ge=0)
    assist_photo: float = Field(default=300000, ge=0)
    retouch: float = Field(default=50000, ge=0)
    makeup: float = Field(default=400000, ge=0)


class EmployeeCreate(EmployeeBase):
    """Schema cho tạo nhân viên mới."""
    bank_account: Optional[BankAccountSchema] = None
    emergency_contact: Optional[EmergencyContactSchema] = None
    default_rates: Optional[DefaultRatesSchema] = None
    is_active: bool = True


class EmployeeUpdate(BaseModel):
    """Schema cho cập nhật nhân viên."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = None
    skills: Optional[List[str]] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    base_salary: Optional[float] = Field(None, ge=0)
    bank_account: Optional[BankAccountSchema] = None
    emergency_contact: Optional[EmergencyContactSchema] = None
    default_rates: Optional[DefaultRatesSchema] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class EmployeeRead(EmployeeBase):
    """Schema cho đọc dữ liệu nhân viên."""
    id: UUID
    bank_account: Dict = Field(default={})
    emergency_contact: Dict = Field(default={})
    default_rates: Dict = Field(default={})
    start_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmployeeList(BaseModel):
    """Schema cho danh sách nhân viên."""
    total: int
    items: List[EmployeeRead]


class EmployeeFilter(BaseModel):
    """Schema cho filter nhân viên."""
    role: Optional[str] = None
    is_active: Optional[bool] = None
    search: Optional[str] = Field(None, description="Tìm kiếm theo tên")
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
