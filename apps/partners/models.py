"""
Models cho quản lý đối tác.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Partner(models.Model):
    """Model đối tác."""

    TYPE_CHOICES = [
        ('clothing', 'Clothing'),
        ('printing', 'Printing'),
        ('flower', 'Flower'),
        ('venue', 'Venue'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name="Mã đối tác"
    )
    name = models.CharField(max_length=200, verbose_name="Tên đối tác")
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        verbose_name="Loại đối tác"
    )

    # Cost có thể là số hoặc chuỗi "Theo bill"
    cost = models.CharField(
        max_length=100,
        verbose_name="Chi phí",
        help_text="Có thể là số hoặc 'Theo bill'"
    )

    # Thông tin liên hệ
    contact_info = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Thông tin liên hệ",
        help_text="Format: {phone, email, address, website, contact_person}"
    )

    # Thông tin ngân hàng
    bank_account = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Thông tin ngân hàng",
        help_text="Format: {bank_name, account_number, account_holder}"
    )

    # Thông tin doanh nghiệp
    business_info = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Thông tin doanh nghiệp",
        help_text="Format: {tax_code, business_license, established_date}"
    )

    # Đánh giá và thống kê
    rating = models.FloatField(
        default=0,
        verbose_name="Đánh giá",
        help_text="Từ 0 đến 5"
    )
    projects_count = models.IntegerField(default=0, verbose_name="Số dự án")
    total_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="Tổng doanh thu"
    )

    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")

    # Hợp đồng
    agreements = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Hợp đồng",
        help_text="Format: [{title, file_url, start_date, end_date, terms}]"
    )

    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_partners',
        verbose_name="Người tạo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'partners'
        verbose_name = 'Đối tác'
        verbose_name_plural = 'Đối tác'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['type', 'is_active']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.type})"

    def save(self, *args, **kwargs):
        """Override save để tự động tạo partner_id."""
        if not self.partner_id:
            # Tạo partner_id tự động: PTN + 5 chữ số
            count = Partner.objects.count()
            self.partner_id = f"PTN{str(count + 1).zfill(5)}"
        super().save(*args, **kwargs)
