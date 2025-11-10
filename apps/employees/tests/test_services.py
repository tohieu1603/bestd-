"""
Unit tests for Employee services.
"""
import pytest
from django.test import TestCase
from apps.employees.services import EmployeeService
from apps.employees.models import Employee
from apps.employees.schemas import EmployeeCreate, EmployeeUpdate
from apps.users.models import User


@pytest.mark.django_db
class TestEmployeeService(TestCase):
    """Test cases for EmployeeService."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='admin'
        )

    def test_create_employee_success(self):
        """Test creating an employee successfully."""
        # Arrange
        employee_data = EmployeeCreate(
            name='John Doe',
            role='Photo/Retouch',
            phone='0123456789',
            email='john@example.com',
            base_salary=10000000
        )

        # Act
        employee = EmployeeService.create_employee(employee_data, created_by=self.user)

        # Assert
        self.assertIsNotNone(employee)
        self.assertEqual(employee.name, 'John Doe')
        self.assertEqual(employee.role, 'Photo/Retouch')
        self.assertTrue(employee.is_active)

    def test_deactivate_employee_success(self):
        """Test deactivating an employee."""
        # Arrange
        employee = Employee.objects.create(
            name='John Doe',
            role='Photo/Retouch',
            phone='0123456789',
            email='john@example.com',
            is_active=True,
            created_by=self.user
        )

        # Act
        result = EmployeeService.deactivate_employee(employee.id)

        # Assert
        self.assertIsNotNone(result)
        self.assertFalse(result.is_active)

    def test_activate_employee_success(self):
        """Test activating an employee."""
        # Arrange
        employee = Employee.objects.create(
            name='John Doe',
            role='Photo/Retouch',
            phone='0123456789',
            email='john@example.com',
            is_active=False,
            created_by=self.user
        )

        # Act
        result = EmployeeService.activate_employee(employee.id)

        # Assert
        self.assertIsNotNone(result)
        self.assertTrue(result.is_active)

    def test_delete_employee_success(self):
        """Test hard deleting an employee."""
        # Arrange
        employee = Employee.objects.create(
            name='John Doe',
            role='Photo/Retouch',
            phone='0123456789',
            email='john@example.com',
            is_active=True,
            created_by=self.user
        )
        employee_id = employee.id

        # Act
        result = EmployeeService.delete_employee(employee_id)

        # Assert
        self.assertTrue(result)
        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(id=employee_id)

    def test_update_employee_success(self):
        """Test updating employee information."""
        # Arrange
        employee = Employee.objects.create(
            name='John Doe',
            role='Photo/Retouch',
            phone='0123456789',
            email='john@example.com',
            is_active=True,
            created_by=self.user
        )

        update_data = EmployeeUpdate(
            name='John Updated',
            phone='0987654321'
        )

        # Act
        updated = EmployeeService.update_employee(employee.id, update_data)

        # Assert
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, 'John Updated')
        self.assertEqual(updated.phone, '0987654321')

    def test_get_employees_by_role(self):
        """Test getting employees by role."""
        # Arrange
        Employee.objects.create(
            name='Photographer 1',
            role='Photo/Retouch',
            phone='0111111111',
            is_active=True,
            created_by=self.user
        )
        Employee.objects.create(
            name='Photographer 2',
            role='Photo/Retouch',
            phone='0222222222',
            is_active=True,
            created_by=self.user
        )
        Employee.objects.create(
            name='Makeup Artist 1',
            role='Makeup Artist',
            phone='0333333333',
            is_active=True,
            created_by=self.user
        )

        # Act
        photographers = EmployeeService.get_employees_by_role('Photo/Retouch')

        # Assert
        self.assertEqual(len(photographers), 2)
        self.assertTrue(all(e.role == 'Photo/Retouch' for e in photographers))

    def test_get_active_employees_only(self):
        """Test getting only active employees."""
        # Arrange
        Employee.objects.create(
            name='Active Employee',
            role='Photo/Retouch',
            phone='0111111111',
            is_active=True,
            created_by=self.user
        )
        Employee.objects.create(
            name='Inactive Employee',
            role='Photo/Retouch',
            phone='0222222222',
            is_active=False,
            created_by=self.user
        )

        # Act
        active_employees = EmployeeService.get_active_employees()

        # Assert
        self.assertEqual(len(active_employees), 1)
        self.assertEqual(active_employees[0].name, 'Active Employee')

    def test_search_employees(self):
        """Test searching employees by name, email, or phone."""
        # Arrange
        Employee.objects.create(
            name='John Photographer',
            role='Photo/Retouch',
            phone='0123456789',
            email='john@example.com',
            is_active=True,
            created_by=self.user
        )
        Employee.objects.create(
            name='Jane Makeup',
            role='Makeup Artist',
            phone='0987654321',
            email='jane@example.com',
            is_active=True,
            created_by=self.user
        )

        # Act
        results = EmployeeService.search_employees('John')

        # Assert
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'John Photographer')
