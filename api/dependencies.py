"""
Common dependencies for API endpoints.
"""
from typing import Optional
from ninja.security import HttpBearer
from apps.users.models import User
from apps.users.services import verify_jwt_token
from .exceptions import UnauthorizedError


class AuthBearer(HttpBearer):
    """JWT Bearer token authentication."""

    def authenticate(self, request, token: str) -> Optional[User]:
        """Authenticate user from JWT token."""
        user = verify_jwt_token(token)
        if not user:
            raise UnauthorizedError("Invalid or expired token")
        return user


# Create auth instance
auth_bearer = AuthBearer()


def get_current_user(request) -> User:
    """Get current authenticated user."""
    if not hasattr(request, 'auth') or not request.auth:
        raise UnauthorizedError("Authentication required")
    return request.auth


def require_admin(request) -> User:
    """Require admin role."""
    user = get_current_user(request)
    if user.role != 'admin':
        from .exceptions import ForbiddenError
        raise ForbiddenError("Admin access required")
    return user
