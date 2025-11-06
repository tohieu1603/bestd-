"""
Pydantic schemas cho Package API.
"""
from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class PackageDetailsSchema(BaseModel):
    """Schema cho chi tiết gói."""
    photo: Optional[int] = Field(None, description="Số lượng ảnh")
    makeup: Optional[int] = Field(None, description="Số người makeup")
    assistant: Optional[int] = Field(None, description="Số trợ lý")
    retouch: Optional[int] = Field(None, description="Số ảnh retouch")
    time: Optional[str] = Field(None, description="Thời gian chụp")
    location: Optional[str] = Field(None, description="Địa điểm")
    retouch_photos: Optional[int] = Field(None, description="Số ảnh được retouch")
    extra_services: Optional[List[str]] = Field(default=[], description="Dịch vụ thêm")


class PackageBase(BaseModel):
    """Base package schema."""
    name: str = Field(..., min_length=1, max_length=200, description="Tên gói")
    category: str = Field(..., description="Danh mục")
    price: float = Field(..., ge=0, description="Giá gói")
    description: Optional[str] = Field(None, description="Mô tả")
    notes: Optional[str] = Field(None, description="Ghi chú")

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        allowed_categories = ['portrait', 'family', 'couple', 'wedding', 'event', 'commercial', 'other']
        if v not in allowed_categories:
            raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        return v


class PackageCreate(PackageBase):
    """Schema cho tạo gói mới."""
    details: Optional[PackageDetailsSchema] = None
    includes: Optional[List[str]] = Field(default=[], description="Danh sách dịch vụ bao gồm")
    is_active: bool = True
    popularity_score: int = Field(default=0, ge=0)


class PackageUpdate(BaseModel):
    """Schema cho cập nhật gói."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    details: Optional[PackageDetailsSchema] = None
    includes: Optional[List[str]] = None
    is_active: Optional[bool] = None
    popularity_score: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    notes: Optional[str] = None


class PackageRead(PackageBase):
    """Schema cho đọc dữ liệu gói."""
    id: UUID
    package_id: str
    details: Dict = Field(default={})
    includes: List[str] = Field(default=[])
    is_active: bool
    popularity_score: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PackageList(BaseModel):
    """Schema cho danh sách gói."""
    total: int
    items: List[PackageRead]


class PackageFilter(BaseModel):
    """Schema cho filter gói."""
    category: Optional[str] = None
    is_active: Optional[bool] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    search: Optional[str] = Field(None, description="Tìm kiếm theo tên")
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
