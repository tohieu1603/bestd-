"""
Models cho quản lý gói chụp.
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Package(models.Model):
    """Model gói chụp."""

    CATEGORY_CHOICES = [
        ('portrait', 'Portrait'),
        ('family', 'Family'),
        ('couple', 'Couple'),
        ('wedding', 'Wedding'),
        ('event', 'Event'),
        ('commercial', 'Commercial'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    package_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name="Mã gói"
    )
    name = models.CharField(max_length=200, verbose_name="Tên gói")
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name="Danh mục"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="Giá"
    )

    # Chi tiết gói
    details = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Chi tiết gói",
        help_text="Format: {photo, makeup, assistant, retouch, time, location, retouch_photos, extra_services[]}"
    )

    includes = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Bao gồm",
        help_text="Danh sách dịch vụ bao gồm"
    )

    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    popularity_score = models.IntegerField(default=0, verbose_name="Điểm phổ biến")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")

    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_packages',
        verbose_name="Người tạo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        db_table = 'packages'
        verbose_name = 'Gói chụp'
        verbose_name_plural = 'Gói chụp'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'category']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.category})"

    def save(self, *args, **kwargs):
        """Override save để tự động tạo package_id."""
        if not self.package_id:
            # Tạo package_id tự động: PKG + 5 chữ số
            count = Package.objects.count()
            self.package_id = f"PKG{str(count + 1).zfill(5)}"
        super().save(*args, **kwargs)
