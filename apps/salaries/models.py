"""
Models cho quản lý lương.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.employees.models import Employee
from apps.projects.models import Project

User = get_user_model()


class Salary(models.Model):
    """Model lương nhân viên."""

    WORK_TYPE_CHOICES = [
        ('mainPhotographer', 'Main Photographer'),
        ('assistPhotographer', 'Assist Photographer'),
        ('makeupArtist', 'Makeup Artist'),
        ('retouchArtist', 'Retouch Artist'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Foreign keys
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='salaries',
        verbose_name="Nhân viên"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='salaries',
        verbose_name="Dự án"
    )

    # Salary details
    month = models.CharField(
        max_length=7,
        verbose_name="Tháng",
        help_text="Format: YYYY-MM"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="Số tiền"
    )
    bonus = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Thưởng"
    )
    work_type = models.CharField(
        max_length=50,
        choices=WORK_TYPE_CHOICES,
        verbose_name="Loại công việc"
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name="Số lượng",
        help_text="Số lượng (ảnh retouch, ngày làm việc, etc.)"
    )

    # Payment status
    is_paid = models.BooleanField(default=False, verbose_name="Đã thanh toán")
    paid_date = models.DateField(null=True, blank=True, verbose_name="Ngày thanh toán")

    notes = models.TextField(blank=True, verbose_name="Ghi chú")

    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_salaries',
        verbose_name="Người tạo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'salaries'
        verbose_name = 'Lương'
        verbose_name_plural = 'Lương'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee', 'month']),
            models.Index(fields=['project']),
            models.Index(fields=['month']),
            models.Index(fields=['is_paid']),
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.month} - {self.work_type}"

    @property
    def total_compensation(self):
        """Tổng thu nhập = lương + thưởng."""
        return self.amount + self.bonus


class MonthlySalary(models.Model):
    """Model tổng hợp lương tháng của nhân viên."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='monthly_salaries',
        verbose_name="Nhân viên"
    )
    month = models.CharField(
        max_length=7,
        verbose_name="Tháng",
        help_text="Format: YYYY-MM"
    )

    # Salary breakdown
    total_salary = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="Tổng lương"
    )
    breakdown = models.JSONField(
        default=dict,
        verbose_name="Chi tiết",
        help_text="Format: {base_salary, project_salaries[], total_bonus, deductions, net_salary}"
    )

    # Payment info
    is_paid = models.BooleanField(default=False, verbose_name="Đã thanh toán")
    paid_date = models.DateField(null=True, blank=True, verbose_name="Ngày thanh toán")
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Phương thức thanh toán"
    )

    notes = models.TextField(blank=True, verbose_name="Ghi chú")

    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_monthly_salaries',
        verbose_name="Người tạo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'monthly_salaries'
        verbose_name = 'Lương tháng'
        verbose_name_plural = 'Lương tháng'
        ordering = ['-month', 'employee']
        unique_together = [['employee', 'month']]
        indexes = [
            models.Index(fields=['month']),
            models.Index(fields=['employee', 'month']),
            models.Index(fields=['is_paid']),
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.month}"
