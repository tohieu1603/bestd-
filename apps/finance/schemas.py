"""
Pydantic schemas cho Finance API.
"""
from datetime import date
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class MonthlyOverviewResponse(BaseModel):
    """Schema cho tổng quan tài chính tháng."""
    month: str
    total_revenue: float = Field(..., description="Tổng doanh thu")
    total_costs: float = Field(..., description="Tổng chi phí")
    total_profit: float = Field(..., description="Tổng lợi nhuận")
    revenue_breakdown: Dict = Field(..., description="Chi tiết doanh thu")
    cost_breakdown: Dict = Field(..., description="Chi tiết chi phí")
    project_count: int = Field(..., description="Số lượng dự án")
    completed_project_count: int = Field(..., description="Số dự án hoàn thành")


class ProfitResponse(BaseModel):
    """Schema cho tính lợi nhuận."""
    period: str
    total_revenue: float
    total_costs: float
    profit: float
    profit_margin: float = Field(..., description="Tỷ suất lợi nhuận (%)")
    projects: List[Dict] = Field(..., description="Danh sách dự án")


class ProjectFinanceDetail(BaseModel):
    """Schema cho chi tiết tài chính dự án."""
    project_id: str
    project_code: str
    customer_name: str
    revenue: float = Field(..., description="Doanh thu")
    costs: Dict = Field(..., description="Chi phí")
    total_cost: float = Field(..., description="Tổng chi phí")
    profit: float = Field(..., description="Lợi nhuận")
    profit_margin: float = Field(..., description="Tỷ suất lợi nhuận (%)")


class CashFlowResponse(BaseModel):
    """Schema cho dòng tiền."""
    period: str
    opening_balance: float = Field(default=0, description="Số dư đầu kỳ")
    total_inflow: float = Field(..., description="Tổng tiền vào")
    total_outflow: float = Field(..., description="Tổng tiền ra")
    closing_balance: float = Field(..., description="Số dư cuối kỳ")
    inflow_details: Dict = Field(..., description="Chi tiết tiền vào")
    outflow_details: Dict = Field(..., description="Chi tiết tiền ra")


class RevenueByPackageResponse(BaseModel):
    """Schema cho doanh thu theo gói."""
    period: str
    packages: List[Dict] = Field(..., description="Danh sách gói và doanh thu")
    total_revenue: float


class TopPerformersResponse(BaseModel):
    """Schema cho nhân viên xuất sắc."""
    period: str
    employees: List[Dict] = Field(..., description="Danh sách nhân viên xuất sắc")


class FinancialSummaryResponse(BaseModel):
    """Schema cho tổng hợp tài chính."""
    period: str
    revenue: float
    costs: float
    profit: float
    profit_margin: float
    project_count: int
    completed_projects: int
    pending_payments: float
    total_salaries: float
    partner_costs: float
