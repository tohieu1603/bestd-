"""
API integration tests cho Package endpoints.
"""
import pytest
import json
from django.test import TestCase, Client
from apps.packages.models import Package
from apps.users.models import User
from apps.users.services import create_jwt_token


@pytest.mark.django_db
class TestPackageAPI(TestCase):
    """Test suite cho Package API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            role='admin'
        )
        self.manager_user = User.objects.create_user(
            username='manager',
            email='manager@test.com',
            password='manager123',
            role='manager'
        )

    def tearDown(self):
        """Clean up test data."""
        Package.objects.all().delete()
        User.objects.all().delete()

    def _get_auth_header(self, user):
        """Helper to get JWT auth header."""
        token = create_jwt_token(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def test_create_package_success(self):
        """Test creating package successfully."""
        # Arrange
        auth_header = self._get_auth_header(self.admin_user)
        payload = {
            'name': 'Wedding Premium',
            'category': 'wedding',
            'price': 8000000,
            'description': 'Gói chụp cưới cao cấp',
            'is_active': True
        }

        # Act
        response = self.client.post(
            '/api/packages/',
            data=json.dumps(payload),
            content_type='application/json',
            **auth_header
        )

        # Assert
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'Wedding Premium')
        self.assertEqual(data['price'], 8000000)

    def test_list_packages_success(self):
        """Test listing packages."""
        # Arrange
        Package.objects.create(
            name='Package 1',
            category='wedding',
            price=5000000,
            created_by=self.admin_user
        )
        Package.objects.create(
            name='Package 2',
            category='event',
            price=3000000,
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.get('/api/packages/', **auth_header)

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['total'], 2)
        self.assertEqual(len(data['items']), 2)

    def test_list_packages_with_category_filter(self):
        """Test listing packages with category filter."""
        # Arrange
        Package.objects.create(
            name='Wedding Package',
            category='wedding',
            price=5000000,
            created_by=self.admin_user
        )
        Package.objects.create(
            name='Event Package',
            category='event',
            price=3000000,
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.get('/api/packages/?category=wedding', **auth_header)

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Wedding Package')

    def test_list_packages_with_price_filter(self):
        """Test listing packages with price range filter."""
        # Arrange
        Package.objects.create(
            name='Cheap Package',
            category='event',
            price=2000000,
            created_by=self.admin_user
        )
        Package.objects.create(
            name='Premium Package',
            category='wedding',
            price=10000000,
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.get('/api/packages/?min_price=5000000', **auth_header)

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Premium Package')

    def test_get_package_by_id_success(self):
        """Test getting package by ID."""
        # Arrange
        package = Package.objects.create(
            name='Test Package',
            category='wedding',
            price=5000000,
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.get(f'/api/packages/{package.id}', **auth_header)

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'Test Package')

    def test_get_package_not_found(self):
        """Test getting non-existent package returns 404."""
        # Arrange
        from uuid import uuid4
        fake_id = uuid4()
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.get(f'/api/packages/{fake_id}', **auth_header)

        # Assert
        self.assertEqual(response.status_code, 404)

    def test_update_package_success(self):
        """Test updating package."""
        # Arrange
        package = Package.objects.create(
            name='Old Name',
            category='wedding',
            price=5000000,
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)
        payload = {
            'name': 'New Name',
            'price': 6000000
        }

        # Act
        response = self.client.put(
            f'/api/packages/{package.id}',
            data=json.dumps(payload),
            content_type='application/json',
            **auth_header
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'New Name')
        self.assertEqual(data['price'], 6000000)

    def test_partial_update_package_success(self):
        """Test partial update (PATCH) package."""
        # Arrange
        package = Package.objects.create(
            name='Original Name',
            category='wedding',
            price=5000000,
            description='Original description',
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)
        payload = {
            'price': 7000000
        }

        # Act
        response = self.client.patch(
            f'/api/packages/{package.id}',
            data=json.dumps(payload),
            content_type='application/json',
            **auth_header
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'Original Name')  # Unchanged
        self.assertEqual(data['price'], 7000000)  # Updated

    def test_delete_package_success(self):
        """Test deleting package (soft delete)."""
        # Arrange
        package = Package.objects.create(
            name='To Delete',
            category='event',
            price=3000000,
            is_active=True,
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.delete(
            f'/api/packages/{package.id}',
            **auth_header
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

        # Verify soft delete
        package.refresh_from_db()
        self.assertFalse(package.is_active)

    def test_get_packages_by_category_endpoint(self):
        """Test get packages by category endpoint."""
        # Arrange
        Package.objects.create(
            name='Wedding 1',
            category='wedding',
            price=5000000,
            is_active=True,
            created_by=self.admin_user
        )
        Package.objects.create(
            name='Wedding 2',
            category='wedding',
            price=7000000,
            is_active=True,
            created_by=self.admin_user
        )
        Package.objects.create(
            name='Event 1',
            category='event',
            price=3000000,
            is_active=True,
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.get('/api/packages/category/wedding', **auth_header)

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        for package in data:
            self.assertEqual(package['category'], 'wedding')

    def test_get_popular_packages_endpoint(self):
        """Test get popular packages endpoint."""
        # Arrange
        Package.objects.create(
            name='Popular 1',
            category='wedding',
            price=5000000,
            popularity_score=10,
            is_active=True,
            created_by=self.admin_user
        )
        Package.objects.create(
            name='Popular 2',
            category='event',
            price=3000000,
            popularity_score=5,
            is_active=True,
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.get('/api/packages/popular/top?limit=2', **auth_header)

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Popular 1')  # Higher score first

    def test_increment_popularity_endpoint(self):
        """Test increment popularity endpoint."""
        # Arrange
        package = Package.objects.create(
            name='Test Package',
            category='wedding',
            price=5000000,
            popularity_score=0,
            is_active=True,
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.post(
            f'/api/packages/{package.id}/increment-popularity',
            **auth_header
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['popularity_score'], 1)

    def test_search_packages_endpoint(self):
        """Test searching packages."""
        # Arrange
        Package.objects.create(
            name='Wedding Premium',
            category='wedding',
            price=8000000,
            description='Gói chụp cưới cao cấp',
            created_by=self.admin_user
        )
        Package.objects.create(
            name='Event Standard',
            category='event',
            price=4000000,
            description='Gói chụp sự kiện',
            created_by=self.admin_user
        )
        auth_header = self._get_auth_header(self.admin_user)

        # Act
        response = self.client.get('/api/packages/?search=Premium', **auth_header)

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['items'][0]['name'], 'Wedding Premium')
