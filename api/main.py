"""
Main API instance configuration for Django Ninja.
"""
from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.http import JsonResponse
from .exceptions import api_exception_handler

# JWT Auth class
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        from apps.users.services import verify_jwt_token
        user = verify_jwt_token(token)
        return user

# Create API instance
api = NinjaAPI(
    title="Studio Management API",
    version="1.0.0",
    description="API for managing studio projects, employees, and salaries",
    docs_url="/docs",
)

# Register exception handler
@api.exception_handler(Exception)
def custom_exception_handler(request, exc):
    return api_exception_handler(request, exc)

# Health check endpoint
@api.get("/health", tags=["System"])
def health_check(request):
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "API is running",
        "version": "1.0.0"
    }

# Import and register routers
from apps.users.api import router as users_router
from apps.employees.api import router as employees_router
from apps.projects.api import router as projects_router
from apps.packages.api import router as packages_router
from apps.partners.api import router as partners_router
from apps.salaries.api import router as salaries_router
from apps.finance.api import router as finance_router

# Auth instance
auth = AuthBearer()

# Add routers with authentication
api.add_router("/auth/", users_router, tags=["Authentication"])
api.add_router("/employees/", employees_router, auth=auth, tags=["Employees"])
api.add_router("/projects/", projects_router, auth=auth, tags=["Projects"])
api.add_router("/packages/", packages_router, auth=auth, tags=["Packages"])
api.add_router("/partners/", partners_router, auth=auth, tags=["Partners"])
api.add_router("/salaries/", salaries_router, auth=auth, tags=["Salaries"])
api.add_router("/finance/", finance_router, auth=auth, tags=["Finance"])
