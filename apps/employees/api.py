"""
API endpoints cho Employee management.
"""
from typing import Optional
from uuid import UUID
from ninja import Router, Query
from ninja.errors import HttpError
from api.main import AuthBearer
from api.permissions import require_roles, require_auth
from .schemas import (
    EmployeeCreate, EmployeeUpdate, EmployeeRead,
    EmployeeList, EmployeeFilter
)
from .services import EmployeeService

router = Router(tags=["Employees"])


@router.post("/debug", auth=AuthBearer(), summary="Debug endpoint")
def debug_create(request):
    """Debug endpoint to see raw request body."""
    import json
    body = json.loads(request.body)
    print(f"Raw request body: {json.dumps(body, indent=2)}")
    return {"received": body}


@router.post("/", response={201: EmployeeRead}, auth=AuthBearer(), summary="Tạo nhân viên mới")
@require_roles('admin', 'Manager')
def create_employee(request, payload: EmployeeCreate):
    """
    Tạo nhân viên mới.

    - **name**: Tên nhân viên (bắt buộc)
    - **role**: Vai trò (bắt buộc)
    - **skills**: Danh sách kỹ năng
    - **phone**: Số điện thoại
    - **email**: Email
    - **base_salary**: Lương cơ bản
    """
    try:
        # request.auth contains the authenticated user from AuthBearer
        import json
        print(f"Received payload: {json.dumps(payload.model_dump(), indent=2, default=str)}")
        employee = EmployeeService.create_employee(payload, created_by=request.auth)
        return 201, employee
    except Exception as e:
        import traceback
        print(f"Error creating employee: {str(e)}")
        print(traceback.format_exc())
        raise HttpError(400, f"Không thể tạo nhân viên: {str(e)}")


@router.get("/", response=EmployeeList, summary="Lấy danh sách nhân viên")
def list_employees(request):
    """
    Lấy danh sách nhân viên với các filter options.

    - **role**: Filter theo vai trò
    - **is_active**: Filter theo trạng thái hoạt động
    - **search**: Tìm kiếm theo tên, email hoặc số điện thoại
    - **skip**: Phân trang - bỏ qua
    - **limit**: Phân trang - giới hạn
    """
    # Extract parameters manually from request.GET
    role = request.GET.get('role', None)
    is_active = request.GET.get('is_active', None)
    search = request.GET.get('search', None)
    skip = int(request.GET.get('skip', 0))
    limit = int(request.GET.get('limit', 20))

    employees, total = EmployeeService.list_employees(
        role=role,
        is_active=is_active,
        search=search,
        skip=skip,
        limit=limit
    )
    return {"total": total, "items": employees}


@router.get("/{employee_id}", response=EmployeeRead, summary="Lấy thông tin nhân viên")
def get_employee(request, employee_id: UUID):
    """
    Lấy thông tin chi tiết của một nhân viên.

    - **employee_id**: UUID của nhân viên
    """
    employee = EmployeeService.get_employee(employee_id)
    if not employee:
        raise HttpError(404, "Không tìm thấy nhân viên")
    return employee


@router.put("/{employee_id}", response=EmployeeRead, summary="Cập nhật nhân viên")
@require_roles('admin', 'Manager')
def update_employee(request, employee_id: UUID, payload: EmployeeUpdate):
    """
    Cập nhật thông tin nhân viên.

    - **employee_id**: UUID của nhân viên
    - **payload**: Dữ liệu cần cập nhật
    """
    employee = EmployeeService.update_employee(employee_id, payload)
    if not employee:
        raise HttpError(404, "Không tìm thấy nhân viên")
    return employee


@router.patch("/{employee_id}", response=EmployeeRead, summary="Cập nhật một phần nhân viên")
def partial_update_employee(request, employee_id: UUID, payload: EmployeeUpdate):
    """
    Cập nhật một phần thông tin nhân viên.

    - **employee_id**: UUID của nhân viên
    - **payload**: Dữ liệu cần cập nhật (chỉ cần truyền fields muốn cập nhật)
    """
    employee = EmployeeService.update_employee(employee_id, payload)
    if not employee:
        raise HttpError(404, "Không tìm thấy nhân viên")
    return employee


@router.delete("/{employee_id}", response={200: dict}, summary="Xóa nhân viên")
@require_roles('admin')
def delete_employee(request, employee_id: UUID):
    """
    Xóa nhân viên (soft delete - set is_active = False).

    - **employee_id**: UUID của nhân viên
    """
    success = EmployeeService.delete_employee(employee_id)
    if not success:
        raise HttpError(404, "Không tìm thấy nhân viên")
    return {"success": True, "message": "Đã xóa nhân viên thành công"}


@router.get("/role/{role}", response=list[EmployeeRead], summary="Lấy nhân viên theo vai trò")
def get_employees_by_role(request, role: str):
    """
    Lấy danh sách nhân viên theo vai trò cụ thể.

    - **role**: Vai trò cần filter
    """
    employees = EmployeeService.get_employees_by_role(role)
    return employees


@router.get("/active/all", response=list[EmployeeRead], summary="Lấy tất cả nhân viên active")
def get_active_employees(request):
    """
    Lấy tất cả nhân viên đang hoạt động.
    """
    employees = EmployeeService.get_active_employees()
    return employees
