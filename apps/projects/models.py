"""
Models cho quản lý dự án.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.packages.models import Package
from apps.employees.models import Employee
from apps.partners.models import Partner

User = get_user_model()


class Project(models.Model):
    """Model dự án."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('deposit', 'Deposit'),
        ('paid', 'Paid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name="Mã dự án"
    )

    # Thông tin khách hàng
    customer_name = models.CharField(max_length=200, verbose_name="Tên khách hàng")
    customer_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    customer_email = models.EmailField(max_length=255, blank=True, verbose_name="Email")

    # Thông tin gói chụp
    package_type = models.ForeignKey(
        Package,
        on_delete=models.PROTECT,
        related_name='projects',
        verbose_name="Loại gói"
    )
    package_name = models.CharField(max_length=200, verbose_name="Tên gói")
    package_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="Giá gói"
    )
    package_discount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0,
        verbose_name="Giảm giá"
    )
    package_final_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="Giá cuối cùng"
    )

    # Gói bổ sung
    additional_packages = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Gói bổ sung",
        help_text="Format: [{package_type, package_name, package_price, package_discount, package_final_price, team, notes}]"
    )

    # Thông tin thanh toán
    payment = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Thanh toán",
        help_text="Format: {status, deposit, final, paid, payment_history[{amount, date, method, notes, received_by}]}"
    )

    # Thông tin chụp
    shoot_date = models.DateField(verbose_name="Ngày chụp")
    shoot_time = models.CharField(max_length=50, blank=True, verbose_name="Giờ chụp")
    location = models.CharField(max_length=500, blank=True, verbose_name="Địa điểm")

    # Trạng thái
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Trạng thái"
    )
    progress = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Tiến độ",
        help_text="Format: {shooting_done, retouch_done, delivered}"
    )

    # Milestones
    milestones = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Cột mốc",
        help_text="Format: [{name, description, stage, status, team, start_date, due_date, completed_date, completed_by, notes}]"
    )

    # Team
    team = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Đội ngũ",
        help_text="Format: {main_photographer:{employee, salary, bonus, notes}, assist_photographers[], makeup_artists[], retouch_artists[]}"
    )

    # Partners
    partners = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Đối tác",
        help_text="Format: {clothing[{partner, actual_cost}], printing:{included, actual_cost}, flower:{included, actual_cost}, total_cost, notes[]}"
    )

    # Ngày hoàn thành và giao hàng
    completed_date = models.DateField(null=True, blank=True, verbose_name="Ngày hoàn thành")
    delivery_date = models.DateField(null=True, blank=True, verbose_name="Ngày giao hàng")

    # Files
    files = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Files",
        help_text="Format: [{type, url, uploaded_at}]"
    )

    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    # Update history
    update_history = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Lịch sử cập nhật",
        help_text="Format: [{date, user, action, notes, changes}]"
    )

    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_projects',
        verbose_name="Người tạo"
    )
    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='modified_projects',
        verbose_name="Người sửa cuối"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'projects'
        verbose_name = 'Dự án'
        verbose_name_plural = 'Dự án'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-shoot_date']),
            models.Index(fields=['customer_name', 'customer_phone']),
            models.Index(fields=['created_by', '-created_at']),
        ]

    def __str__(self):
        return f"{self.project_code} - {self.customer_name}"

    def save(self, *args, **kwargs):
        """Override save để tự động tạo project_code và tính giá."""
        if not self.project_code:
            # Tạo project_code: PRJ + YYMM + 4 chữ số
            from datetime import datetime
            count = Project.objects.count()
            now = datetime.now()
            year = str(now.year)[2:]
            month = str(now.month).zfill(2)
            self.project_code = f"PRJ{year}{month}{str(count + 1).zfill(4)}"

        # Tính giá cuối cùng
        if self.package_price is not None and self.package_discount is not None:
            self.package_final_price = self.package_price - self.package_discount
        else:
            self.package_final_price = self.package_price

        # Set default progress
        if not self.progress:
            self.progress = {
                'shooting_done': False,
                'retouch_done': False,
                'delivered': False
            }

        # Set default payment
        if not self.payment:
            self.payment = {
                'status': 'unpaid',
                'deposit': 0,
                'final': 0,
                'paid': 0,
                'payment_history': []
            }

        super().save(*args, **kwargs)
