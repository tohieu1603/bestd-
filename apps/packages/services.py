"""
Business logic services cho Package.
"""
from typing import Optional, List
from uuid import UUID
from django.db.models import Q
from .models import Package
from .schemas import PackageCreate, PackageUpdate


class PackageService:
    """Service class cho xử lý logic gói chụp."""

    @staticmethod
    def create_package(data: PackageCreate, created_by=None) -> Package:
        """
        Tạo gói chụp mới.

        Args:
            data: Dữ liệu gói chụp
            created_by: User tạo

        Returns:
            Package object
        """
        package_data = data.model_dump(exclude={'details', 'includes'})

        package = Package(**package_data)

        # Ensure notes has a value (database constraint)
        if not package.notes:
            package.notes = ''

        if data.details:
            package.details = data.details.model_dump()

        if data.includes:
            package.includes = data.includes

        if created_by:
            package.created_by = created_by

        package.save()
        return package

    @staticmethod
    def update_package(package_id: UUID, data: PackageUpdate) -> Optional[Package]:
        """
        Cập nhật thông tin gói chụp.

        Args:
            package_id: ID gói chụp
            data: Dữ liệu cập nhật

        Returns:
            Package object hoặc None
        """
        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude={'details', 'includes'})

        for field, value in update_data.items():
            setattr(package, field, value)

        # Update nested fields
        if data.details is not None:
            package.details = data.details.model_dump()

        if data.includes is not None:
            package.includes = data.includes

        package.save()
        return package

    @staticmethod
    def get_package(package_id: UUID) -> Optional[Package]:
        """
        Lấy thông tin gói chụp theo ID.

        Args:
            package_id: ID gói chụp

        Returns:
            Package object hoặc None
        """
        try:
            return Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            return None

    @staticmethod
    def list_packages(
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Package], int]:
        """
        Lấy danh sách gói chụp với filter.

        Args:
            category: Filter theo danh mục
            is_active: Filter theo trạng thái
            min_price: Giá tối thiểu
            max_price: Giá tối đa
            search: Tìm kiếm theo tên
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa

        Returns:
            Tuple (danh sách gói, tổng số)
        """
        queryset = Package.objects.all()

        # Apply filters
        if category:
            queryset = queryset.filter(category=category)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        total = queryset.count()
        packages = list(queryset[skip:skip + limit])

        return packages, total

    @staticmethod
    def delete_package(package_id: UUID) -> bool:
        """
        Xóa gói chụp (soft delete).

        Args:
            package_id: ID gói chụp

        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        try:
            package = Package.objects.get(id=package_id)
            package.is_active = False
            package.save()
            return True
        except Package.DoesNotExist:
            return False

    @staticmethod
    def get_packages_by_category(category: str) -> List[Package]:
        """
        Lấy danh sách gói theo danh mục.

        Args:
            category: Danh mục

        Returns:
            Danh sách gói chụp
        """
        return list(Package.objects.filter(category=category, is_active=True))

    @staticmethod
    def get_popular_packages(limit: int = 10) -> List[Package]:
        """
        Lấy danh sách gói phổ biến.

        Args:
            limit: Số lượng gói

        Returns:
            Danh sách gói chụp phổ biến
        """
        return list(
            Package.objects.filter(is_active=True)
            .order_by('-popularity_score', '-created_at')[:limit]
        )

    @staticmethod
    def increment_popularity(package_id: UUID) -> Optional[Package]:
        """
        Tăng điểm phổ biến của gói.

        Args:
            package_id: ID gói chụp

        Returns:
            Package object hoặc None
        """
        try:
            package = Package.objects.get(id=package_id)
            package.popularity_score += 1
            package.save()
            return package
        except Package.DoesNotExist:
            return None
