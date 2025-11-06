#!/usr/bin/env python
"""
Master seed script - seeds all data in correct order.
Run this script to populate the database with sample data.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.core.management import call_command


def main():
    print("=" * 60)
    print("STUDIO MANAGEMENT SYSTEM - DATABASE SEEDING")
    print("=" * 60)
    print()

    commands = [
        ('seed_packages', 'Seeding packages...'),
        ('seed_employees', 'Seeding employees...'),
    ]

    for command, message in commands:
        print()
        print("-" * 60)
        print(message)
        print("-" * 60)
        try:
            call_command(command)
        except Exception as e:
            print(f"ERROR running {command}: {e}")
            sys.exit(1)

    print()
    print("=" * 60)
    print("✓ ALL DATA SEEDED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("You can now:")
    print("  1. Start the backend: python manage.py runserver")
    print("  2. Start the frontend: cd ../frontend && npm run dev")
    print("  3. Login with: admin / admin123")
    print()


if __name__ == '__main__':
    main()
