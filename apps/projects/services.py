"""
Business logic services cho Project.
"""
from typing import Optional, List
from uuid import UUID
from datetime import date
from django.db.models import Q
from .models import Project
from .schemas import (
    ProjectCreate, ProjectUpdate, MilestoneSchema,
    ProgressSchema, PaymentHistorySchema
)


class ProjectService:
    """Service class cho xử lý logic dự án."""

    @staticmethod
    def create_project(data: ProjectCreate, created_by=None) -> Project:
        """
        Tạo dự án mới.

        Args:
            data: Dữ liệu dự án
            created_by: User tạo

        Returns:
            Project object
        """
        from apps.packages.models import Package

        project_data = data.model_dump(
            exclude={'additional_packages', 'team', 'partners', 'payment', 'package_type'}
        )

        # Handle package_type ForeignKey
        if data.package_type:
            try:
                package = Package.objects.get(id=data.package_type)
                project_data['package_type'] = package
            except Package.DoesNotExist:
                project_data['package_type'] = None
        else:
            project_data['package_type'] = None

        project = Project(**project_data)

        # Handle nested data
        if data.additional_packages:
            project.additional_packages = [pkg.model_dump(mode='json') for pkg in data.additional_packages]

        if data.team:
            project.team = data.team.model_dump(mode='json')

        if data.partners:
            project.partners = data.partners.model_dump(mode='json')

        if data.payment:
            project.payment = data.payment.model_dump(mode='json')

        if created_by:
            project.created_by = created_by
            project.last_modified_by = created_by

        project.save()
        return project

    @staticmethod
    def update_project(project_id: UUID, data: ProjectUpdate, updated_by=None) -> Optional[Project]:
        """
        Cập nhật thông tin dự án.

        Args:
            project_id: ID dự án
            data: Dữ liệu cập nhật
            updated_by: User cập nhật

        Returns:
            Project object hoặc None
        """
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return None

        from apps.packages.models import Package

        update_data = data.model_dump(
            exclude_unset=True,
            exclude={'additional_packages', 'team', 'partners', 'payment', 'progress', 'milestones', 'files', 'package_type'}
        )

        for field, value in update_data.items():
            setattr(project, field, value)

        # Handle package_type ForeignKey
        if hasattr(data, 'package_type') and data.package_type is not None:
            if data.package_type:
                try:
                    package = Package.objects.get(id=data.package_type)
                    project.package_type = package
                except Package.DoesNotExist:
                    pass
            else:
                project.package_type = None

        # Update nested fields (only if they exist in the update schema)
        if hasattr(data, 'additional_packages') and data.additional_packages is not None:
            project.additional_packages = [pkg.model_dump(mode='json') for pkg in data.additional_packages]

        if hasattr(data, 'team') and data.team is not None:
            project.team = data.team.model_dump(mode='json')

        if hasattr(data, 'partners') and data.partners is not None:
            project.partners = data.partners.model_dump(mode='json')

        if hasattr(data, 'payment') and data.payment is not None:
            project.payment = data.payment.model_dump(mode='json')

        if hasattr(data, 'progress') and data.progress is not None:
            project.progress = data.progress.model_dump()

        if hasattr(data, 'milestones') and data.milestones is not None:
            project.milestones = [milestone.model_dump(mode='json') for milestone in data.milestones]

        if hasattr(data, 'files') and data.files is not None:
            project.files = [file.model_dump(mode='json') for file in data.files]

        if updated_by:
            project.last_modified_by = updated_by

        project.save()
        return project

    @staticmethod
    def get_project(project_id: UUID) -> Optional[Project]:
        """
        Lấy thông tin dự án theo ID.

        Args:
            project_id: ID dự án

        Returns:
            Project object hoặc None
        """
        try:
            return Project.objects.select_related('package_type').get(id=project_id)
        except Project.DoesNotExist:
            return None

    @staticmethod
    def list_projects(
        status: Optional[str] = None,
        payment_status: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        customer_name: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Project], int]:
        """
        Lấy danh sách dự án với filter.

        Args:
            status: Filter theo trạng thái
            payment_status: Filter theo trạng thái thanh toán
            from_date: Từ ngày
            to_date: Đến ngày
            customer_name: Tìm kiếm theo tên khách hàng
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa

        Returns:
            Tuple (danh sách dự án, tổng số)
        """
        queryset = Project.objects.select_related('package_type').all()

        # Apply filters
        if status:
            queryset = queryset.filter(status=status)

        if payment_status:
            queryset = queryset.filter(payment__status=payment_status)

        if from_date:
            queryset = queryset.filter(shoot_date__gte=from_date)

        if to_date:
            queryset = queryset.filter(shoot_date__lte=to_date)

        if customer_name:
            queryset = queryset.filter(
                Q(customer_name__icontains=customer_name) | Q(customer_phone__icontains=customer_name)
            )

        total = queryset.count()
        projects = list(queryset[skip:skip + limit])

        return projects, total

    @staticmethod
    def delete_project(project_id: UUID) -> bool:
        """
        Xóa dự án (set status = cancelled).

        Args:
            project_id: ID dự án

        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        try:
            project = Project.objects.get(id=project_id)
            project.status = 'cancelled'
            project.save()
            return True
        except Project.DoesNotExist:
            return False

    @staticmethod
    def add_milestone(project_id: UUID, milestone: MilestoneSchema) -> Optional[Project]:
        """
        Thêm milestone vào dự án.

        Args:
            project_id: ID dự án
            milestone: Dữ liệu milestone

        Returns:
            Project object hoặc None
        """
        try:
            project = Project.objects.get(id=project_id)
            if not project.milestones:
                project.milestones = []
            project.milestones.append(milestone.model_dump(mode='json'))
            project.save()
            return project
        except Project.DoesNotExist:
            return None

    @staticmethod
    def update_progress(project_id: UUID, progress: ProgressSchema) -> Optional[Project]:
        """
        Cập nhật tiến độ dự án.

        Args:
            project_id: ID dự án
            progress: Dữ liệu tiến độ

        Returns:
            Project object hoặc None
        """
        try:
            project = Project.objects.get(id=project_id)
            project.progress = progress.model_dump()

            # Auto update status based on progress
            if progress.delivered:
                project.status = 'completed'
            elif progress.retouch_done or progress.shooting_done:
                project.status = 'in-progress'

            project.save()
            return project
        except Project.DoesNotExist:
            return None

    @staticmethod
    def add_payment(project_id: UUID, payment_item: PaymentHistorySchema) -> Optional[Project]:
        """
        Thêm thanh toán vào dự án.

        Args:
            project_id: ID dự án
            payment_item: Dữ liệu thanh toán

        Returns:
            Project object hoặc None
        """
        try:
            project = Project.objects.get(id=project_id)
            if not project.payment:
                project.payment = {
                    'status': 'unpaid',
                    'deposit': 0,
                    'final': 0,
                    'paid': 0,
                    'payment_history': []
                }

            # Add to history
            project.payment['payment_history'].append(payment_item.model_dump(mode='json'))

            # Update paid amount
            project.payment['paid'] += payment_item.amount

            # Update status
            if project.payment['paid'] >= project.package_final_price:
                project.payment['status'] = 'paid'
            elif project.payment['paid'] > 0:
                project.payment['status'] = 'deposit'

            project.save()
            return project
        except Project.DoesNotExist:
            return None

    @staticmethod
    def get_projects_by_status(status: str) -> List[Project]:
        """
        Lấy danh sách dự án theo trạng thái.

        Args:
            status: Trạng thái dự án

        Returns:
            Danh sách dự án
        """
        return list(Project.objects.filter(status=status).select_related('package_type'))

    @staticmethod
    def get_upcoming_projects(days: int = 7) -> List[Project]:
        """
        Lấy danh sách dự án sắp tới.

        Args:
            days: Số ngày tới

        Returns:
            Danh sách dự án
        """
        from datetime import datetime, timedelta
        end_date = datetime.now().date() + timedelta(days=days)
        return list(
            Project.objects.filter(
                shoot_date__lte=end_date,
                shoot_date__gte=datetime.now().date(),
                status='pending'
            ).select_related('package_type').order_by('shoot_date')
        )
