"""
Management command to create admin user.
"""
from django.core.management.base import BaseCommand
from apps.users.models import User
import uuid


class Command(BaseCommand):
    help = 'Create admin user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create(
                id=uuid.uuid4(),
                username='admin',
                email='admin@studio.com',
                full_name='System Administrator',
                role='admin',
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {admin.username}'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
