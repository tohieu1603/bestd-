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
    MonthlySalaryCreate, MonthlySalaryUpdate, MonthlySalaryRead, MonthlySalaryList,
    CalculateSalaryRequest, SalaryReportResponse
)
from .services import SalaryService

router = Router(tags=["Salaries"])


# ========== Monthly Salary Endpoints (for frontend) ==========
@router.post("/", response={201: MonthlySalaryRead}, summary="Tạo bảng lương tháng")
def create_monthly_salary(request, payload: MonthlySalaryCreate):
    """
    Tạo bảng lương tháng mới.

    - **employee_id**: ID nhân viên (bắt buộc)
    - **month**: Tháng YYYY-MM (bắt buộc)
    - **base_salary**: Lương cơ bản
    - **bonus**: Thưởng
    - **deduction**: Khấu trừ
    - **total_amount**: Tổng lương (bắt buộc)
    - **projects_detail**: Chi tiết dự án tham gia
    - **status**: Trạng thái (pending/paid/cancelled)
    """
    try:
        # Pass authenticated user or None
        created_by = request.user if request.user.is_authenticated else None
        monthly_salary = SalaryService.create_monthly_salary(payload, created_by=created_by)
        return 201, monthly_salary
    except Exception as e:
        raise HttpError(400, f"Không thể tạo bảng lương: {str(e)}")


@router.get("/", response=MonthlySalaryList, summary="Lấy danh sách bảng lương tháng")
def list_monthly_salaries(request):
    """
    Lấy danh sách bảng lương tháng.

    - **month**: Filter theo tháng (YYYY-MM)
    - **status**: Filter theo trạng thái (pending/paid/cancelled)
    - **skip**: Phân trang - bỏ qua
    - **limit**: Phân trang - giới hạn
    """
    month = request.GET.get('month', None)
    status = request.GET.get('status', None)
    skip = int(request.GET.get('skip', 0))
    limit = int(request.GET.get('limit', 20))

    salaries, total = SalaryService.list_monthly_salaries(
        month=month,
        status=status,
        skip=skip,
        limit=limit
    )

    # Convert to response format
    results = []
    for salary in salaries:
        results.append({
            'id': salary.id,
            'employee': {
                'id': salary.employee.id,
                'name': salary.employee.name
            },
            'month': salary.month,
            'base_salary': float(salary.base_salary),
            'bonus': float(salary.bonus),
            'deduction': float(salary.deduction),
            'total_amount': float(salary.total_amount),
            'projects_detail': salary.projects_detail,
            'status': salary.status,
            'payment_date': salary.payment_date,
            'payment_method': salary.payment_method,
            'notes': salary.notes,
            'created_at': salary.created_at,
            'updated_at': salary.updated_at
        })

    return {"total": total, "results": results}


@router.get("/{salary_id}", response=MonthlySalaryRead, summary="Lấy thông tin bảng lương")
def get_monthly_salary(request, salary_id: UUID):
    """
    Lấy thông tin chi tiết của một bảng lương tháng.

    - **salary_id**: UUID của bảng lương
    """
    salary = SalaryService.get_monthly_salary(salary_id)
    if not salary:
        raise HttpError(404, "Không tìm thấy bảng lương")
    return salary


@router.put("/{salary_id}", response=MonthlySalaryRead, summary="Cập nhật bảng lương")
def update_monthly_salary(request, salary_id: UUID, payload: MonthlySalaryUpdate):
    """
    Cập nhật thông tin bảng lương tháng.

    - **salary_id**: UUID của bảng lương
    - **payload**: Dữ liệu cần cập nhật
    """
    salary = SalaryService.update_monthly_salary(salary_id, payload)
    if not salary:
        raise HttpError(404, "Không tìm thấy bảng lương")
    return salary


@router.delete("/{salary_id}", response={200: dict}, summary="Xóa bảng lương")
def delete_monthly_salary(request, salary_id: UUID):
    """
    Xóa bảng lương tháng.

    - **salary_id**: UUID của bảng lương
    """
    success = SalaryService.delete_monthly_salary(salary_id)
    if not success:
        raise HttpError(404, "Không tìm thấy bảng lương")
    return {"success": True, "message": "Đã xóa bảng lương thành công"}


# ========== Project Salary Endpoints (old) ==========
@router.post("/project-salary/", response={201: SalaryRead}, summary="Tạo lương theo dự án")
def create_salary(request, payload: SalaryCreate):
    """
    Tạo salary theo dự án.

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


@router.get("/project-salary/", response=SalaryList, summary="Lấy danh sách lương theo dự án")
def list_salaries(request):
    """
    Lấy danh sách salary theo dự án với các filter options.

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


@router.get("/project-salary/{salary_id}", response=SalaryRead, summary="Lấy thông tin lương dự án")
def get_salary(request, salary_id: UUID):
    """
    Lấy thông tin chi tiết của một salary theo dự án.

    - **salary_id**: UUID của salary
    """
    salary = SalaryService.get_salary(salary_id)
    if not salary:
        raise HttpError(404, "Không tìm thấy salary")
    return salary


@router.put("/project-salary/{salary_id}", response=SalaryRead, summary="Cập nhật lương dự án")
def update_salary(request, salary_id: UUID, payload: SalaryUpdate):
    """
    Cập nhật thông tin salary theo dự án.

    - **salary_id**: UUID của salary
    - **payload**: Dữ liệu cần cập nhật
    """
    salary = SalaryService.update_salary(salary_id, payload)
    if not salary:
        raise HttpError(404, "Không tìm thấy salary")
    return salary


@router.delete("/project-salary/{salary_id}", response={200: dict}, summary="Xóa lương dự án")
def delete_salary(request, salary_id: UUID):
    """
    Xóa salary theo dự án.

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
