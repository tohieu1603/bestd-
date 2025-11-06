"""
Pydantic schemas cho Partner API.
"""
from datetime import datetime, date
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, field_validator, EmailStr
from uuid import UUID


class ContactInfoSchema(BaseModel):
    """Schema cho thông tin liên hệ."""
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    website: Optional[str] = None
    contact_person: Optional[str] = None


class BankAccountSchema(BaseModel):
    """Schema cho thông tin ngân hàng."""
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_holder: Optional[str] = None


class BusinessInfoSchema(BaseModel):
    """Schema cho thông tin doanh nghiệp."""
    tax_code: Optional[str] = None
    business_license: Optional[str] = None
    established_date: Optional[date] = None


class AgreementSchema(BaseModel):
    """Schema cho hợp đồng."""
    title: str
    file_url: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    terms: Optional[str] = None


class PartnerBase(BaseModel):
    """Base partner schema."""
    name: str = Field(..., min_length=1, max_length=200, description="Tên đối tác")
    type: str = Field(..., description="Loại đối tác")
    cost: str = Field(..., description="Chi phí (số hoặc 'Theo bill')")
    notes: Optional[str] = Field(None, description="Ghi chú")

    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        allowed_types = ['clothing', 'printing', 'flower', 'venue', 'equipment', 'other']
        if v not in allowed_types:
            raise ValueError(f'Type must be one of: {", ".join(allowed_types)}')
        return v


class PartnerCreate(PartnerBase):
    """Schema cho tạo đối tác mới."""
    contact_info: Optional[ContactInfoSchema] = None
    bank_account: Optional[BankAccountSchema] = None
    business_info: Optional[BusinessInfoSchema] = None
    rating: float = Field(default=0, ge=0, le=5)
    is_active: bool = True
    agreements: Optional[List[AgreementSchema]] = Field(default=[])


class PartnerUpdate(BaseModel):
    """Schema cho cập nhật đối tác."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    type: Optional[str] = None
    cost: Optional[str] = None
    contact_info: Optional[ContactInfoSchema] = None
    bank_account: Optional[BankAccountSchema] = None
    business_info: Optional[BusinessInfoSchema] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    is_active: Optional[bool] = None
    notes: Optional[str] = None
    agreements: Optional[List[AgreementSchema]] = None


class PartnerRead(PartnerBase):
    """Schema cho đọc dữ liệu đối tác."""
    id: UUID
    partner_id: str
    contact_info: Dict = Field(default={})
    bank_account: Dict = Field(default={})
    business_info: Dict = Field(default={})
    rating: float
    projects_count: int
    total_revenue: float
    is_active: bool
    agreements: List = Field(default=[])
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PartnerList(BaseModel):
    """Schema cho danh sách đối tác."""
    total: int
    items: List[PartnerRead]


class PartnerFilter(BaseModel):
    """Schema cho filter đối tác."""
    type: Optional[str] = None
    is_active: Optional[bool] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    search: Optional[str] = Field(None, description="Tìm kiếm theo tên")
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
