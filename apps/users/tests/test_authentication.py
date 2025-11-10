"""
Tests cho User Authentication.
"""
import pytest
import json
from django.test import TestCase, Client
from apps.users.models import User
from apps.users.services import create_jwt_token, verify_jwt_token


@pytest.mark.django_db
class TestAuthentication(TestCase):
    """Test suite cho authentication."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

    def tearDown(self):
        """Clean up test data."""
        User.objects.all().delete()

    def test_register_success(self):
        """Test user registration successfully."""
        # Arrange
        payload = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpass123',
            'full_name': 'New User',
            'role': 'employee'
        }

        # Act
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('token', data)
        self.assertEqual(data['user']['username'], 'newuser')
        self.assertEqual(data['user']['email'], 'newuser@test.com')

        # Verify user created in database
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)
        self.assertEqual(user.role, 'employee')

    def test_register_duplicate_username_fails(self):
        """Test registration with duplicate username fails."""
        # Arrange
        User.objects.create_user(
            username='existing',
            email='existing@test.com',
            password='pass123'
        )
        payload = {
            'username': 'existing',
            'email': 'different@test.com',
            'password': 'pass456',
            'full_name': 'Test User',
            'role': 'employee'
        }

        # Act
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('Username already exists', data['detail'])

    def test_register_duplicate_email_fails(self):
        """Test registration with duplicate email fails."""
        # Arrange
        User.objects.create_user(
            username='user1',
            email='duplicate@test.com',
            password='pass123'
        )
        payload = {
            'username': 'user2',
            'email': 'duplicate@test.com',
            'password': 'pass456',
            'full_name': 'Test User',
            'role': 'employee'
        }

        # Act
        response = self.client.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('Email already exists', data['detail'])

    def test_login_success(self):
        """Test login with valid credentials."""
        # Arrange
        User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='employee'
        )
        payload = {
            'username': 'testuser',
            'password': 'testpass123'
        }

        # Act
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('token', data)
        self.assertEqual(data['user']['username'], 'testuser')

    def test_login_invalid_username_fails(self):
        """Test login with invalid username fails."""
        # Arrange
        payload = {
            'username': 'nonexistent',
            'password': 'anypassword'
        }

        # Act
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertIn('Invalid credentials', data['detail'])

    def test_login_invalid_password_fails(self):
        """Test login with invalid password fails."""
        # Arrange
        User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='correctpass'
        )
        payload = {
            'username': 'testuser',
            'password': 'wrongpass'
        }

        # Act
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Assert
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertIn('Invalid credentials', data['detail'])

    def test_jwt_token_creation_and_verification(self):
        """Test JWT token creation and verification."""
        # Arrange
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass',
            role='admin'
        )

        # Act - Create token
        token = create_jwt_token(user)

        # Assert - Token exists
        self.assertIsNotNone(token)
        self.assertTrue(len(token) > 0)

        # Act - Verify token
        verified_user = verify_jwt_token(token)

        # Assert - User correct
        self.assertIsNotNone(verified_user)
        self.assertEqual(verified_user.username, 'testuser')
        self.assertEqual(verified_user.role, 'admin')

    def test_get_current_user_success(self):
        """Test getting current authenticated user."""
        # Arrange
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass',
            role='manager'
        )
        token = create_jwt_token(user)

        # Act
        response = self.client.get(
            '/api/auth/me',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['role'], 'manager')

    def test_get_current_user_unauthorized(self):
        """Test getting current user without auth fails."""
        # Act
        response = self.client.get('/api/auth/me')

        # Assert
        self.assertEqual(response.status_code, 401)

    def test_change_password_success(self):
        """Test changing password successfully."""
        # Arrange
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='oldpass123'
        )
        token = create_jwt_token(user)
        payload = {
            'old_password': 'oldpass123',
            'new_password': 'newpass456'
        }

        # Act
        response = self.client.post(
            '/api/auth/change-password',
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('successfully', data['message'])

        # Verify password changed
        user.refresh_from_db()
        self.assertTrue(user.check_password('newpass456'))
        self.assertFalse(user.check_password('oldpass123'))

    def test_change_password_wrong_old_password(self):
        """Test changing password with wrong old password fails."""
        # Arrange
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='correctpass'
        )
        token = create_jwt_token(user)
        payload = {
            'old_password': 'wrongpass',
            'new_password': 'newpass123'
        }

        # Act
        response = self.client.post(
            '/api/auth/change-password',
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        # Assert
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('Invalid old password', data['detail'])

    def test_logout_success(self):
        """Test logout endpoint."""
        # Arrange
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass'
        )
        token = create_jwt_token(user)

        # Act
        response = self.client.post(
            '/api/auth/logout',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('Logged out', data['message'])

    def test_token_expiry_validation(self):
        """Test that token can be verified and returns user."""
        # Arrange
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass'
        )

        # Act
        token = create_jwt_token(user)
        verified_user = verify_jwt_token(token)

        # Assert - Verify token returns valid user
        self.assertIsNotNone(verified_user)
        self.assertEqual(verified_user.id, user.id)
        self.assertTrue(verified_user.is_active)
