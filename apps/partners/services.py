"""
Business logic services cho Partner.
"""
from typing import Optional, List
from uuid import UUID
from django.db.models import Q
from .models import Partner
from .schemas import PartnerCreate, PartnerUpdate


class PartnerService:
    """Service class cho xử lý logic đối tác."""

    @staticmethod
    def create_partner(data: PartnerCreate, created_by=None) -> Partner:
        """
        Tạo đối tác mới.

        Args:
            data: Dữ liệu đối tác
            created_by: User tạo

        Returns:
            Partner object
        """
        partner_data = data.model_dump(
            exclude={'contact_info', 'bank_account', 'business_info', 'agreements'}
        )

        partner = Partner(**partner_data)

        if data.contact_info:
            partner.contact_info = data.contact_info.model_dump()

        if data.bank_account:
            partner.bank_account = data.bank_account.model_dump()

        if data.business_info:
            partner.business_info = data.business_info.model_dump(mode='json')

        if data.agreements:
            partner.agreements = [agreement.model_dump(mode='json') for agreement in data.agreements]

        if created_by:
            partner.created_by = created_by

        partner.save()
        return partner

    @staticmethod
    def update_partner(partner_id: UUID, data: PartnerUpdate) -> Optional[Partner]:
        """
        Cập nhật thông tin đối tác.

        Args:
            partner_id: ID đối tác
            data: Dữ liệu cập nhật

        Returns:
            Partner object hoặc None
        """
        try:
            partner = Partner.objects.get(id=partner_id)
        except Partner.DoesNotExist:
            return None

        update_data = data.model_dump(
            exclude_unset=True,
            exclude={'contact_info', 'bank_account', 'business_info', 'agreements'}
        )

        for field, value in update_data.items():
            setattr(partner, field, value)

        # Update nested fields
        if data.contact_info is not None:
            partner.contact_info = data.contact_info.model_dump()

        if data.bank_account is not None:
            partner.bank_account = data.bank_account.model_dump()

        if data.business_info is not None:
            partner.business_info = data.business_info.model_dump(mode='json')

        if data.agreements is not None:
            partner.agreements = [agreement.model_dump(mode='json') for agreement in data.agreements]

        partner.save()
        return partner

    @staticmethod
    def get_partner(partner_id: UUID) -> Optional[Partner]:
        """
        Lấy thông tin đối tác theo ID.

        Args:
            partner_id: ID đối tác

        Returns:
            Partner object hoặc None
        """
        try:
            return Partner.objects.get(id=partner_id)
        except Partner.DoesNotExist:
            return None

    @staticmethod
    def list_partners(
        type: Optional[str] = None,
        is_active: Optional[bool] = None,
        min_rating: Optional[float] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Partner], int]:
        """
        Lấy danh sách đối tác với filter.

        Args:
            type: Filter theo loại
            is_active: Filter theo trạng thái
            min_rating: Đánh giá tối thiểu
            search: Tìm kiếm theo tên
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa

        Returns:
            Tuple (danh sách đối tác, tổng số)
        """
        queryset = Partner.objects.all()

        # Apply filters
        if type:
            queryset = queryset.filter(type=type)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if min_rating is not None:
            queryset = queryset.filter(rating__gte=min_rating)

        if search:
            queryset = queryset.filter(Q(name__icontains=search))

        total = queryset.count()
        partners = list(queryset[skip:skip + limit])

        return partners, total

    @staticmethod
    def delete_partner(partner_id: UUID) -> bool:
        """
        Xóa đối tác (soft delete).

        Args:
            partner_id: ID đối tác

        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        try:
            partner = Partner.objects.get(id=partner_id)
            partner.is_active = False
            partner.save()
            return True
        except Partner.DoesNotExist:
            return False

    @staticmethod
    def get_partners_by_type(type: str) -> List[Partner]:
        """
        Lấy danh sách đối tác theo loại.

        Args:
            type: Loại đối tác

        Returns:
            Danh sách đối tác
        """
        return list(Partner.objects.filter(type=type, is_active=True))

    @staticmethod
    def update_statistics(partner_id: UUID, project_cost: float) -> Optional[Partner]:
        """
        Cập nhật thống kê đối tác.

        Args:
            partner_id: ID đối tác
            project_cost: Chi phí dự án

        Returns:
            Partner object hoặc None
        """
        try:
            partner = Partner.objects.get(id=partner_id)
            partner.projects_count += 1
            partner.total_revenue += project_cost
            partner.save()
            return partner
        except Partner.DoesNotExist:
            return None

    @staticmethod
    def update_rating(partner_id: UUID, new_rating: float) -> Optional[Partner]:
        """
        Cập nhật đánh giá đối tác.

        Args:
            partner_id: ID đối tác
            new_rating: Đánh giá mới

        Returns:
            Partner object hoặc None
        """
        try:
            partner = Partner.objects.get(id=partner_id)
            # Calculate average rating
            if partner.projects_count > 0:
                partner.rating = (partner.rating * (partner.projects_count - 1) + new_rating) / partner.projects_count
            else:
                partner.rating = new_rating
            partner.save()
            return partner
        except Partner.DoesNotExist:
            return None
