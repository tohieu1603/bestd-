"""
Global exception handlers for the API.
"""
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied, ObjectDoesNotExist
from pydantic import ValidationError as PydanticValidationError
import logging

logger = logging.getLogger(__name__)


class APIException(Exception):
    """Base API exception."""
    status_code = 400
    default_message = "An error occurred"

    def __init__(self, message=None, status_code=None):
        self.message = message or self.default_message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(APIException):
    """Resource not found exception."""
    status_code = 404
    default_message = "Resource not found"


class UnauthorizedError(APIException):
    """Unauthorized access exception."""
    status_code = 401
    default_message = "Unauthorized access"


class ForbiddenError(APIException):
    """Forbidden access exception."""
    status_code = 403
    default_message = "Forbidden access"


class BadRequestError(APIException):
    """Bad request exception."""
    status_code = 400
    default_message = "Bad request"


def api_exception_handler(request, exc):
    """
    Global exception handler for API.
    """
    # Custom API exceptions
    if isinstance(exc, APIException):
        return JsonResponse({
            "success": False,
            "error": exc.message,
            "status_code": exc.status_code
        }, status=exc.status_code)

    # Django validation errors
    if isinstance(exc, ValidationError):
        return JsonResponse({
            "success": False,
            "error": "Validation error",
            "details": exc.message_dict if hasattr(exc, 'message_dict') else str(exc),
            "status_code": 400
        }, status=400)

    # Pydantic validation errors
    if isinstance(exc, PydanticValidationError):
        return JsonResponse({
            "success": False,
            "error": "Validation error",
            "details": exc.errors(),
            "status_code": 422
        }, status=422)

    # Django ObjectDoesNotExist
    if isinstance(exc, ObjectDoesNotExist):
        return JsonResponse({
            "success": False,
            "error": "Resource not found",
            "status_code": 404
        }, status=404)

    # Django PermissionDenied
    if isinstance(exc, PermissionDenied):
        return JsonResponse({
            "success": False,
            "error": "Permission denied",
            "status_code": 403
        }, status=403)

    # Log unexpected errors
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

    # Generic error response
    return JsonResponse({
        "success": False,
        "error": "Internal server error",
        "status_code": 500
    }, status=500)
