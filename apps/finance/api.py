"""
API endpoints cho Finance management.
"""
from datetime import date
from ninja import Router, Query
from ninja.errors import HttpError
from .schemas import (
    MonthlyOverviewResponse, ProfitResponse, ProjectFinanceDetail,
    CashFlowResponse, RevenueByPackageResponse, FinancialSummaryResponse
)
from .services import FinanceService

router = Router(tags=["Finance"])


@router.get("/monthly-overview/{month}", response=MonthlyOverviewResponse, summary="Tổng quan tài chính tháng")
def monthly_overview(request, month: str):
    """
    Lấy tổng quan tài chính của tháng.

    - **month**: Tháng (YYYY-MM)

    Returns:
    - Tổng doanh thu, chi phí, lợi nhuận
    - Chi tiết doanh thu và chi phí
    - Số lượng dự án
    """
    try:
        overview = FinanceService.monthly_overview(month)
        return overview
    except Exception as e:
        raise HttpError(400, f"Không thể lấy tổng quan tháng: {str(e)}")


@router.get("/profit", response=ProfitResponse, summary="Tính lợi nhuận")
def calculate_profit(
    request,
    from_date: date = Query(..., description="Từ ngày"),
    to_date: date = Query(..., description="Đến ngày")
):
    """
    Tính lợi nhuận trong khoảng thời gian.

    - **from_date**: Từ ngày
    - **to_date**: Đến ngày

    Returns:
    - Tổng doanh thu, chi phí, lợi nhuận
    - Tỷ suất lợi nhuận
    - Chi tiết từng dự án
    """
    try:
        profit = FinanceService.calculate_profit(from_date, to_date)
        return profit
    except Exception as e:
        raise HttpError(400, f"Không thể tính lợi nhuận: {str(e)}")


@router.get("/project/{project_id}", response=ProjectFinanceDetail, summary="Chi tiết tài chính dự án")
def project_finance_detail(request, project_id: str):
    """
    Lấy chi tiết tài chính của dự án.

    - **project_id**: UUID của dự án

    Returns:
    - Doanh thu, chi phí, lợi nhuận của dự án
    - Chi tiết các khoản chi phí
    """
    detail = FinanceService.project_finance_detail(project_id)
    if not detail:
        raise HttpError(404, "Không tìm thấy dự án")
    return detail


@router.get("/cash-flow/{month}", response=CashFlowResponse, summary="Dòng tiền tháng")
def cash_flow(request, month: str):
    """
    Lấy thông tin dòng tiền của tháng.

    - **month**: Tháng (YYYY-MM)

    Returns:
    - Tổng tiền vào, tiền ra
    - Số dư đầu kỳ, cuối kỳ
    - Chi tiết dòng tiền
    """
    try:
        flow = FinanceService.cash_flow(month)
        return flow
    except Exception as e:
        raise HttpError(400, f"Không thể lấy dòng tiền: {str(e)}")


@router.get("/revenue-by-package/{month}", response=RevenueByPackageResponse, summary="Doanh thu theo gói")
def revenue_by_package(request, month: str):
    """
    Lấy doanh thu theo từng gói chụp.

    - **month**: Tháng (YYYY-MM)

    Returns:
    - Danh sách gói và doanh thu tương ứng
    - Tổng doanh thu
    """
    try:
        revenue = FinanceService.revenue_by_package(month)
        return revenue
    except Exception as e:
        raise HttpError(400, f"Không thể lấy doanh thu theo gói: {str(e)}")


@router.get("/summary/{month}", response=FinancialSummaryResponse, summary="Tổng hợp tài chính")
def financial_summary(request, month: str):
    """
    Lấy tổng hợp tài chính của tháng.

    - **month**: Tháng (YYYY-MM)

    Returns:
    - Tổng hợp đầy đủ các chỉ số tài chính
    - Doanh thu, chi phí, lợi nhuận
    - Các khoản chưa thanh toán
    """
    try:
        summary = FinanceService.financial_summary(month)
        return summary
    except Exception as e:
        raise HttpError(400, f"Không thể lấy tổng hợp tài chính: {str(e)}")
