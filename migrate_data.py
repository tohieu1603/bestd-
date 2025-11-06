"""
Script để migrate data từ MongoDB (hệ thống cũ) sang Django (hệ thống mới)
"""
import os
import sys
import django
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.packages.models import Package
from apps.employees.models import Employee
from apps.partners.models import Partner

# MongoDB connection (nếu cần)
try:
    from pymongo import MongoClient
    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False
    print("PyMongo not installed. Will use manual data input.")

def migrate_from_mongodb(mongo_uri='mongodb://localhost:27017/studio_management'):
    """Migrate data from MongoDB to Django"""
    if not MONGO_AVAILABLE:
        print("Please install pymongo: pip install pymongo")
        return

    try:
        client = MongoClient(mongo_uri)
        db = client.get_database()

        # Migrate Packages
        print("\n=== Migrating Packages ===")
        packages_collection = db.packages
        packages = list(packages_collection.find())

        for pkg in packages:
            try:
                # Map MongoDB data to Django model
                package_data = {
                    'name': pkg.get('name'),
                    'category': pkg.get('category', 'wedding'),
                    'price': pkg.get('price', 0),
                    'details': {
                        'photo': pkg.get('details', {}).get('photo', 0),
                        'makeup': pkg.get('details', {}).get('makeup', 0),
                        'assistant': pkg.get('details', {}).get('assistant', 0),
                        'retouch': pkg.get('details', {}).get('retouch', 0),
                        'time': pkg.get('details', {}).get('time', ''),
                        'location': pkg.get('details', {}).get('location', ''),
                        'retouchPhotos': pkg.get('details', {}).get('retouchPhotos', 0),
                        'extraServices': pkg.get('details', {}).get('extraServices', [])
                    },
                    'includes': pkg.get('includes', []),
                    'description': pkg.get('description', ''),
                    'notes': pkg.get('notes', ''),
                    'is_active': pkg.get('isActive', True),
                    'popularity_score': pkg.get('popularityScore', 0)
                }

                # Create package
                Package.objects.create(**package_data)
                print(f"✓ Migrated package: {package_data['name']}")
            except Exception as e:
                print(f"✗ Error migrating package {pkg.get('name')}: {e}")

        # Migrate Employees
        print("\n=== Migrating Employees ===")
        employees_collection = db.employees
        employees = list(employees_collection.find())

        for emp in employees:
            try:
                employee_data = {
                    'name': emp.get('name'),
                    'role': emp.get('role', 'Photo/Retouch'),
                    'skills': emp.get('skills', []),
                    'phone': emp.get('phone', ''),
                    'email': emp.get('email', ''),
                    'address': emp.get('address', ''),
                    'base_salary': emp.get('baseSalary', 0),
                    'bank_account': {
                        'bank_name': emp.get('bankAccount', {}).get('bankName', ''),
                        'account_number': emp.get('bankAccount', {}).get('accountNumber', ''),
                        'account_holder': emp.get('bankAccount', {}).get('accountHolder', '')
                    },
                    'emergency_contact': {
                        'name': emp.get('emergencyContact', {}).get('name', ''),
                        'phone': emp.get('emergencyContact', {}).get('phone', ''),
                        'relationship': emp.get('emergencyContact', {}).get('relationship', '')
                    },
                    'default_rates': {
                        'main_photo': emp.get('defaultRates', {}).get('mainPhoto', 500000),
                        'assist_photo': emp.get('defaultRates', {}).get('assistPhoto', 300000),
                        'retouch': emp.get('defaultRates', {}).get('retouch', 50000),
                        'makeup': emp.get('defaultRates', {}).get('makeup', 400000)
                    },
                    'notes': emp.get('notes', ''),
                    'is_active': emp.get('isActive', True)
                }

                Employee.objects.create(**employee_data)
                print(f"✓ Migrated employee: {employee_data['name']}")
            except Exception as e:
                print(f"✗ Error migrating employee {emp.get('name')}: {e}")

        print("\n=== Migration Complete ===")
        print(f"Total Packages: {Package.objects.count()}")
        print(f"Total Employees: {Employee.objects.count()}")

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Please check your MongoDB connection string and ensure MongoDB is running.")

