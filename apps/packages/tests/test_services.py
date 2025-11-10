"""
Unit tests cho PackageService.
"""
import pytest
from django.test import TestCase
from apps.packages.models import Package
from apps.packages.services import PackageService
from apps.packages.schemas import PackageCreate, PackageUpdate
from apps.users.models import User


@pytest.mark.django_db
class TestPackageService(TestCase):
    """Test suite cho PackageService."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )

    def tearDown(self):
        """Clean up test data."""
        Package.objects.all().delete()
        User.objects.all().delete()

    def test_create_package_success(self):
        """Test creating a package successfully."""
        # Arrange
        package_data = PackageCreate(
            name='Wedding Basic',
            category='wedding',
            price=5000000,
            description='Gói chụp cưới cơ bản',
            is_active=True
        )

        # Act
        package = PackageService.create_package(package_data, created_by=self.user)

        # Assert
        self.assertIsNotNone(package)
        self.assertEqual(package.name, 'Wedding Basic')
        self.assertEqual(package.category, 'wedding')
        self.assertEqual(package.price, 5000000)
        self.assertTrue(package.is_active)

    def test_update_package_success(self):
        """Test updating package successfully."""
        # Arrange
        package = Package.objects.create(
            name='Old Name',
            category='wedding',
            price=3000000,
            created_by=self.user
        )
        update_data = PackageUpdate(
            name='New Name',
            price=4000000
        )

        # Act
        updated_package = PackageService.update_package(package.id, update_data)

        # Assert
        self.assertIsNotNone(updated_package)
        self.assertEqual(updated_package.name, 'New Name')
        self.assertEqual(updated_package.price, 4000000)
        self.assertEqual(updated_package.category, 'wedding')  # Unchanged

    def test_get_package_by_id(self):
        """Test getting package by ID."""
        # Arrange
        package = Package.objects.create(
            name='Test Package',
            category='event',
            price=2000000,
            created_by=self.user
        )

        # Act
        retrieved_package = PackageService.get_package(package.id)

        # Assert
        self.assertIsNotNone(retrieved_package)
        self.assertEqual(retrieved_package.id, package.id)
        self.assertEqual(retrieved_package.name, 'Test Package')

    def test_get_package_not_found(self):
        """Test getting non-existent package returns None."""
        # Arrange
        from uuid import uuid4
        fake_id = uuid4()

        # Act
        package = PackageService.get_package(fake_id)

        # Assert
        self.assertIsNone(package)

    def test_list_packages_with_filters(self):
        """Test listing packages with various filters."""
        # Arrange
        Package.objects.create(
            name='Wedding Pro',
            category='wedding',
            price=8000000,
            is_active=True,
            created_by=self.user
        )
        Package.objects.create(
            name='Event Basic',
            category='event',
            price=3000000,
            is_active=True,
            created_by=self.user
        )
        Package.objects.create(
            name='Wedding Deluxe',
            category='wedding',
            price=15000000,
            is_active=False,
            created_by=self.user
        )

        # Act - Filter by category
        packages, total = PackageService.list_packages(category='wedding')

        # Assert
        self.assertEqual(total, 2)
        self.assertEqual(len(packages), 2)

        # Act - Filter by is_active
        packages, total = PackageService.list_packages(is_active=True)

        # Assert
        self.assertEqual(total, 2)

        # Act - Filter by price range
        packages, total = PackageService.list_packages(
            min_price=5000000,
            max_price=10000000
        )

        # Assert
        self.assertEqual(total, 1)
        self.assertEqual(packages[0].name, 'Wedding Pro')

    def test_search_packages(self):
        """Test searching packages by name."""
        # Arrange
        Package.objects.create(
            name='Wedding Premium',
            category='wedding',
            price=10000000,
            description='Gói chụp cưới cao cấp',
            created_by=self.user
        )
        Package.objects.create(
            name='Event Standard',
            category='event',
            price=5000000,
            description='Gói chụp sự kiện',
            created_by=self.user
        )

        # Act
        packages, total = PackageService.list_packages(search='wedding')

        # Assert
        self.assertEqual(total, 1)
        self.assertEqual(packages[0].name, 'Wedding Premium')

    def test_delete_package_soft_delete(self):
        """Test deleting package (soft delete)."""
        # Arrange
        package = Package.objects.create(
            name='To Delete',
            category='event',
            price=2000000,
            is_active=True,
            created_by=self.user
        )

        # Act
        success = PackageService.delete_package(package.id)

        # Assert
        self.assertTrue(success)
        package.refresh_from_db()
        self.assertFalse(package.is_active)

    def test_get_packages_by_category(self):
        """Test getting packages by specific category."""
        # Arrange
        Package.objects.create(
            name='Wedding 1',
            category='wedding',
            price=5000000,
            is_active=True,
            created_by=self.user
        )
        Package.objects.create(
            name='Wedding 2',
            category='wedding',
            price=7000000,
            is_active=True,
            created_by=self.user
        )
        Package.objects.create(
            name='Event 1',
            category='event',
            price=3000000,
            is_active=True,
            created_by=self.user
        )

        # Act
        packages = PackageService.get_packages_by_category('wedding')

        # Assert
        self.assertEqual(len(packages), 2)
        for package in packages:
            self.assertEqual(package.category, 'wedding')

    def test_get_popular_packages(self):
        """Test getting popular packages."""
        # Arrange
        pkg1 = Package.objects.create(
            name='Popular 1',
            category='wedding',
            price=5000000,
            popularity_score=10,
            is_active=True,
            created_by=self.user
        )
        pkg2 = Package.objects.create(
            name='Popular 2',
            category='event',
            price=3000000,
            popularity_score=5,
            is_active=True,
            created_by=self.user
        )

        # Act
        packages = PackageService.get_popular_packages(limit=2)

        # Assert
        self.assertEqual(len(packages), 2)
        self.assertEqual(packages[0].name, 'Popular 1')  # Higher score first
        self.assertEqual(packages[1].name, 'Popular 2')

    def test_increment_popularity(self):
        """Test incrementing package popularity."""
        # Arrange
        package = Package.objects.create(
            name='Test Package',
            category='wedding',
            price=5000000,
            popularity_score=0,
            is_active=True,
            created_by=self.user
        )

        # Act
        updated_package = PackageService.increment_popularity(package.id)

        # Assert
        self.assertIsNotNone(updated_package)
        self.assertEqual(updated_package.popularity_score, 1)

        # Act again
        updated_package = PackageService.increment_popularity(package.id)

        # Assert
        self.assertEqual(updated_package.popularity_score, 2)

    def test_pagination(self):
        """Test pagination for list_packages."""
        # Arrange - Create 5 packages
        for i in range(5):
            Package.objects.create(
                name=f'Package {i}',
                category='wedding',
                price=5000000,
                is_active=True,
                created_by=self.user
            )

        # Act - Get first 2
        packages, total = PackageService.list_packages(skip=0, limit=2)

        # Assert
        self.assertEqual(total, 5)
        self.assertEqual(len(packages), 2)

        # Act - Get next 2
        packages, total = PackageService.list_packages(skip=2, limit=2)

        # Assert
        self.assertEqual(total, 5)
        self.assertEqual(len(packages), 2)
