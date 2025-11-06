"""
User authentication API endpoints.
"""
from ninja import Router
from ninja.errors import HttpError
from django.contrib.auth import authenticate
from .schemas import (
    LoginSchema,
    TokenSchema,
    UserSchema,
    PasswordChangeSchema,
)
from .services import create_jwt_token, verify_jwt_token
from api.main import AuthBearer

router = Router()


@router.post("/login", auth=None)
def login(request, payload: LoginSchema):
    """
    User login endpoint.
    Returns JWT token on successful authentication.
    """
    from .models import User

    try:
        user = User.objects.get(username=payload.username)
        if user.check_password(payload.password):
            token = create_jwt_token(user)
            return {
                "success": True,
                "token": token,
                "message": "Login successful",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat(),
                }
            }
    except User.DoesNotExist:
        pass

    raise HttpError(401, "Invalid credentials")


@router.get("/me", auth=AuthBearer())
def get_current_user(request):
    """
    Get current authenticated user.
    """
    user = request.auth
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }


@router.post("/change-password", auth=AuthBearer())
def change_password(request, payload: PasswordChangeSchema):
    """
    Change user password.
    """
    user = request.auth

    if not user.check_password(payload.old_password):
        raise HttpError(400, "Invalid old password")

    user.set_password(payload.new_password)
    user.save()

    return {"message": "Password changed successfully"}


@router.post("/logout", auth=AuthBearer())
def logout(request):
    """
    Logout endpoint (token invalidation handled on client side).
    """
    return {"message": "Logged out successfully"}
