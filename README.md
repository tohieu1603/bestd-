# Studio Management Backend API

Django-based REST API for managing studio projects, employees, salaries, and financial operations.

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Deployment](#deployment)

## Overview

This backend service provides a comprehensive API for studio management, including:
- User authentication and authorization
- Employee management
- Project tracking
- Package management
- Partner relationships
- Salary calculations
- Financial reporting

## Technology Stack

- **Framework**: Django 5.0.1
- **API**: Django Ninja 1.1.0
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **Authentication**: JWT (PyJWT)
- **Validation**: Pydantic 2.5.3
- **Server**: Gunicorn

## Setup Instructions

### Prerequisites

- Python 3.12+
- PostgreSQL 16
- Redis 7
- pip and virtualenv

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Setup database**
   ```bash
   # Create PostgreSQL database
   createdb studio_db

   # Run migrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

   API will be available at: http://localhost:8000
   API Documentation: http://localhost:8000/api/docs

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   cd ..  # Go to project root
   docker-compose up -d
   ```

2. **Run migrations in container**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

3. **Create superuser in container**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

## API Endpoints

### System
- `GET /api/health/` - Health check endpoint

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login (returns JWT token)
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/me/` - Get current user profile
- `PUT /api/auth/me/` - Update current user profile
- `POST /api/auth/change-password/` - Change password

### Employees
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee
- `GET /api/employees/{id}/projects/` - Get employee's projects
- `GET /api/employees/{id}/salaries/` - Get employee's salary history

### Projects
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create new project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project
- `POST /api/projects/{id}/assign-employee/` - Assign employee to project
- `POST /api/projects/{id}/complete/` - Mark project as completed

### Packages
- `GET /api/packages/` - List all packages
- `POST /api/packages/` - Create new package
- `GET /api/packages/{id}/` - Get package details
- `PUT /api/packages/{id}/` - Update package
- `DELETE /api/packages/{id}/` - Delete package

### Partners
- `GET /api/partners/` - List all partners
- `POST /api/partners/` - Create new partner
- `GET /api/partners/{id}/` - Get partner details
- `PUT /api/partners/{id}/` - Update partner
- `DELETE /api/partners/{id}/` - Delete partner
- `GET /api/partners/{id}/projects/` - Get partner's projects

### Salaries
- `GET /api/salaries/` - List all salary records
- `POST /api/salaries/calculate/` - Calculate monthly salaries
- `GET /api/salaries/{id}/` - Get salary details
- `POST /api/salaries/{id}/pay/` - Mark salary as paid
- `GET /api/salaries/monthly-report/` - Get monthly salary report

### Finance
- `GET /api/finance/dashboard/` - Financial dashboard overview
- `GET /api/finance/monthly-summary/` - Monthly financial summary
- `GET /api/finance/revenue-by-project/` - Revenue breakdown by project
- `GET /api/finance/expense-report/` - Expense report

## Development Workflow

### Code Style

This project uses pre-commit hooks to ensure code quality:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

Tools used:
- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Linting
- **mypy**: Type checking

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest tests/test_users.py

# Run specific test
pytest tests/test_users.py::test_user_registration
```

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration history
python manage.py showmigrations

# Rollback migration
python manage.py migrate app_name migration_name
```

### Django Shell

```bash
# Standard shell
python manage.py shell

# IPython shell (enhanced)
python manage.py shell_plus
```

### Create New App

```bash
# Create new Django app
python manage.py startapp app_name apps/app_name
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Pytest fixtures
├── factories.py         # Factory Boy factories
├── test_users.py        # User tests
├── test_employees.py    # Employee tests
├── test_projects.py     # Project tests
├── test_salaries.py     # Salary tests
└── test_finance.py      # Finance tests
```

### Writing Tests

```python
import pytest
from apps.users.models import User

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    assert user.username == "testuser"
    assert user.check_password("testpass123")
```

### Test Coverage

Aim for 80%+ code coverage. View coverage report:

```bash
pytest --cov=apps --cov-report=html
open htmlcov/index.html  # View in browser
```

## Deployment

### Environment Variables

Required environment variables for production:

```env
# Django
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=<strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://:password@host:6379/0

# JWT
JWT_SECRET_KEY=<jwt-secret-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# App Settings
STUDIO_NAME=Your Studio Name
FIXED_MONTHLY_RENT=20700000
```

### Docker Production Build

```bash
# Build production image
docker build --target production -t studio-backend:latest .

# Run container
docker run -d \
  --name studio-backend \
  -p 8000:8000 \
  --env-file .env \
  studio-backend:latest
```

### Health Checks

The application exposes a health check endpoint at `/api/health/` which returns:

```json
{
  "status": "ok",
  "message": "API is running",
  "version": "1.0.0"
}
```

### Performance Tuning

- **Gunicorn workers**: `(2 x CPU cores) + 1`
- **Database connection pooling**: Configured in settings
- **Redis caching**: Enabled for frequently accessed data
- **Static files**: Served via WhiteNoise or CDN

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check PostgreSQL is running
   - Verify DATABASE_URL is correct
   - Check network connectivity

2. **Migration conflicts**
   ```bash
   python manage.py migrate --fake app_name migration_name
   ```

3. **Static files not loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Redis connection issues**
   - Check Redis is running
   - Verify REDIS_URL is correct
   - Test connection: `redis-cli ping`

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Add your feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Create Pull Request

## License

Proprietary - All rights reserved

## Contact

For questions or support, contact: your-email@example.com
