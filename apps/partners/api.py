"""
API endpoints cho Partner management.
"""
from typing import Optional
from uuid import UUID
from ninja import Router, Query
from ninja.errors import HttpError
from .schemas import PartnerCreate, PartnerUpdate, PartnerRead, PartnerList
from .services import PartnerService

router = Router(tags=["Partners"])


@router.post("/", response={201: PartnerRead}, summary="Tạo đối tác mới")
def create_partner(request, payload: PartnerCreate):
    """
    Tạo đối tác mới.

    - **name**: Tên đối tác (bắt buộc)
    - **type**: Loại đối tác (bắt buộc)
    - **cost**: Chi phí (bắt buộc)
    - **contact_info**: Thông tin liên hệ
    - **bank_account**: Thông tin ngân hàng
    - **business_info**: Thông tin doanh nghiệp
    """
    try:
        partner = PartnerService.create_partner(payload, created_by=request.user)
        return 201, partner
    except Exception as e:
        raise HttpError(400, f"Không thể tạo đối tác: {str(e)}")


@router.get("/", response=PartnerList, summary="Lấy danh sách đối tác")
def list_partners(request):
    """
    Lấy danh sách đối tác với các filter options.

    - **type**: Filter theo loại
    - **is_active**: Filter theo trạng thái hoạt động
    - **min_rating**: Filter đánh giá tối thiểu
    - **search**: Tìm kiếm theo tên
    - **skip**: Phân trang - bỏ qua
    - **limit**: Phân trang - giới hạn
    """
    # Extract parameters manually from request.GET
    type_param = request.GET.get('type', None)
    is_active = request.GET.get('is_active', None)
    min_rating = float(request.GET.get('min_rating')) if request.GET.get('min_rating') else None
    search = request.GET.get('search', None)
    skip = int(request.GET.get('skip', 0))
    limit = int(request.GET.get('limit', 20))

    partners, total = PartnerService.list_partners(
        type=type_param,
        is_active=is_active,
        min_rating=min_rating,
        search=search,
        skip=skip,
        limit=limit
    )
    return {"total": total, "items": partners}


@router.get("/{partner_id}", response=PartnerRead, summary="Lấy thông tin đối tác")
def get_partner(request, partner_id: UUID):
    """
    Lấy thông tin chi tiết của một đối tác.

    - **partner_id**: UUID của đối tác
    """
    partner = PartnerService.get_partner(partner_id)
    if not partner:
        raise HttpError(404, "Không tìm thấy đối tác")
    return partner


@router.put("/{partner_id}", response=PartnerRead, summary="Cập nhật đối tác")
def update_partner(request, partner_id: UUID, payload: PartnerUpdate):
    """
    Cập nhật thông tin đối tác.

    - **partner_id**: UUID của đối tác
    - **payload**: Dữ liệu cần cập nhật
    """
    partner = PartnerService.update_partner(partner_id, payload)
    if not partner:
        raise HttpError(404, "Không tìm thấy đối tác")
    return partner


@router.patch("/{partner_id}", response=PartnerRead, summary="Cập nhật một phần đối tác")
def partial_update_partner(request, partner_id: UUID, payload: PartnerUpdate):
    """
    Cập nhật một phần thông tin đối tác.

    - **partner_id**: UUID của đối tác
    - **payload**: Dữ liệu cần cập nhật (chỉ cần truyền fields muốn cập nhật)
    """
    partner = PartnerService.update_partner(partner_id, payload)
    if not partner:
        raise HttpError(404, "Không tìm thấy đối tác")
    return partner


@router.delete("/{partner_id}", response={200: dict}, summary="Xóa đối tác")
def delete_partner(request, partner_id: UUID):
    """
    Xóa đối tác (soft delete).

    - **partner_id**: UUID của đối tác
    """
    success = PartnerService.delete_partner(partner_id)
    if not success:
        raise HttpError(404, "Không tìm thấy đối tác")
    return {"success": True, "message": "Đã xóa đối tác thành công"}


@router.get("/type/{type}", response=list[PartnerRead], summary="Lấy đối tác theo loại")
def get_partners_by_type(request, type: str):
    """
    Lấy danh sách đối tác theo loại cụ thể.

    - **type**: Loại đối tác cần filter
    """
    partners = PartnerService.get_partners_by_type(type)
    return partners


@router.post("/{partner_id}/update-statistics", response=PartnerRead, summary="Cập nhật thống kê")
def update_statistics(request, partner_id: UUID, project_cost: float):
    """
    Cập nhật thống kê đối tác khi hoàn thành dự án.

    - **partner_id**: UUID của đối tác
    - **project_cost**: Chi phí dự án
    """
    partner = PartnerService.update_statistics(partner_id, project_cost)
    if not partner:
        raise HttpError(404, "Không tìm thấy đối tác")
    return partner


@router.post("/{partner_id}/update-rating", response=PartnerRead, summary="Cập nhật đánh giá")
def update_rating(request, partner_id: UUID, rating: float = Query(..., ge=0, le=5)):
    """
    Cập nhật đánh giá đối tác.

    - **partner_id**: UUID của đối tác
    - **rating**: Đánh giá mới (0-5)
    """
    partner = PartnerService.update_rating(partner_id, rating)
    if not partner:
        raise HttpError(404, "Không tìm thấy đối tác")
    return partner
