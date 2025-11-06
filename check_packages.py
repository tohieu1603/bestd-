import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.packages.models import Package
from django.db.models import Count

print(f'Total packages: {Package.objects.count()}\n')

print('Packages by category:')
for category_data in Package.objects.values('category').annotate(count=Count('id')).order_by('category'):
    print(f'  {category_data["category"]}: {category_data["count"]}')

print('\nAll packages:')
for pkg in Package.objects.all().order_by('category', 'price'):
    print(f'  {pkg.package_id} | {pkg.category:12} | {pkg.name:30} | {pkg.price:>12,.0f} VND')
