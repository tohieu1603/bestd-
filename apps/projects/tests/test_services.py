"""
Unit tests for Project services.
"""
import pytest
from datetime import date
from decimal import Decimal
from django.test import TestCase
from apps.projects.services import ProjectService
from apps.projects.models import Project
from apps.employees.models import Employee
from apps.packages.models import Package
from apps.users.models import User
from apps.projects.schemas import ProjectCreate, TeamSchema, TeamMemberSchema, PaymentSchema


@pytest.mark.django_db
class TestProjectService(TestCase):
    """Test cases for ProjectService."""

    def setUp(self):
        """Set up test data."""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='admin'
        )

        # Create test employee (photographer)
        self.photographer = Employee.objects.create(
            name='John Photographer',
            role='Photo/Retouch',
            phone='0123456789',
            email='photo@example.com',
            is_active=True,
            created_by=self.user
        )

        # Create inactive employee
        self.inactive_photographer = Employee.objects.create(
            name='Inactive Photographer',
            role='Photo/Retouch',
            phone='0987654321',
            email='inactive@example.com',
            is_active=False,
            created_by=self.user
        )

        # Create test package
        self.package = Package.objects.create(
            name='Wedding Basic',
            category='wedding',
            price=Decimal('5000000'),
            description='Basic wedding package',
            created_by=self.user
        )

    def test_create_project_success(self):
        """Test creating a project successfully."""
        # Arrange
        team_data = TeamSchema(
            main_photographer=TeamMemberSchema(
                employee=self.photographer.id,
                salary=1000000,
                bonus=200000
            )
        )

        payment_data = PaymentSchema(
            status='unpaid',
            deposit=3000000,
            final=5000000,
            paid=0
        )

        project_data = ProjectCreate(
            customer_name='Test Customer',
            customer_phone='0123456789',
            customer_email='customer@example.com',
            package_type=self.package.id,
            package_name='Wedding Basic',
            package_price=5000000,
            package_discount=0,
            shoot_date=date.today(),
            team=team_data,
            payment=payment_data
        )

        # Act
        project = ProjectService.create_project(project_data, created_by=self.user)

        # Assert
        self.assertIsNotNone(project)
        self.assertEqual(project.customer_name, 'Test Customer')
        self.assertEqual(project.status, 'pending')
        self.assertIsNotNone(project.team)

    def test_create_project_without_photographer_fails(self):
        """Test that creating project without photographer fails."""
        # Arrange
        project_data = ProjectCreate(
            customer_name='Test Customer',
            customer_phone='0123456789',
            package_type=self.package.id,
            package_name='Wedding Basic',
            package_price=5000000,
            package_discount=0,
            shoot_date=date.today(),
            team=None  # No team
        )

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            ProjectService.create_project(project_data, created_by=self.user)

        self.assertIn('Photographer chính', str(context.exception))

    def test_create_project_with_inactive_photographer_fails(self):
        """Test that creating project with inactive photographer fails."""
        # Arrange
        team_data = TeamSchema(
            main_photographer=TeamMemberSchema(
                employee=self.inactive_photographer.id,
                salary=1000000,
                bonus=200000
            )
        )

        project_data = ProjectCreate(
            customer_name='Test Customer',
            customer_phone='0123456789',
            package_type=self.package.id,
            package_name='Wedding Basic',
            package_price=5000000,
            package_discount=0,
            shoot_date=date.today(),
            team=team_data
        )

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            ProjectService.create_project(project_data, created_by=self.user)

        self.assertIn('nghỉ việc', str(context.exception))

    def test_create_project_with_negative_price_fails(self):
        """Test that negative price is rejected."""
        # Arrange
        from pydantic import ValidationError

        team_data = TeamSchema(
            main_photographer=TeamMemberSchema(
                employee=self.photographer.id,
                salary=1000000,
                bonus=200000
            )
        )

        # Act & Assert - Pydantic validates before service layer
        with self.assertRaises(ValidationError) as context:
            project_data = ProjectCreate(
                customer_name='Test Customer',
                customer_phone='0123456789',
                package_type=self.package.id,
                package_name='Wedding Basic',
                package_price=-5000000,  # Negative price
                package_discount=0,
                shoot_date=date.today(),
                team=team_data
            )

        self.assertIn('greater_than_equal', str(context.exception))

    def test_create_project_with_discount_greater_than_price_fails(self):
        """Test that discount > price is rejected."""
        # Arrange
        team_data = TeamSchema(
            main_photographer=TeamMemberSchema(
                employee=self.photographer.id,
                salary=1000000,
                bonus=200000
            )
        )

        project_data = ProjectCreate(
            customer_name='Test Customer',
            customer_phone='0123456789',
            package_type=self.package.id,
            package_name='Wedding Basic',
            package_price=5000000,
            package_discount=6000000,  # Discount > price
            shoot_date=date.today(),
            team=team_data
        )

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            ProjectService.create_project(project_data, created_by=self.user)

        self.assertIn('Chiết khấu', str(context.exception))

    def test_delete_completed_project_fails(self):
        """Test that deleting completed project fails."""
        # Arrange - Create a completed project
        project = Project.objects.create(
            customer_name='Test Customer',
            customer_phone='0123456789',
            package_type=self.package,
            package_name='Wedding Basic',
            package_price=5000000,
            package_discount=0,
            package_final_price=5000000,
            shoot_date=date.today(),
            status='completed',  # Completed status
            created_by=self.user
        )

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            ProjectService.delete_project(project.id)

        self.assertIn('hoàn thành', str(context.exception))

    def test_delete_cancelled_project_fails(self):
        """Test that deleting already cancelled project fails."""
        # Arrange - Create a cancelled project
        project = Project.objects.create(
            customer_name='Test Customer',
            customer_phone='0123456789',
            package_type=self.package,
            package_name='Wedding Basic',
            package_price=5000000,
            package_discount=0,
            package_final_price=5000000,
            shoot_date=date.today(),
            status='cancelled',  # Already cancelled
            created_by=self.user
        )

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            ProjectService.delete_project(project.id)

        self.assertIn('đã bị hủy', str(context.exception))

    def test_delete_pending_project_success(self):
        """Test deleting pending project successfully."""
        # Arrange
        project = Project.objects.create(
            customer_name='Test Customer',
            customer_phone='0123456789',
            package_type=self.package,
            package_name='Wedding Basic',
            package_price=5000000,
            package_discount=0,
            package_final_price=5000000,
            shoot_date=date.today(),
            status='pending',
            created_by=self.user
        )

        # Act
        result = ProjectService.delete_project(project.id)

        # Assert
        self.assertTrue(result)
        project.refresh_from_db()
        self.assertEqual(project.status, 'cancelled')

    def test_get_project_by_id(self):
        """Test retrieving project by ID."""
        # Arrange
        project = Project.objects.create(
            customer_name='Test Customer',
            customer_phone='0123456789',
            package_type=self.package,
            package_name='Wedding Basic',
            package_price=5000000,
            package_discount=0,
            package_final_price=5000000,
            shoot_date=date.today(),
            status='pending',
            created_by=self.user
        )

        # Act
        retrieved_project = ProjectService.get_project(project.id)

        # Assert
        self.assertIsNotNone(retrieved_project)
        self.assertEqual(retrieved_project.id, project.id)
        self.assertEqual(retrieved_project.customer_name, 'Test Customer')

    def test_list_projects_with_filters(self):
        """Test listing projects with status filter."""
        # Arrange - Create multiple projects
        Project.objects.create(
            customer_name='Customer 1',
            customer_phone='0111111111',
            package_type=self.package,
            package_name='Package 1',
            package_price=5000000,
            package_discount=0,
            package_final_price=5000000,
            shoot_date=date.today(),
            status='pending',
            created_by=self.user
        )
        Project.objects.create(
            customer_name='Customer 2',
            customer_phone='0222222222',
            package_type=self.package,
            package_name='Package 2',
            package_price=6000000,
            package_discount=0,
            package_final_price=6000000,
            shoot_date=date.today(),
            status='completed',
            created_by=self.user
        )

        # Act
        pending_projects, total = ProjectService.list_projects(status='pending')

        # Assert
        self.assertEqual(len(pending_projects), 1)
        self.assertEqual(pending_projects[0].customer_name, 'Customer 1')
