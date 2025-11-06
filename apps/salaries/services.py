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

        # Breakdown
        breakdown = {
            'base_salary': float(employee.base_salary),
            'project_salaries': project_salaries,
            'total_project_amount': float(total_amount),
            'total_bonus': float(total_bonus),
            'deductions': 0,
            'net_salary': float(employee.base_salary + total_amount + total_bonus)
        }

        # Tạo hoặc cập nhật MonthlySalary
        monthly_salary, created = MonthlySalary.objects.update_or_create(
            employee=employee,
            month=month,
            defaults={
                'total_salary': breakdown['net_salary'],
                'breakdown': breakdown,
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
        total_salary = monthly_salaries.aggregate(total=Sum('total_salary'))['total'] or 0
        total_paid = monthly_salaries.filter(is_paid=True).aggregate(total=Sum('total_salary'))['total'] or 0
        total_unpaid = total_salary - total_paid

        employee_salaries = []
        for ms in monthly_salaries:
            employee_salaries.append({
                'employee_id': str(ms.employee.id),
                'employee_name': ms.employee.name,
                'role': ms.employee.role,
                'total_salary': float(ms.total_salary),
                'is_paid': ms.is_paid,
                'breakdown': ms.breakdown
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
            monthly_salary.is_paid = True
            monthly_salary.paid_date = paid_date
            monthly_salary.payment_method = payment_method
            monthly_salary.save()
            return monthly_salary
        except MonthlySalary.DoesNotExist:
            return None
