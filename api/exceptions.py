"""
Global exception handlers for the API.
"""
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied, ObjectDoesNotExist
from pydantic import ValidationError as PydanticValidationError
import logging
import json

logger = logging.getLogger(__name__)


def serialize_pydantic_errors(errors):
    """Convert Pydantic errors to JSON-serializable format."""
    serialized = []
    for error in errors:
        error_dict = {}
        for key, value in error.items():
            if key == 'ctx' and isinstance(value, dict):
                # Serialize context values
                error_dict[key] = {k: str(v) for k, v in value.items()}
            else:
                error_dict[key] = str(value) if not isinstance(value, (str, int, float, bool, type(None), list, dict)) else value
        serialized.append(error_dict)
    return serialized


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
        try:
            details = serialize_pydantic_errors(exc.errors())
        except Exception as e:
            logger.error(f"Error serializing Pydantic errors: {e}")
            details = str(exc)

        return JsonResponse({
            "success": False,
            "error": "Validation error",
            "details": details,
            "status_code": 422
        }, status=422)

    # Python ValueError (from Pydantic validators)
    if isinstance(exc, ValueError):
        return JsonResponse({
            "success": False,
            "error": str(exc),
            "status_code": 400
        }, status=400)

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
