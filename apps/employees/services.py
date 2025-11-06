"""
Business logic services cho Employee.
"""
from typing import Optional, List, Dict
from uuid import UUID
from django.db.models import Q
from .models import Employee
from .schemas import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    """Service class cho xử lý logic nhân viên."""

    @staticmethod
    def create_employee(data: EmployeeCreate, created_by=None) -> Employee:
        """
        Tạo nhân viên mới.

        Args:
            data: Dữ liệu nhân viên
            created_by: User tạo

        Returns:
            Employee object
        """
        employee_data = data.model_dump(exclude={'bank_account', 'emergency_contact', 'default_rates'})

        # Xử lý nested data
        employee = Employee(**employee_data)

        if data.bank_account:
            employee.bank_account = data.bank_account.model_dump()

        if data.emergency_contact:
            employee.emergency_contact = data.emergency_contact.model_dump()

        if data.default_rates:
            employee.default_rates = data.default_rates.model_dump()
        else:
            employee.set_default_rates()

        if created_by:
            employee.created_by = created_by

        employee.save()
        return employee

    @staticmethod
    def update_employee(employee_id: UUID, data: EmployeeUpdate) -> Optional[Employee]:
        """
        Cập nhật thông tin nhân viên.

        Args:
            employee_id: ID nhân viên
            data: Dữ liệu cập nhật

        Returns:
            Employee object hoặc None
        """
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude={'bank_account', 'emergency_contact', 'default_rates'})

        for field, value in update_data.items():
            setattr(employee, field, value)

        # Update nested fields
        if data.bank_account is not None:
            employee.bank_account = data.bank_account.model_dump()

        if data.emergency_contact is not None:
            employee.emergency_contact = data.emergency_contact.model_dump()

        if data.default_rates is not None:
            employee.default_rates = data.default_rates.model_dump()

        employee.save()
        return employee

    @staticmethod
    def get_employee(employee_id: UUID) -> Optional[Employee]:
        """
        Lấy thông tin nhân viên theo ID.

        Args:
            employee_id: ID nhân viên

        Returns:
            Employee object hoặc None
        """
        try:
            return Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return None

    @staticmethod
    def list_employees(
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Employee], int]:
        """
        Lấy danh sách nhân viên với filter.

        Args:
            role: Filter theo vai trò
            is_active: Filter theo trạng thái
            search: Tìm kiếm theo tên
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa

        Returns:
            Tuple (danh sách nhân viên, tổng số)
        """
        queryset = Employee.objects.all()

        # Apply filters
        if role:
            queryset = queryset.filter(role=role)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search)
            )

        total = queryset.count()
        employees = list(queryset[skip:skip + limit])

        return employees, total

    @staticmethod
    def delete_employee(employee_id: UUID) -> bool:
        """
        Xóa nhân viên (soft delete - set is_active = False).

        Args:
            employee_id: ID nhân viên

        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        try:
            employee = Employee.objects.get(id=employee_id)
            employee.is_active = False
            employee.save()
            return True
        except Employee.DoesNotExist:
            return False

    @staticmethod
    def get_employees_by_role(role: str) -> List[Employee]:
        """
        Lấy danh sách nhân viên theo vai trò.

        Args:
            role: Vai trò

        Returns:
            Danh sách nhân viên
        """
        return list(Employee.objects.filter(role=role, is_active=True))

    @staticmethod
    def get_active_employees() -> List[Employee]:
        """
        Lấy tất cả nhân viên đang hoạt động.

        Returns:
            Danh sách nhân viên active
        """
        return list(Employee.objects.filter(is_active=True))

    @staticmethod
    def search_employees(query: str) -> List[Employee]:
        """
        Tìm kiếm nhân viên theo tên, email hoặc số điện thoại.

        Args:
            query: Từ khóa tìm kiếm

        Returns:
            Danh sách nhân viên
        """
        return list(
            Employee.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            )
        )
