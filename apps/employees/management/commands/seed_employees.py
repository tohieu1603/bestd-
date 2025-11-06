"""
Management command to seed sample employees.
"""
from django.core.management.base import BaseCommand
from apps.employees.models import Employee


class Command(BaseCommand):
    help = 'Seed sample employees into database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed employees...'))

        employees_data = [
            {
                'name': 'Nguyễn Văn An',
                'role': 'Photo/Retouch',
                'skills': ['Portrait', 'Wedding', 'Lightroom', 'Photoshop'],
                'phone': '0901234567',
                'email': 'an.nguyen@studio.com',
                'address': '123 Nguyễn Huệ, Q1, TP.HCM',
                'base_salary': 15000000,
                'notes': 'Photographer chính với 5 năm kinh nghiệm',
                'bank_account': {
                    'bank_name': 'Vietcombank',
                    'account_number': '1234567890',
                    'account_holder': 'NGUYEN VAN AN'
                },
                'emergency_contact': {
                    'name': 'Nguyễn Thị Bình',
                    'phone': '0912345678',
                    'relationship': 'Vợ'
                },
                'default_rates': {
                    'main_photo': 2000000,
                    'assist_photo': 1000000,
                    'makeup': 0,
                    'retouch': 50000
                },
                'start_date': '2020-01-15',
                'is_active': True
            },
            {
                'name': 'Trần Thị Mai',
                'role': 'Makeup Artist',
                'skills': ['Bridal Makeup', 'Fashion Makeup', 'Special Effects'],
                'phone': '0902345678',
                'email': 'mai.tran@studio.com',
                'address': '456 Lê Lợi, Q1, TP.HCM',
                'base_salary': 12000000,
                'notes': 'Chuyên makeup cô dâu',
                'bank_account': {
                    'bank_name': 'Techcombank',
                    'account_number': '2345678901',
                    'account_holder': 'TRAN THI MAI'
                },
                'emergency_contact': {
                    'name': 'Trần Văn Cường',
                    'phone': '0923456789',
                    'relationship': 'Anh trai'
                },
                'default_rates': {
                    'main_photo': 0,
                    'assist_photo': 0,
                    'makeup': 1500000,
                    'retouch': 0
                },
                'start_date': '2020-03-01',
                'is_active': True
            },
            {
                'name': 'Lê Minh Tuấn',
                'role': 'Photo/Retouch',
                'skills': ['Portrait', 'Commercial', 'Studio Setup', 'Photoshop'],
                'phone': '0903456789',
                'email': 'tuan.le@studio.com',
                'address': '789 Trần Hưng Đạo, Q5, TP.HCM',
                'base_salary': 13000000,
                'notes': 'Photographer phụ và retouch artist',
                'bank_account': {
                    'bank_name': 'ACB',
                    'account_number': '3456789012',
                    'account_holder': 'LE MINH TUAN'
                },
                'emergency_contact': {
                    'name': 'Lê Thị Hoa',
                    'phone': '0934567890',
                    'relationship': 'Mẹ'
                },
                'default_rates': {
                    'main_photo': 1500000,
                    'assist_photo': 800000,
                    'makeup': 0,
                    'retouch': 40000
                },
                'start_date': '2021-06-15',
                'is_active': True
            },
            {
                'name': 'Phạm Thu Hà',
                'role': 'Content',
                'skills': ['Social Media', 'Copywriting', 'Content Strategy', 'SEO'],
                'phone': '0904567890',
                'email': 'ha.pham@studio.com',
                'address': '321 Võ Văn Tần, Q3, TP.HCM',
                'base_salary': 10000000,
                'notes': 'Quản lý nội dung và social media',
                'bank_account': {
                    'bank_name': 'VietinBank',
                    'account_number': '4567890123',
                    'account_holder': 'PHAM THU HA'
                },
                'emergency_contact': {
                    'name': 'Phạm Văn Nam',
                    'phone': '0945678901',
                    'relationship': 'Bố'
                },
                'default_rates': {
                    'main_photo': 0,
                    'assist_photo': 0,
                    'makeup': 0,
                    'retouch': 0
                },
                'start_date': '2021-09-01',
                'is_active': True
            },
            {
                'name': 'Võ Đức Thành',
                'role': 'Sales',
                'skills': ['Customer Service', 'Consultation', 'CRM', 'Negotiation'],
                'phone': '0905678901',
                'email': 'thanh.vo@studio.com',
                'address': '654 Hai Bà Trưng, Q1, TP.HCM',
                'base_salary': 8000000,
                'notes': 'Sales consultant',
                'bank_account': {
                    'bank_name': 'MB Bank',
                    'account_number': '5678901234',
                    'account_holder': 'VO DUC THANH'
                },
                'emergency_contact': {
                    'name': 'Võ Thị Lan',
                    'phone': '0956789012',
                    'relationship': 'Chị gái'
                },
                'default_rates': {
                    'main_photo': 0,
                    'assist_photo': 0,
                    'makeup': 0,
                    'retouch': 0
                },
                'start_date': '2022-01-10',
                'is_active': True
            },
            {
                'name': 'Đỗ Thị Lan Anh',
                'role': 'Makeup Artist',
                'skills': ['Bridal Makeup', 'Event Makeup', 'Hair Styling'],
                'phone': '0906789012',
                'email': 'lananh.do@studio.com',
                'address': '987 Cách Mạng Tháng 8, Q10, TP.HCM',
                'base_salary': 11000000,
                'notes': 'Makeup artist chuyên event',
                'bank_account': {
                    'bank_name': 'Sacombank',
                    'account_number': '6789012345',
                    'account_holder': 'DO THI LAN ANH'
                },
                'emergency_contact': {
                    'name': 'Đỗ Văn Bình',
                    'phone': '0967890123',
                    'relationship': 'Chồng'
                },
                'default_rates': {
                    'main_photo': 0,
                    'assist_photo': 0,
                    'makeup': 1200000,
                    'retouch': 0
                },
                'start_date': '2022-03-15',
                'is_active': True
            },
            {
                'name': 'Hoàng Minh Khôi',
                'role': 'Photo/Retouch',
                'skills': ['Event Photography', 'Video', 'Editing', 'Drone'],
                'phone': '0907890123',
                'email': 'khoi.hoang@studio.com',
                'address': '159 Nguyễn Đình Chiểu, Q3, TP.HCM',
                'base_salary': 12000000,
                'notes': 'Photographer kiêm videographer',
                'bank_account': {
                    'bank_name': 'HDBank',
                    'account_number': '7890123456',
                    'account_holder': 'HOANG MINH KHOI'
                },
                'emergency_contact': {
                    'name': 'Hoàng Thị Mai',
                    'phone': '0978901234',
                    'relationship': 'Mẹ'
                },
                'default_rates': {
                    'main_photo': 1800000,
                    'assist_photo': 900000,
                    'makeup': 0,
                    'retouch': 45000
                },
                'start_date': '2022-07-01',
                'is_active': True
            },
            {
                'name': 'Ngô Thị Hương',
                'role': 'Manager',
                'skills': ['Project Management', 'Team Leadership', 'Budget Planning', 'Client Relations'],
                'phone': '0908901234',
                'email': 'huong.ngo@studio.com',
                'address': '753 Lý Thái Tổ, Q10, TP.HCM',
                'base_salary': 20000000,
                'notes': 'Studio Manager',
                'bank_account': {
                    'bank_name': 'BIDV',
                    'account_number': '8901234567',
                    'account_holder': 'NGO THI HUONG'
                },
                'emergency_contact': {
                    'name': 'Ngô Văn Tùng',
                    'phone': '0989012345',
                    'relationship': 'Chồng'
                },
                'default_rates': {
                    'main_photo': 0,
                    'assist_photo': 0,
                    'makeup': 0,
                    'retouch': 0
                },
                'start_date': '2019-05-01',
                'is_active': True
            },
        ]

        created_count = 0
        updated_count = 0

        for emp_data in employees_data:
            # Check if employee already exists by email
            existing_emp = Employee.objects.filter(email=emp_data['email']).first()

            if existing_emp:
                # Update existing employee
                for key, value in emp_data.items():
                    setattr(existing_emp, key, value)
                existing_emp.save()
                updated_count += 1
                self.stdout.write(f'  Updated: {emp_data["name"]}')
            else:
                # Create new employee
                Employee.objects.create(**emp_data)
                created_count += 1
                self.stdout.write(f'  Created: {emp_data["name"]}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully seeded employees!\n'
                f'Created: {created_count}\n'
                f'Updated: {updated_count}\n'
                f'Total: {created_count + updated_count}'
            )
        )