def create_sample_data():
    """Create sample data nếu không có MongoDB"""
    print("\n=== Creating Sample Data ===")

    # Sample Packages
    sample_packages = [
        {
            'name': 'Gói Wedding Premium',
            'category': 'wedding',
            'price': 15000000,
            'details': {
                'photo': 1,
                'makeup': 1,
                'assistant': 1,
                'retouch': 100,
                'time': '5-6 giờ',
                'location': 'Studio + 1 ngoại cảnh',
                'retouchPhotos': 100,
                'extraServices': ['Album 30x40', 'Video highlights']
            },
            'includes': ['100 ảnh retouch', 'Album 30x40', 'Video highlights', 'Makeup & Làm tóc'],
            'description': 'Gói chụp ảnh cưới cao cấp với đầy đủ dịch vụ',
            'is_active': True,
            'popularity_score': 10
        },
        {
            'name': 'Gói Wedding Standard',
            'category': 'wedding',
            'price': 10000000,
            'details': {
                'photo': 1,
                'makeup': 1,
                'assistant': 0,
                'retouch': 50,
                'time': '4 giờ',
                'location': 'Studio',
                'retouchPhotos': 50,
                'extraServices': ['Album 20x30']
            },
            'includes': ['50 ảnh retouch', 'Album 20x30', 'Makeup & Làm tóc'],
            'description': 'Gói chụp ảnh cưới tiết kiệm',
            'is_active': True,
            'popularity_score': 8
        },
        {
            'name': 'Gói Family Portrait',
            'category': 'family',
            'price': 3000000,
            'details': {
                'photo': 1,
                'makeup': 0,
                'assistant': 0,
                'retouch': 20,
                'time': '2 giờ',
                'location': 'Studio',
                'retouchPhotos': 20,
                'extraServices': []
            },
            'includes': ['20 ảnh retouch', 'File digital'],
            'description': 'Gói chụp ảnh gia đình',
            'is_active': True,
            'popularity_score': 7
        },
        {
            'name': 'Gói Couple Premium',
            'category': 'couple',
            'price': 5000000,
            'details': {
                'photo': 1,
                'makeup': 1,
                'assistant': 0,
                'retouch': 40,
                'time': '3 giờ',
                'location': 'Studio + 1 ngoại cảnh',
                'retouchPhotos': 40,
                'extraServices': ['Album 20x30']
            },
            'includes': ['40 ảnh retouch', 'Album 20x30', 'Makeup'],
            'description': 'Gói chụp ảnh cặp đôi cao cấp',
            'is_active': True,
            'popularity_score': 9
        }
    ]

    for pkg_data in sample_packages:
        try:
            Package.objects.create(**pkg_data)
            print(f"✓ Created package: {pkg_data['name']}")
        except Exception as e:
            print(f"✗ Error creating package: {e}")

    # Sample Employees
    sample_employees = [
        {
            'name': 'Nguyễn Văn A',
            'role': 'Photo/Retouch',
            'skills': ['Chụp chính', 'Retouch'],
            'phone': '0901234567',
            'email': 'nguyenvana@example.com',
            'base_salary': 8000000,
            'bank_account': {
                'bank_name': 'Vietcombank',
                'account_number': '1234567890',
                'account_holder': 'NGUYEN VAN A'
            },
            'emergency_contact': {
                'name': 'Nguyễn Thị B',
                'phone': '0909876543',
                'relationship': 'Vợ'
            },
            'default_rates': {
                'main_photo': 800000,
                'assist_photo': 400000,
                'retouch': 60000,
                'makeup': 0
            },
            'is_active': True
        },
        {
            'name': 'Trần Thị C',
            'role': 'Makeup Artist',
            'skills': ['Makeup', 'Làm tóc'],
            'phone': '0902345678',
            'email': 'tranthic@example.com',
            'base_salary': 6000000,
            'bank_account': {
                'bank_name': 'Techcombank',
                'account_number': '0987654321',
                'account_holder': 'TRAN THI C'
            },
            'emergency_contact': {
                'name': 'Trần Văn D',
                'phone': '0908765432',
                'relationship': 'Chồng'
            },
            'default_rates': {
                'main_photo': 0,
                'assist_photo': 0,
                'retouch': 0,
                'makeup': 600000
            },
            'is_active': True
        },
        {
            'name': 'Lê Văn E',
            'role': 'Photo/Retouch',
            'skills': ['Chụp phụ', 'Retouch'],
            'phone': '0903456789',
            'email': 'levane@example.com',
            'base_salary': 5000000,
            'bank_account': {
                'bank_name': 'ACB',
                'account_number': '1122334455',
                'account_holder': 'LE VAN E'
            },
            'emergency_contact': {
                'name': 'Lê Thị F',
                'phone': '0907654321',
                'relationship': 'Mẹ'
            },
            'default_rates': {
                'main_photo': 500000,
                'assist_photo': 350000,
                'retouch': 50000,
                'makeup': 0
            },
            'is_active': True
        },
        {
            'name': 'Phạm Thị G',
            'role': 'Sales',
            'skills': ['Sales', 'Tư vấn khách hàng'],
            'phone': '0904567890',
            'email': 'phamthig@example.com',
            'base_salary': 7000000,
            'bank_account': {
                'bank_name': 'VPBank',
                'account_number': '5566778899',
                'account_holder': 'PHAM THI G'
            },
            'emergency_contact': {
                'name': 'Phạm Văn H',
                'phone': '0906543210',
                'relationship': 'Anh'
            },
            'default_rates': {
                'main_photo': 0,
                'assist_photo': 0,
                'retouch': 0,
                'makeup': 0
            },
            'is_active': True
        }
    ]

    for emp_data in sample_employees:
        try:
            Employee.objects.create(**emp_data)
            print(f"✓ Created employee: {emp_data['name']}")
        except Exception as e:
            print(f"✗ Error creating employee: {e}")

    print("\n=== Sample Data Created ===")
    print(f"Total Packages: {Package.objects.count()}")
    print(f"Total Employees: {Employee.objects.count()}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Migrate data to Django database')
    parser.add_argument('--mode', choices=['mongodb', 'sample'], default='sample',
                      help='Migration mode: mongodb (from old system) or sample (create sample data)')
    parser.add_argument('--mongo-uri', default='mongodb://localhost:27017/studio_management',
                      help='MongoDB connection URI')

    args = parser.parse_args()

    if args.mode == 'mongodb':
        migrate_from_mongodb(args.mongo_uri)
    else:
        create_sample_data()
