"""
Permission decorators for role-based access control.
"""
from functools import wraps
from ninja.errors import HttpError


def require_roles(*allowed_roles):
    """
    Decorator to check if user has required role.
    Usage: @require_roles('admin', 'Manager')
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                raise HttpError(401, "Authentication required")

            user_role = getattr(request.user, 'role', None)
            if user_role not in allowed_roles:
                raise HttpError(403, f"Permission denied. Required roles: {', '.join(allowed_roles)}")

            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_admin(func):
    """
    Decorator to require admin role.
    Usage: @require_admin
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            raise HttpError(401, "Authentication required")

        if getattr(request.user, 'role', None) != 'admin':
            raise HttpError(403, "Admin access required")

        return func(request, *args, **kwargs)
    return wrapper


def require_auth(func):
    """
    Decorator to require authentication.
    Usage: @require_auth
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            raise HttpError(401, "Authentication required")

        return func(request, *args, **kwargs)
    return wrapper
