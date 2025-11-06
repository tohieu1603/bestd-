"""
Models cho quản lý nhân viên.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Employee(models.Model):
    """Model nhân viên."""

    ROLE_CHOICES = [
        ('Photo/Retouch', 'Photo/Retouch'),
        ('Makeup Artist', 'Makeup Artist'),
        ('Sales', 'Sales'),
        ('Manager', 'Manager'),
        ('Content', 'Content'),
        ('Designer', 'Designer'),
    ]

    SKILL_CHOICES = [
        ('Chụp chính', 'Chụp chính'),
        ('Chụp phụ', 'Chụp phụ'),
        ('Retouch', 'Retouch'),
        ('Makeup', 'Makeup'),
        ('Làm tóc', 'Làm tóc'),
        ('Styling', 'Styling'),
        ('Sales', 'Sales'),
        ('Tư vấn khách hàng', 'Tư vấn khách hàng'),
        ('Quản lý dự án', 'Quản lý dự án'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Tên nhân viên")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="Vai trò")
    skills = models.JSONField(default=list, blank=True, verbose_name="Kỹ năng")

    # Thông tin liên hệ
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    email = models.EmailField(max_length=255, blank=True, verbose_name="Email")
    address = models.CharField(max_length=500, blank=True, verbose_name="Địa chỉ")

    # Thông tin ngân hàng
    bank_account = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Thông tin ngân hàng",
        help_text="Format: {bank_name, account_number, account_holder}"
    )

    # Liên hệ khẩn cấp
    emergency_contact = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Liên hệ khẩn cấp",
        help_text="Format: {name, phone, relationship}"
    )

    # Thông tin công việc
    start_date = models.DateField(auto_now_add=True, verbose_name="Ngày bắt đầu")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    base_salary = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Lương cơ bản"
    )

    # Đơn giá mặc định cho các công việc
    default_rates = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Đơn giá mặc định",
        help_text="Format: {main_photo, assist_photo, retouch, makeup}"
    )

    notes = models.TextField(blank=True, verbose_name="Ghi chú")

    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_employees',
        verbose_name="Người tạo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'employees'
        verbose_name = 'Nhân viên'
        verbose_name_plural = 'Nhân viên'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'role']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.role})"

    def set_default_rates(self):
        """Set default rates based on role."""
        if not self.default_rates:
            self.default_rates = {
                'main_photo': 500000,
                'assist_photo': 300000,
                'retouch': 50000,
                'makeup': 400000
            }
