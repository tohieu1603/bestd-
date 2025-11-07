"""
API endpoints cho Project management.
"""
from typing import Optional
from uuid import UUID
from datetime import date
from ninja import Router, Query
from ninja.errors import HttpError
from api.main import AuthBearer
from api.permissions import require_roles, require_auth
from .schemas import (
    ProjectCreate, ProjectUpdate, ProjectRead, ProjectList,
    AddMilestoneRequest, UpdateProgressRequest, AddPaymentRequest
)
from .services import ProjectService

router = Router(tags=["Projects"])


@router.post("/", response={201: ProjectRead}, auth=AuthBearer(), summary="Tạo dự án mới")
def create_project(request, payload: ProjectCreate):
    """
    Tạo dự án mới.

    - **customer_name**: Tên khách hàng (bắt buộc)
    - **customer_phone**: Số điện thoại (bắt buộc)
    - **package_type**: ID gói chụp (bắt buộc)
    - **shoot_date**: Ngày chụp (bắt buộc)
    - **team**: Đội ngũ thực hiện
    - **partners**: Đối tác
    - **payment**: Thông tin thanh toán
    """
    try:
        # Only pass created_by if user is authenticated
        created_by = request.user if request.user.is_authenticated else None
        project = ProjectService.create_project(payload, created_by=created_by)
        return 201, project
    except Exception as e:
        raise HttpError(400, f"Không thể tạo dự án: {str(e)}")


@router.get("/", response=ProjectList, auth=AuthBearer(), summary="Lấy danh sách dự án")
def list_projects(request):
    """
    Lấy danh sách dự án với các filter options.

    - **status**: Filter theo trạng thái (pending, in-progress, completed, cancelled)
    - **payment_status**: Filter theo trạng thái thanh toán (unpaid, deposit, paid)
    - **from_date**: Filter từ ngày chụp
    - **to_date**: Filter đến ngày chụp
    - **customer_name**: Tìm kiếm theo tên hoặc số điện thoại khách hàng
    - **skip**: Phân trang - bỏ qua
    - **limit**: Phân trang - giới hạn
    """
    # Extract parameters manually from request.GET
    status = request.GET.get('status', None)
    payment_status = request.GET.get('payment_status', None)
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)
    customer_name = request.GET.get('customer_name', None)
    skip = int(request.GET.get('skip', 0))
    limit = int(request.GET.get('limit', 20))

    projects, total = ProjectService.list_projects(
        status=status,
        payment_status=payment_status,
        from_date=from_date,
        to_date=to_date,
        customer_name=customer_name,
        skip=skip,
        limit=limit
    )
    return {"total": total, "items": projects}


@router.get("/{project_id}", response=ProjectRead, summary="Lấy thông tin dự án")
def get_project(request, project_id: UUID):
    """
    Lấy thông tin chi tiết của một dự án.

    - **project_id**: UUID của dự án
    """
    project = ProjectService.get_project(project_id)
    if not project:
        raise HttpError(404, "Không tìm thấy dự án")
    return project


@router.put("/{project_id}", response=ProjectRead, summary="Cập nhật dự án")
def update_project(request, project_id: UUID, payload: ProjectUpdate):
    """
    Cập nhật thông tin dự án.

    - **project_id**: UUID của dự án
    - **payload**: Dữ liệu cần cập nhật
    """
    project = ProjectService.update_project(project_id, payload, updated_by=request.user)
    if not project:
        raise HttpError(404, "Không tìm thấy dự án")
    return project


@router.patch("/{project_id}", response=ProjectRead, auth=AuthBearer(), summary="Cập nhật một phần dự án")
def partial_update_project(request, project_id: UUID, payload: ProjectUpdate):
    """
    Cập nhật một phần thông tin dự án.

    - **project_id**: UUID của dự án
    - **payload**: Dữ liệu cần cập nhật (chỉ cần truyền fields muốn cập nhật)

    Permissions:
    - Status updates to 'confirmed': Requires admin or Manager role
    - Other updates: Requires authentication
    """
    # Check if trying to confirm project (set status to 'confirmed')
    if payload.status == 'confirmed':
        # Get user from auth
        user = request.auth
        user_role = getattr(user, 'role', None) if user else None
        if user_role not in ['admin', 'manager']:
            raise HttpError(403, "Chỉ admin hoặc Manager mới có thể xác nhận dự án")

        # Use the authenticated user for update
        project = ProjectService.update_project(project_id, payload, updated_by=user)
    else:
        # For non-confirmation updates, use request.auth
        project = ProjectService.update_project(project_id, payload, updated_by=request.auth)

    if not project:
        raise HttpError(404, "Không tìm thấy dự án")
    return project


@router.delete("/{project_id}", response={200: dict}, auth=AuthBearer(), summary="Xóa dự án")
@require_roles('admin', 'Manager')
def delete_project(request, project_id: UUID):
    """
    Xóa dự án (set status = cancelled).

    - **project_id**: UUID của dự án
    """
    success = ProjectService.delete_project(project_id)
    if not success:
        raise HttpError(404, "Không tìm thấy dự án")
    return {"success": True, "message": "Đã hủy dự án thành công"}


@router.post("/{project_id}/milestones", response=ProjectRead, summary="Thêm milestone")
def add_milestone(request, project_id: UUID, payload: AddMilestoneRequest):
    """
    Thêm milestone vào dự án.

    - **project_id**: UUID của dự án
    - **milestone**: Thông tin milestone
    """
    project = ProjectService.add_milestone(project_id, payload.milestone)
    if not project:
        raise HttpError(404, "Không tìm thấy dự án")
    return project


@router.put("/{project_id}/progress", response=ProjectRead, summary="Cập nhật tiến độ")
def update_progress(request, project_id: UUID, payload: UpdateProgressRequest):
    """
    Cập nhật tiến độ dự án.

    - **project_id**: UUID của dự án
    - **progress**: Thông tin tiến độ (shooting_done, retouch_done, delivered)
    """
    project = ProjectService.update_progress(project_id, payload.progress)
    if not project:
        raise HttpError(404, "Không tìm thấy dự án")
    return project


@router.post("/{project_id}/payments", response=ProjectRead, summary="Thêm thanh toán")
def add_payment(request, project_id: UUID, payload: AddPaymentRequest):
    """
    Thêm thanh toán vào dự án.

    - **project_id**: UUID của dự án
    - **payment_item**: Thông tin thanh toán (amount, date, method, notes)
    """
    project = ProjectService.add_payment(project_id, payload.payment_item)
    if not project:
        raise HttpError(404, "Không tìm thấy dự án")
    return project


@router.get("/status/{status}", response=list[ProjectRead], summary="Lấy dự án theo trạng thái")
def get_projects_by_status(request, status: str):
    """
    Lấy danh sách dự án theo trạng thái cụ thể.

    - **status**: Trạng thái dự án (pending, in-progress, completed, cancelled)
    """
    projects = ProjectService.get_projects_by_status(status)
    return projects


@router.get("/upcoming/list", response=list[ProjectRead], summary="Lấy dự án sắp tới")
def get_upcoming_projects(request, days: int = Query(7, ge=1, le=30)):
    """
    Lấy danh sách dự án sắp tới trong X ngày.

    - **days**: Số ngày tới (mặc định 7)
    """
    projects = ProjectService.get_upcoming_projects(days)
    return projects
