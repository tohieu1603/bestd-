"""
Pydantic schemas cho Project API.
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, field_validator
from uuid import UUID


# Team schemas
class TeamMemberSchema(BaseModel):
    """Schema cho thành viên team."""
    employee: UUID
    salary: Optional[float] = Field(None, ge=0)
    bonus: Optional[float] = Field(default=0, ge=0)
    notes: Optional[str] = None


class RetouchArtistSchema(TeamMemberSchema):
    """Schema cho retouch artist có thêm quantity."""
    quantity: Optional[int] = Field(None, ge=0)


class TeamSchema(BaseModel):
    """Schema cho team."""
    main_photographer: Optional[TeamMemberSchema] = None
    assist_photographers: Optional[List[TeamMemberSchema]] = Field(default=[])
    makeup_artists: Optional[List[TeamMemberSchema]] = Field(default=[])
    retouch_artists: Optional[List[RetouchArtistSchema]] = Field(default=[])


# Milestone schema
class MilestoneSchema(BaseModel):
    """Schema cho milestone."""
    name: str
    description: Optional[str] = None
    stage: str = Field(..., description="shooting, makeup, retouch, delivery, custom")
    status: str = Field(default='pending', description="pending, in-progress, completed")
    team: Optional[TeamSchema] = None
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    completed_by: Optional[UUID] = None
    notes: Optional[str] = None


# Payment schema
class PaymentHistorySchema(BaseModel):
    """Schema cho lịch sử thanh toán."""
    amount: float = Field(..., ge=0)
    date: date
    method: Optional[str] = None
    notes: Optional[str] = None
    received_by: Optional[UUID] = None


class PaymentSchema(BaseModel):
    """Schema cho thanh toán."""
    status: str = Field(default='unpaid', description="unpaid, deposit, paid")
    deposit: float = Field(default=0, ge=0)
    final: float = Field(default=0, ge=0)
    paid: float = Field(default=0, ge=0)
    payment_history: Optional[List[PaymentHistorySchema]] = Field(default=[])


# Partner schema
class PartnerItemSchema(BaseModel):
    """Schema cho partner item."""
    partner: UUID
    actual_cost: Optional[float] = Field(None, ge=0)


class PartnerServiceSchema(BaseModel):
    """Schema cho partner service (printing, flower)."""
    included: bool = False
    actual_cost: Optional[float] = Field(None, ge=0)


class PartnersSchema(BaseModel):
    """Schema cho partners."""
    clothing: Optional[List[PartnerItemSchema]] = Field(default=[])
    printing: Optional[PartnerServiceSchema] = None
    flower: Optional[PartnerServiceSchema] = None
    total_cost: Optional[float] = Field(default=0, ge=0)
    notes: Optional[List[str]] = Field(default=[])


# Additional package schema
class AdditionalPackageSchema(BaseModel):
    """Schema cho gói bổ sung."""
    package_type: UUID
    package_name: str
    package_price: float = Field(..., ge=0)
    package_discount: float = Field(default=0, ge=0)
    package_final_price: Optional[float] = None
    team: Optional[TeamSchema] = None
    notes: Optional[str] = None


# Progress schema
class ProgressSchema(BaseModel):
    """Schema cho tiến độ."""
    shooting_done: bool = False
    retouch_done: bool = False
    delivered: bool = False


# File schema
class FileSchema(BaseModel):
    """Schema cho file."""
    type: str
    url: str
    uploaded_at: Optional[datetime] = None


# Main project schemas
class ProjectBase(BaseModel):
    """Base project schema."""
    customer_name: str = Field(..., min_length=1, max_length=200)
    customer_phone: str = Field(..., min_length=1, max_length=20)
    customer_email: Optional[EmailStr] = None
    package_type: UUID
    package_name: str
    package_price: float = Field(..., ge=0)
    package_discount: float = Field(default=0, ge=0)
    shoot_date: date
    shoot_time: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema cho tạo dự án mới."""
    additional_packages: Optional[List[AdditionalPackageSchema]] = Field(default=[])
    team: Optional[TeamSchema] = None
    partners: Optional[PartnersSchema] = None
    payment: Optional[PaymentSchema] = None
    status: str = Field(default='pending')


class ProjectUpdate(BaseModel):
    """Schema cho cập nhật dự án."""
    customer_name: Optional[str] = Field(None, min_length=1, max_length=200)
    customer_phone: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    package_name: Optional[str] = None
    package_price: Optional[float] = Field(None, ge=0)
    package_discount: Optional[float] = Field(None, ge=0)
    shoot_date: Optional[date] = None
    shoot_time: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    additional_packages: Optional[List[AdditionalPackageSchema]] = None
    team: Optional[TeamSchema] = None
    partners: Optional[PartnersSchema] = None
    payment: Optional[PaymentSchema] = None
    progress: Optional[ProgressSchema] = None
    milestones: Optional[List[MilestoneSchema]] = None
    completed_date: Optional[date] = None
    delivery_date: Optional[date] = None
    files: Optional[List[FileSchema]] = None
    notes: Optional[str] = None


class ProjectRead(ProjectBase):
    """Schema cho đọc dữ liệu dự án."""
    id: UUID
    project_code: str
    package_final_price: float
    additional_packages: List = Field(default=[])
    payment: Dict = Field(default={})
    status: str
    progress: Dict = Field(default={})
    milestones: List = Field(default=[])
    team: Dict = Field(default={})
    partners: Dict = Field(default={})
    completed_date: Optional[date] = None
    delivery_date: Optional[date] = None
    files: List = Field(default=[])
    update_history: List = Field(default=[])
    created_at: datetime
    updated_at: datetime

    @field_validator('package_type', mode='before')
    @classmethod
    def serialize_package_type(cls, v):
        """Convert Package instance to UUID."""
        if hasattr(v, 'id'):
            return v.id
        return v

    class Config:
        from_attributes = True


class ProjectList(BaseModel):
    """Schema cho danh sách dự án."""
    total: int
    items: List[ProjectRead]


class ProjectFilter(BaseModel):
    """Schema cho filter dự án."""
    status: Optional[str] = None
    payment_status: Optional[str] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    customer_name: Optional[str] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class AddMilestoneRequest(BaseModel):
    """Schema cho thêm milestone."""
    milestone: MilestoneSchema


class UpdateProgressRequest(BaseModel):
    """Schema cho cập nhật tiến độ."""
    progress: ProgressSchema


class AddPaymentRequest(BaseModel):
    """Schema cho thêm thanh toán."""
    payment_item: PaymentHistorySchema
