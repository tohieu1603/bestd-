"""
Business logic services cho Salary.
"""
from typing import Optional, List, Dict
from uuid import UUID
from datetime import date
from django.db.models import Sum, Q
from .models import Salary, MonthlySalary
from .schemas import SalaryCreate, SalaryUpdate, MonthlySalaryCreate, MonthlySalaryUpdate
from apps.employees.models import Employee


class SalaryService:
    """Service class cho xử lý logic lương."""

    @staticmethod
    def create_salary(data: SalaryCreate, created_by=None) -> Salary:
        """
        Tạo salary mới.

        Args:
            data: Dữ liệu salary
            created_by: User tạo

        Returns:
            Salary object
        """
        salary_data = data.model_dump()
        salary = Salary(**salary_data)

        if created_by:
            salary.created_by = created_by

        salary.save()
        return salary

    @staticmethod
    def update_salary(salary_id: UUID, data: SalaryUpdate) -> Optional[Salary]:
        """
        Cập nhật thông tin salary.

        Args:
            salary_id: ID salary
            data: Dữ liệu cập nhật

        Returns:
            Salary object hoặc None
        """
        try:
            salary = Salary.objects.get(id=salary_id)
        except Salary.DoesNotExist:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(salary, field, value)

        salary.save()
        return salary

    @staticmethod
    def get_salary(salary_id: UUID) -> Optional[Salary]:
        """
        Lấy thông tin salary theo ID.

        Args:
            salary_id: ID salary

        Returns:
            Salary object hoặc None
        """
        try:
            return Salary.objects.select_related('employee', 'project').get(id=salary_id)
        except Salary.DoesNotExist:
            return None

    @staticmethod
    def list_salaries(
        employee: Optional[UUID] = None,
        project: Optional[UUID] = None,
        month: Optional[str] = None,
        is_paid: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Salary], int]:
        """
        Lấy danh sách salary với filter.

        Args:
            employee: Filter theo nhân viên
            project: Filter theo dự án
            month: Filter theo tháng
            is_paid: Filter theo trạng thái thanh toán
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa

        Returns:
            Tuple (danh sách salary, tổng số)
        """
        queryset = Salary.objects.select_related('employee', 'project').all()

        if employee:
            queryset = queryset.filter(employee_id=employee)

        if project:
            queryset = queryset.filter(project_id=project)

        if month:
            queryset = queryset.filter(month=month)

        if is_paid is not None:
            queryset = queryset.filter(is_paid=is_paid)

        total = queryset.count()
        salaries = list(queryset[skip:skip + limit])

        return salaries, total

    @staticmethod
    def delete_salary(salary_id: UUID) -> bool:
        """
        Xóa salary.

        Args:
            salary_id: ID salary

        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        try:
            salary = Salary.objects.get(id=salary_id)
            salary.delete()
            return True
        except Salary.DoesNotExist:
            return False

    @staticmethod
    def create_monthly_salary(data: MonthlySalaryCreate, created_by=None) -> MonthlySalary:
        """
        Tạo monthly salary mới.

        Args:
            data: Dữ liệu monthly salary
            created_by: User tạo

        Returns:
            MonthlySalary object
        """
        salary_data = data.model_dump()
        employee_id = salary_data.pop('employee_id')

        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            raise ValueError(f"Employee with id {employee_id} does not exist")

        monthly_salary = MonthlySalary(
            employee=employee,
            **salary_data
        )

        # Only set created_by if it's a valid user instance
        if created_by and hasattr(created_by, 'id'):
            monthly_salary.created_by = created_by

        monthly_salary.save()
        return monthly_salary

    @staticmethod
    def update_monthly_salary(salary_id: UUID, data: MonthlySalaryUpdate) -> Optional[MonthlySalary]:
        """
        Cập nhật monthly salary.

        Args:
            salary_id: ID monthly salary
            data: Dữ liệu cập nhật

        Returns:
            MonthlySalary object hoặc None
        """
        try:
            monthly_salary = MonthlySalary.objects.get(id=salary_id)
        except MonthlySalary.DoesNotExist:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(monthly_salary, field, value)

        monthly_salary.save()
        return monthly_salary

    @staticmethod
    def get_monthly_salary(salary_id: UUID) -> Optional[MonthlySalary]:
        """
        Lấy monthly salary theo ID.

        Args:
            salary_id: ID monthly salary

        Returns:
            MonthlySalary object hoặc None
        """
        try:
            return MonthlySalary.objects.select_related('employee').get(id=salary_id)
        except MonthlySalary.DoesNotExist:
            return None

    @staticmethod
    def list_monthly_salaries(
        month: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[MonthlySalary], int]:
        """
        Lấy danh sách monthly salary.

        Args:
            month: Filter theo tháng
            status: Filter theo trạng thái
            skip: Số bản ghi bỏ qua
            limit: Số bản ghi tối đa

        Returns:
            Tuple (danh sách monthly salary, tổng số)
        """
        queryset = MonthlySalary.objects.select_related('employee').all()

        if month:
            queryset = queryset.filter(month=month)

        if status:
            queryset = queryset.filter(status=status)

        total = queryset.count()
        salaries = list(queryset[skip:skip + limit])

        return salaries, total

    @staticmethod
    def delete_monthly_salary(salary_id: UUID) -> bool:
        """
        Xóa monthly salary.

        Args:
            salary_id: ID monthly salary

        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        try:
            monthly_salary = MonthlySalary.objects.get(id=salary_id)
            monthly_salary.delete()
            return True
        except MonthlySalary.DoesNotExist:
            return False

    @staticmethod
    def calculate_monthly_salary(employee_id: UUID, month: str, created_by=None) -> MonthlySalary:
        """
        Tính lương tháng cho nhân viên.

        Args:
            employee_id: ID nhân viên
            month: Tháng (YYYY-MM)
            created_by: User tạo

        Returns:
            MonthlySalary object
        """
        employee = Employee.objects.get(id=employee_id)

        # Lấy tất cả salary của nhân viên trong tháng
        salaries = Salary.objects.filter(employee_id=employee_id, month=month)

        # Tính tổng
        project_salaries = []
        total_amount = 0
        total_bonus = 0

        for salary in salaries:
            project_salaries.append({
                'project': str(salary.project_id),
                'work_type': salary.work_type,
                'amount': float(salary.amount),
                'bonus': float(salary.bonus),
                'quantity': salary.quantity
            })
            total_amount += salary.amount
            total_bonus += salary.bonus

        # Tạo hoặc cập nhật MonthlySalary
        monthly_salary, created = MonthlySalary.objects.update_or_create(
            employee=employee,
            month=month,
            defaults={
                'base_salary': employee.base_salary,
                'bonus': total_bonus,
                'deduction': 0,
                'total_amount': employee.base_salary + total_amount + total_bonus,
                'projects_detail': project_salaries,
                'status': 'pending',
                'created_by': created_by
            }
        )

        return monthly_salary

    @staticmethod
    def generate_report(month: str) -> Dict:
        """
        Tạo báo cáo lương tháng.

        Args:
            month: Tháng (YYYY-MM)

        Returns:
            Dict chứa báo cáo
        """
        monthly_salaries = MonthlySalary.objects.filter(month=month).select_related('employee')

        total_employees = monthly_salaries.count()
        total_salary = monthly_salaries.aggregate(total=Sum('total_amount'))['total'] or 0
        total_paid = monthly_salaries.filter(status='paid').aggregate(total=Sum('total_amount'))['total'] or 0
        total_unpaid = total_salary - total_paid

        employee_salaries = []
        for ms in monthly_salaries:
            employee_salaries.append({
                'employee_id': str(ms.employee.id),
                'employee_name': ms.employee.name,
                'role': ms.employee.role,
                'total_salary': float(ms.total_amount),
                'status': ms.status,
                'base_salary': float(ms.base_salary),
                'bonus': float(ms.bonus),
                'deduction': float(ms.deduction),
                'projects_detail': ms.projects_detail
            })

        return {
            'month': month,
            'total_employees': total_employees,
            'total_salary': float(total_salary),
            'total_paid': float(total_paid),
            'total_unpaid': float(total_unpaid),
            'employee_salaries': employee_salaries
        }

    @staticmethod
    def get_employee_salary_history(employee_id: UUID) -> List[MonthlySalary]:
        """
        Lấy lịch sử lương của nhân viên.

        Args:
            employee_id: ID nhân viên

        Returns:
            Danh sách MonthlySalary
        """
        return list(
            MonthlySalary.objects.filter(employee_id=employee_id)
            .order_by('-month')
        )

    @staticmethod
    def mark_as_paid(monthly_salary_id: UUID, paid_date: date, payment_method: str) -> Optional[MonthlySalary]:
        """
        Đánh dấu lương đã thanh toán.

        Args:
            monthly_salary_id: ID monthly salary
            paid_date: Ngày thanh toán
            payment_method: Phương thức thanh toán

        Returns:
            MonthlySalary object hoặc None
        """
        try:
            monthly_salary = MonthlySalary.objects.get(id=monthly_salary_id)
            monthly_salary.status = 'paid'
            monthly_salary.payment_date = paid_date
            monthly_salary.payment_method = payment_method
            monthly_salary.save()
            return monthly_salary
        except MonthlySalary.DoesNotExist:
            return None
