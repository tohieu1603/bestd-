"""
API endpoints cho Salary management.
"""
from typing import Optional
from uuid import UUID
from datetime import date
from ninja import Router, Query
from ninja.errors import HttpError
from .schemas import (
    SalaryCreate, SalaryUpdate, SalaryRead, SalaryList,
    MonthlySalaryRead, MonthlySalaryList,
    CalculateSalaryRequest, SalaryReportResponse
)
from .services import SalaryService

router = Router(tags=["Salaries"])


@router.post("/", response={201: SalaryRead}, summary="Tạo salary mới")
def create_salary(request, payload: SalaryCreate):
    """
    Tạo salary mới.

    - **employee**: ID nhân viên (bắt buộc)
    - **project**: ID dự án (bắt buộc)
    - **month**: Tháng YYYY-MM (bắt buộc)
    - **amount**: Số tiền (bắt buộc)
    - **work_type**: Loại công việc (bắt buộc)
    """
    try:
        salary = SalaryService.create_salary(payload, created_by=request.user)
        return 201, salary
    except Exception as e:
        raise HttpError(400, f"Không thể tạo salary: {str(e)}")


@router.get("/", response=SalaryList, summary="Lấy danh sách salary")
def list_salaries(request):
    """
    Lấy danh sách salary với các filter options.

    - **employee**: Filter theo nhân viên
    - **project**: Filter theo dự án
    - **month**: Filter theo tháng (YYYY-MM)
    - **is_paid**: Filter theo trạng thái thanh toán
    - **skip**: Phân trang - bỏ qua
    - **limit**: Phân trang - giới hạn
    """
    # Extract parameters manually from request.GET
    employee = request.GET.get('employee', None)
    project = request.GET.get('project', None)
    month = request.GET.get('month', None)
    is_paid = request.GET.get('is_paid', None)
    skip = int(request.GET.get('skip', 0))
    limit = int(request.GET.get('limit', 20))

    salaries, total = SalaryService.list_salaries(
        employee=employee,
        project=project,
        month=month,
        is_paid=is_paid,
        skip=skip,
        limit=limit
    )
    return {"total": total, "items": salaries}


@router.get("/{salary_id}", response=SalaryRead, summary="Lấy thông tin salary")
def get_salary(request, salary_id: UUID):
    """
    Lấy thông tin chi tiết của một salary.

    - **salary_id**: UUID của salary
    """
    salary = SalaryService.get_salary(salary_id)
    if not salary:
        raise HttpError(404, "Không tìm thấy salary")
    return salary


@router.put("/{salary_id}", response=SalaryRead, summary="Cập nhật salary")
def update_salary(request, salary_id: UUID, payload: SalaryUpdate):
    """
    Cập nhật thông tin salary.

    - **salary_id**: UUID của salary
    - **payload**: Dữ liệu cần cập nhật
    """
    salary = SalaryService.update_salary(salary_id, payload)
    if not salary:
        raise HttpError(404, "Không tìm thấy salary")
    return salary


@router.delete("/{salary_id}", response={200: dict}, summary="Xóa salary")
def delete_salary(request, salary_id: UUID):
    """
    Xóa salary.

    - **salary_id**: UUID của salary
    """
    success = SalaryService.delete_salary(salary_id)
    if not success:
        raise HttpError(404, "Không tìm thấy salary")
    return {"success": True, "message": "Đã xóa salary thành công"}


@router.post("/calculate-monthly", response=MonthlySalaryRead, summary="Tính lương tháng")
def calculate_monthly_salary(request, payload: CalculateSalaryRequest):
    """
    Tính lương tháng cho nhân viên.

    - **employee**: ID nhân viên
    - **month**: Tháng (YYYY-MM)
    """
    try:
        monthly_salary = SalaryService.calculate_monthly_salary(
            employee_id=payload.employee,
            month=payload.month,
            created_by=request.user
        )
        return monthly_salary
    except Exception as e:
        raise HttpError(400, f"Không thể tính lương: {str(e)}")


@router.get("/report/{month}", response=SalaryReportResponse, summary="Báo cáo lương tháng")
def generate_report(request, month: str):
    """
    Tạo báo cáo lương tháng.

    - **month**: Tháng (YYYY-MM)
    """
    try:
        report = SalaryService.generate_report(month)
        return report
    except Exception as e:
        raise HttpError(400, f"Không thể tạo báo cáo: {str(e)}")


@router.get("/employee/{employee_id}/history", response=list[MonthlySalaryRead], summary="Lịch sử lương nhân viên")
def get_employee_salary_history(request, employee_id: UUID):
    """
    Lấy lịch sử lương của nhân viên.

    - **employee_id**: ID nhân viên
    """
    history = SalaryService.get_employee_salary_history(employee_id)
    return history


@router.post("/monthly/{monthly_salary_id}/mark-paid", response=MonthlySalaryRead, summary="Đánh dấu đã thanh toán")
def mark_as_paid(
    request,
    monthly_salary_id: UUID,
    paid_date: date = Query(..., description="Ngày thanh toán"),
    payment_method: str = Query(..., description="Phương thức thanh toán")
):
    """
    Đánh dấu lương đã thanh toán.

    - **monthly_salary_id**: ID monthly salary
    - **paid_date**: Ngày thanh toán
    - **payment_method**: Phương thức thanh toán
    """
    monthly_salary = SalaryService.mark_as_paid(monthly_salary_id, paid_date, payment_method)
    if not monthly_salary:
        raise HttpError(404, "Không tìm thấy monthly salary")
    return monthly_salary
