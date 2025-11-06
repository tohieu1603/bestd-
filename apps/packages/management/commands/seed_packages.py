"""
Management command to seed photography packages.
"""
from django.core.management.base import BaseCommand
from apps.packages.models import Package


class Command(BaseCommand):
    help = 'Seed photography packages into database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed packages...'))

        packages_data = [
            # PORTRAIT PACKAGES
            {
                'name': 'Gói Portrait Basic',
                'category': 'portrait',
                'price': 1500000,
                'description': 'Gói chụp portrait cơ bản cho cá nhân',
                'details': {
                    'photo': 1,
                    'makeup': 1,
                    'assistant': 0,
                    'retouch': 20,
                    'time': '2 giờ',
                    'location': 'Studio',
                    'retouch_photos': 20,
                    'extra_services': ['Tư vấn concept', 'Cho thuê trang phục studio']
                },
                'includes': [
                    '1 Photographer',
                    '1 Makeup Artist',
                    '2 giờ chụp tại studio',
                    '20 ảnh retouch cơ bản',
                    'Tư vấn concept miễn phí',
                    'Cho thuê trang phục studio'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Portrait Standard',
                'category': 'portrait',
                'price': 2500000,
                'description': 'Gói chụp portrait tiêu chuẩn với nhiều concept',
                'details': {
                    'photo': 1,
                    'makeup': 1,
                    'assistant': 1,
                    'retouch': 40,
                    'time': '3-4 giờ',
                    'location': 'Studio hoặc outdoor',
                    'retouch_photos': 40,
                    'extra_services': ['Tư vấn concept', 'Cho thuê trang phục', 'Trợ lý chụp']
                },
                'includes': [
                    '1 Photographer chính',
                    '1 Trợ lý chụp',
                    '1 Makeup Artist',
                    '3-4 giờ chụp',
                    '40 ảnh retouch chuyên nghiệp',
                    'Đa dạng concept và phong cách',
                    'Cho thuê trang phục cao cấp',
                    'Chụp tại studio hoặc outdoor'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Portrait Premium',
                'category': 'portrait',
                'price': 4000000,
                'description': 'Gói chụp portrait cao cấp với dịch vụ toàn diện',
                'details': {
                    'photo': 2,
                    'makeup': 1,
                    'assistant': 1,
                    'retouch': 60,
                    'time': '4-5 giờ',
                    'location': 'Studio + outdoor',
                    'retouch_photos': 60,
                    'extra_services': ['Full makeup', 'Nhiều concept', 'Album cao cấp']
                },
                'includes': [
                    '1 Photographer chính + 1 Photographer phụ',
                    '1 Trợ lý chụp',
                    '1 Makeup Artist chuyên nghiệp',
                    '4-5 giờ chụp',
                    '60 ảnh retouch cao cấp',
                    'Nhiều concept và phong cách độc đáo',
                    'Makeup chuyên nghiệp với nhiều look',
                    'Album photobook cao cấp',
                    'Chụp cả studio và outdoor'
                ],
                'is_active': True,
                'popularity_score': 0
            },

            # FAMILY PACKAGES
            {
                'name': 'Gói Family Basic',
                'category': 'family',
                'price': 2000000,
                'description': 'Gói chụp gia đình cơ bản, ấm áp và tự nhiên',
                'details': {
                    'photo': 1,
                    'makeup': 1,
                    'assistant': 0,
                    'retouch': 30,
                    'time': '2 giờ',
                    'location': 'Studio',
                    'retouch_photos': 30,
                    'extra_services': ['Tư vấn concept gia đình']
                },
                'includes': [
                    '1 Photographer',
                    '1 Makeup Artist (cho người lớn)',
                    '2 giờ chụp tại studio',
                    '30 ảnh retouch',
                    'Tư vấn concept phù hợp với gia đình',
                    'Cho thuê trang phục cho cả gia đình'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Family Standard',
                'category': 'family',
                'price': 3500000,
                'description': 'Gói chụp gia đình tiêu chuẩn với nhiều concept',
                'details': {
                    'photo': 1,
                    'makeup': 1,
                    'assistant': 1,
                    'retouch': 50,
                    'time': '3-4 giờ',
                    'location': 'Studio hoặc outdoor',
                    'retouch_photos': 50,
                    'extra_services': ['Trợ lý chụp', 'Nhiều concept']
                },
                'includes': [
                    '1 Photographer chính',
                    '1 Trợ lý chụp',
                    '1 Makeup Artist',
                    '3-4 giờ chụp',
                    '50 ảnh retouch chuyên nghiệp',
                    'Nhiều concept gia đình',
                    'Chụp tại studio hoặc outdoor',
                    'Trang phục cho cả gia đình'
                ],
                'is_active': True,
                'popularity_score': 0
            },

            # COUPLE PACKAGES
            {
                'name': 'Gói Couple Basic',
                'category': 'couple',
                'price': 1800000,
                'description': 'Gói chụp couple lãng mạn cơ bản',
                'details': {
                    'photo': 1,
                    'makeup': 1,
                    'assistant': 0,
                    'retouch': 30,
                    'time': '2 giờ',
                    'location': 'Studio',
                    'retouch_photos': 30,
                    'extra_services': ['Tư vấn concept couple']
                },
                'includes': [
                    '1 Photographer',
                    '1 Makeup Artist',
                    '2 giờ chụp tại studio',
                    '30 ảnh retouch',
                    'Tư vấn concept lãng mạn',
                    'Cho thuê trang phục couple'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Couple Standard',
                'category': 'couple',
                'price': 3000000,
                'description': 'Gói chụp couple với concept đa dạng',
                'details': {
                    'photo': 1,
                    'makeup': 1,
                    'assistant': 1,
                    'retouch': 50,
                    'time': '3-4 giờ',
                    'location': 'Studio + outdoor',
                    'retouch_photos': 50,
                    'extra_services': ['Trợ lý chụp', 'Nhiều concept']
                },
                'includes': [
                    '1 Photographer chính',
                    '1 Trợ lý chụp',
                    '1 Makeup Artist',
                    '3-4 giờ chụp',
                    '50 ảnh retouch chuyên nghiệp',
                    'Nhiều concept lãng mạn',
                    'Chụp cả studio và outdoor',
                    'Trang phục couple cao cấp'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Couple Premium',
                'category': 'couple',
                'price': 5000000,
                'description': 'Gói chụp couple cao cấp với album photobook',
                'details': {
                    'photo': 2,
                    'makeup': 1,
                    'assistant': 1,
                    'retouch': 80,
                    'time': '5-6 giờ',
                    'location': 'Studio + outdoor + địa điểm đặc biệt',
                    'retouch_photos': 80,
                    'extra_services': ['Album cao cấp', 'Video ngắn', 'Drone']
                },
                'includes': [
                    '1 Photographer chính + 1 Photographer phụ',
                    '1 Trợ lý chụp',
                    '1 Makeup Artist chuyên nghiệp',
                    '5-6 giờ chụp',
                    '80 ảnh retouch cao cấp',
                    'Nhiều concept độc đáo',
                    'Album photobook cao cấp 20x30cm',
                    'Video highlight clip',
                    'Chụp tại nhiều địa điểm'
                ],
                'is_active': True,
                'popularity_score': 0
            },

            # WEDDING PACKAGES
            {
                'name': 'Gói Wedding Basic',
                'category': 'wedding',
                'price': 8000000,
                'description': 'Gói chụp cưới cơ bản cho ngày trọng đại',
                'details': {
                    'photo': 2,
                    'makeup': 1,
                    'assistant': 1,
                    'retouch': 100,
                    'time': 'Full day',
                    'location': 'Nhà + Lễ cưới',
                    'retouch_photos': 100,
                    'extra_services': ['Theo dõi cả ngày']
                },
                'includes': [
                    '2 Photographers (chính + phụ)',
                    '1 Trợ lý chụp',
                    '1 Makeup Artist',
                    'Chụp full day (sáng đến tối)',
                    '100 ảnh retouch chuyên nghiệp',
                    'Album photobook cơ bản',
                    'Theo dõi từ nhà đến tiệc cưới'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Wedding Standard',
                'category': 'wedding',
                'price': 15000000,
                'description': 'Gói chụp cưới tiêu chuẩn với video',
                'details': {
                    'photo': 2,
                    'makeup': 2,
                    'assistant': 2,
                    'retouch': 150,
                    'time': 'Full day + Pre-wedding',
                    'location': 'Pre-wedding + Ngày cưới',
                    'retouch_photos': 150,
                    'extra_services': ['Video highlight', 'Album cao cấp']
                },
                'includes': [
                    '2 Photographers chuyên nghiệp',
                    '2 Trợ lý chụp',
                    '2 Makeup Artists',
                    'Chụp Pre-wedding (1 ngày)',
                    'Chụp ngày cưới full day',
                    '150 ảnh retouch cao cấp',
                    'Album photobook cao cấp 30x40cm',
                    'Video highlight 5-7 phút',
                    'USB tất cả ảnh gốc'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Wedding Premium',
                'category': 'wedding',
                'price': 25000000,
                'description': 'Gói chụp cưới cao cấp với dịch vụ hoàn hảo',
                'details': {
                    'photo': 3,
                    'makeup': 2,
                    'assistant': 2,
                    'retouch': 200,
                    'time': 'Pre-wedding 2 ngày + Wedding day',
                    'location': 'Pre-wedding đa địa điểm + Ngày cưới',
                    'retouch_photos': 200,
                    'extra_services': ['Full video', 'Drone', 'Album premium', 'Canvas prints']
                },
                'includes': [
                    '3 Photographers (1 chính + 2 phụ)',
                    '2 Trợ lý chụp',
                    '2 Makeup Artists chuyên nghiệp',
                    'Chụp Pre-wedding 2 ngày (có thể chụp ở resort)',
                    'Chụp ngày cưới full day',
                    '200 ảnh retouch cao cấp',
                    '2 Album photobook cao cấp 40x50cm',
                    'Video cinematic full 15-20 phút',
                    'Video highlight 5-7 phút',
                    'Flycam/Drone cho Pre-wedding',
                    '5 Canvas prints 50x70cm',
                    'USB tất cả ảnh gốc + video'
                ],
                'is_active': True,
                'popularity_score': 0
            },

            # EVENT PACKAGES
            {
                'name': 'Gói Event Basic',
                'category': 'event',
                'price': 3000000,
                'description': 'Gói chụp sự kiện cơ bản',
                'details': {
                    'photo': 1,
                    'makeup': 0,
                    'assistant': 0,
                    'retouch': 50,
                    'time': '4 giờ',
                    'location': 'Địa điểm sự kiện',
                    'retouch_photos': 50,
                    'extra_services': ['Theo dõi sự kiện']
                },
                'includes': [
                    '1 Photographer',
                    'Chụp 4 giờ tại sự kiện',
                    '50 ảnh retouch cơ bản',
                    'Giao ảnh trong 7 ngày',
                    'File ảnh online drive'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Event Standard',
                'category': 'event',
                'price': 5000000,
                'description': 'Gói chụp sự kiện tiêu chuẩn với video',
                'details': {
                    'photo': 2,
                    'makeup': 0,
                    'assistant': 1,
                    'retouch': 100,
                    'time': '6 giờ',
                    'location': 'Địa điểm sự kiện',
                    'retouch_photos': 100,
                    'extra_services': ['Video highlight']
                },
                'includes': [
                    '2 Photographers',
                    '1 Trợ lý chụp',
                    'Chụp 6 giờ tại sự kiện',
                    '100 ảnh retouch chuyên nghiệp',
                    'Video highlight 3-5 phút',
                    'Giao ảnh trong 5 ngày',
                    'USB + File online'
                ],
                'is_active': True,
                'popularity_score': 0
            },

            # COMMERCIAL PACKAGES
            {
                'name': 'Gói Commercial Basic',
                'category': 'commercial',
                'price': 5000000,
                'description': 'Gói chụp sản phẩm/quảng cáo cơ bản',
                'details': {
                    'photo': 1,
                    'makeup': 0,
                    'assistant': 1,
                    'retouch': 30,
                    'time': '4 giờ',
                    'location': 'Studio',
                    'retouch_photos': 30,
                    'extra_services': ['Chụp sản phẩm']
                },
                'includes': [
                    '1 Photographer chuyên nghiệp',
                    '1 Trợ lý chụp',
                    '4 giờ chụp tại studio',
                    '30 ảnh retouch cao cấp',
                    'Setup lighting chuyên nghiệp',
                    'Phù hợp cho sản phẩm, lookbook'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Commercial Standard',
                'category': 'commercial',
                'price': 10000000,
                'description': 'Gói chụp thương mại tiêu chuẩn với model',
                'details': {
                    'photo': 2,
                    'makeup': 1,
                    'assistant': 2,
                    'retouch': 60,
                    'time': '8 giờ',
                    'location': 'Studio + outdoor',
                    'retouch_photos': 60,
                    'extra_services': ['Model', 'Styling', 'Props']
                },
                'includes': [
                    '2 Photographers chuyên nghiệp',
                    '2 Trợ lý chụp',
                    '1 Makeup Artist',
                    '1 Stylist',
                    '8 giờ chụp',
                    '60 ảnh retouch chuyên nghiệp',
                    'Thuê model (nếu cần)',
                    'Props và styling',
                    'Phù hợp cho TVC, catalog, lookbook'
                ],
                'is_active': True,
                'popularity_score': 0
            },
            {
                'name': 'Gói Commercial Premium',
                'category': 'commercial',
                'price': 20000000,
                'description': 'Gói chụp thương mại cao cấp toàn diện',
                'details': {
                    'photo': 3,
                    'makeup': 2,
                    'assistant': 2,
                    'retouch': 100,
                    'time': '2 ngày',
                    'location': 'Đa địa điểm',
                    'retouch_photos': 100,
                    'extra_services': ['Video TVC', 'Models', 'Full production']
                },
                'includes': [
                    '3 Photographers chuyên nghiệp',
                    '2 Trợ lý chụp',
                    '2 Makeup Artists',
                    '1-2 Stylists',
                    'Chụp 2 ngày',
                    '100 ảnh retouch cao cấp',
                    'Video TVC 30s-1 phút',
                    'Thuê models chuyên nghiệp',
                    'Full production team',
                    'Props, styling, location scouting',
                    'Phù hợp cho campaign lớn'
                ],
                'is_active': True,
                'popularity_score': 0
            },
        ]

        created_count = 0
        updated_count = 0

        for package_data in packages_data:
            # Check if package already exists by name
            existing_package = Package.objects.filter(name=package_data['name']).first()

            if existing_package:
                # Update existing package
                for key, value in package_data.items():
                    setattr(existing_package, key, value)
                existing_package.save()
                updated_count += 1
                self.stdout.write(f'  Updated: {package_data["name"]}')
            else:
                # Create new package
                Package.objects.create(**package_data)
                created_count += 1
                self.stdout.write(f'  Created: {package_data["name"]}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully seeded packages!\n'
                f'Created: {created_count}\n'
                f'Updated: {updated_count}\n'
                f'Total: {created_count + updated_count}'
            )
        )
