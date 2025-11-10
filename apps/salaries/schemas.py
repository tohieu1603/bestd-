"""
Pydantic schemas cho Salary API.
"""
from datetime import datetime, date
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class SalaryBase(BaseModel):
    """Base salary schema."""
    employee: UUID = Field(..., description="ID nhân viên")
    project: UUID = Field(..., description="ID dự án")
    month: str = Field(..., pattern=r'^\d{4}-\d{2}$', description="Tháng (YYYY-MM)")
    amount: float = Field(..., ge=0, description="Số tiền")
    bonus: float = Field(default=0, ge=0, description="Thưởng")
    work_type: str = Field(..., description="Loại công việc")
    quantity: int = Field(default=1, ge=0, description="Số lượng")
    notes: Optional[str] = None

    @field_validator('work_type')
    @classmethod
    def validate_work_type(cls, v):
        allowed_types = ['mainPhotographer', 'assistPhotographer', 'makeupArtist', 'retouchArtist', 'other']
        if v not in allowed_types:
            raise ValueError(f'Work type must be one of: {", ".join(allowed_types)}')
        return v


class SalaryCreate(SalaryBase):
    """Schema cho tạo salary."""
    is_paid: bool = False


class SalaryUpdate(BaseModel):
    """Schema cho cập nhật salary."""
    amount: Optional[float] = Field(None, ge=0)
    bonus: Optional[float] = Field(None, ge=0)
    work_type: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    is_paid: Optional[bool] = None
    paid_date: Optional[date] = None
    notes: Optional[str] = None


class SalaryRead(SalaryBase):
    """Schema cho đọc dữ liệu salary."""
    id: UUID
    is_paid: bool
    paid_date: Optional[date] = None
    total_compensation: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SalaryList(BaseModel):
    """Schema cho danh sách salary."""
    total: int
    items: List[SalaryRead]


class EmployeeMinimal(BaseModel):
    """Minimal employee info for salary."""
    id: UUID
    name: str

    class Config:
        from_attributes = True


class ProjectDetail(BaseModel):
    """Project detail for salary."""
    project_id: str  # Changed to str for flexibility
    project_name: str
    salary: float


class MonthlySalaryBase(BaseModel):
    """Base monthly salary schema."""
    employee_id: UUID = Field(..., description="ID nhân viên")
    month: str = Field(..., pattern=r'^\d{4}-\d{2}$', description="Tháng (YYYY-MM)")
    base_salary: float = Field(default=0, ge=0, description="Lương cơ bản")
    bonus: float = Field(default=0, ge=0, description="Thưởng")
    deduction: float = Field(default=0, ge=0, description="Khấu trừ")
    total_amount: float = Field(..., ge=0, description="Tổng lương")


class MonthlySalaryCreate(BaseModel):
    """Schema cho tạo monthly salary."""
    employee_id: UUID = Field(..., description="ID nhân viên")
    month: str = Field(..., pattern=r'^\d{4}-\d{2}$', description="Tháng (YYYY-MM)")
    base_salary: float = Field(default=0, ge=0, description="Lương cơ bản")
    bonus: float = Field(default=0, ge=0, description="Thưởng")
    deduction: float = Field(default=0, ge=0, description="Khấu trừ")
    total_amount: float = Field(..., ge=0, description="Tổng lương")
    projects_detail: List[ProjectDetail] = Field(default=[], description="Chi tiết dự án")
    status: str = Field(default='pending', description="Trạng thái")
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class MonthlySalaryUpdate(BaseModel):
    """Schema cho cập nhật monthly salary."""
    base_salary: Optional[float] = Field(None, ge=0)
    bonus: Optional[float] = Field(None, ge=0)
    deduction: Optional[float] = Field(None, ge=0)
    total_amount: Optional[float] = Field(None, ge=0)
    projects_detail: Optional[List[ProjectDetail]] = None
    status: Optional[str] = None
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class MonthlySalaryRead(BaseModel):
    """Schema cho đọc dữ liệu monthly salary."""
    id: UUID
    employee: EmployeeMinimal
    month: str
    base_salary: float
    bonus: float
    deduction: float
    total_amount: float
    projects_detail: List[Dict] = []
    status: str
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MonthlySalaryList(BaseModel):
    """Schema cho danh sách monthly salary."""
    total: int
    results: List[Dict]  # Use Dict to match manual serialization in API


class SalaryFilter(BaseModel):
    """Schema cho filter salary."""
    employee: Optional[UUID] = None
    project: Optional[UUID] = None
    month: Optional[str] = None
    is_paid: Optional[bool] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class CalculateSalaryRequest(BaseModel):
    """Schema cho tính lương tháng."""
    employee: UUID = Field(..., description="ID nhân viên")
    month: str = Field(..., pattern=r'^\d{4}-\d{2}$', description="Tháng (YYYY-MM)")


class SalaryReportResponse(BaseModel):
    """Schema cho báo cáo lương."""
    month: str
    total_employees: int
    total_salary: float
    total_paid: float
    total_unpaid: float
    employee_salaries: List[Dict]
