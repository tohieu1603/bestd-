"""
API endpoints cho Package management.
"""
from typing import Optional
from uuid import UUID
from ninja import Router, Query
from ninja.errors import HttpError
from .schemas import PackageCreate, PackageUpdate, PackageRead, PackageList
from .services import PackageService

router = Router(tags=["Packages"])


@router.post("/", response={201: PackageRead}, summary="Tạo gói chụp mới")
def create_package(request, payload: PackageCreate):
    """
    Tạo gói chụp mới.

    - **name**: Tên gói (bắt buộc)
    - **category**: Danh mục (bắt buộc)
    - **price**: Giá (bắt buộc)
    - **details**: Chi tiết gói
    - **includes**: Danh sách dịch vụ bao gồm
    """
    try:
        # Only pass created_by if user is authenticated
        created_by = request.user if request.user.is_authenticated else None
        package = PackageService.create_package(payload, created_by=created_by)
        return 201, package
    except Exception as e:
        raise HttpError(400, f"Không thể tạo gói chụp: {str(e)}")


@router.get("/", response=PackageList, summary="Lấy danh sách gói chụp")
def list_packages(request):
    """
    Lấy danh sách gói chụp với các filter options.

    - **category**: Filter theo danh mục
    - **is_active**: Filter theo trạng thái hoạt động
    - **min_price**: Filter giá tối thiểu
    - **max_price**: Filter giá tối đa
    - **search**: Tìm kiếm theo tên hoặc mô tả
    - **skip**: Phân trang - bỏ qua
    - **limit**: Phân trang - giới hạn
    """
    # Extract parameters manually from request.GET
    category = request.GET.get('category', None)
    is_active = request.GET.get('is_active', None)
    min_price = float(request.GET.get('min_price')) if request.GET.get('min_price') else None
    max_price = float(request.GET.get('max_price')) if request.GET.get('max_price') else None
    search = request.GET.get('search', None)
    skip = int(request.GET.get('skip', 0))
    limit = int(request.GET.get('limit', 20))

    packages, total = PackageService.list_packages(
        category=category,
        is_active=is_active,
        min_price=min_price,
        max_price=max_price,
        search=search,
        skip=skip,
        limit=limit
    )
    return {"total": total, "items": packages}


@router.get("/{package_id}", response=PackageRead, summary="Lấy thông tin gói chụp")
def get_package(request, package_id: UUID):
    """
    Lấy thông tin chi tiết của một gói chụp.

    - **package_id**: UUID của gói chụp
    """
    package = PackageService.get_package(package_id)
    if not package:
        raise HttpError(404, "Không tìm thấy gói chụp")
    return package


@router.put("/{package_id}", response=PackageRead, summary="Cập nhật gói chụp")
def update_package(request, package_id: UUID, payload: PackageUpdate):
    """
    Cập nhật thông tin gói chụp.

    - **package_id**: UUID của gói chụp
    - **payload**: Dữ liệu cần cập nhật
    """
    package = PackageService.update_package(package_id, payload)
    if not package:
        raise HttpError(404, "Không tìm thấy gói chụp")
    return package


@router.patch("/{package_id}", response=PackageRead, summary="Cập nhật một phần gói chụp")
def partial_update_package(request, package_id: UUID, payload: PackageUpdate):
    """
    Cập nhật một phần thông tin gói chụp.

    - **package_id**: UUID của gói chụp
    - **payload**: Dữ liệu cần cập nhật (chỉ cần truyền fields muốn cập nhật)
    """
    package = PackageService.update_package(package_id, payload)
    if not package:
        raise HttpError(404, "Không tìm thấy gói chụp")
    return package


@router.delete("/{package_id}", response={200: dict}, summary="Xóa gói chụp")
def delete_package(request, package_id: UUID):
    """
    Xóa gói chụp (soft delete).

    - **package_id**: UUID của gói chụp
    """
    success = PackageService.delete_package(package_id)
    if not success:
        raise HttpError(404, "Không tìm thấy gói chụp")
    return {"success": True, "message": "Đã xóa gói chụp thành công"}


@router.get("/category/{category}", response=list[PackageRead], summary="Lấy gói theo danh mục")
def get_packages_by_category(request, category: str):
    """
    Lấy danh sách gói chụp theo danh mục cụ thể.

    - **category**: Danh mục cần filter
    """
    packages = PackageService.get_packages_by_category(category)
    return packages


@router.get("/popular/top", response=list[PackageRead], summary="Lấy gói phổ biến")
def get_popular_packages(request, limit: int = Query(10, ge=1, le=50)):
    """
    Lấy danh sách gói chụp phổ biến.

    - **limit**: Số lượng gói (mặc định 10)
    """
    packages = PackageService.get_popular_packages(limit)
    return packages


@router.post("/{package_id}/increment-popularity", response=PackageRead, summary="Tăng điểm phổ biến")
def increment_popularity(request, package_id: UUID):
    """
    Tăng điểm phổ biến của gói (được gọi khi gói được chọn).

    - **package_id**: UUID của gói chụp
    """
    package = PackageService.increment_popularity(package_id)
    if not package:
        raise HttpError(404, "Không tìm thấy gói chụp")
    return package
