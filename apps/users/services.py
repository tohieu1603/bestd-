"""
User authentication services.
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import User


def create_jwt_token(user: User) -> str:
    """
    Create JWT token for user.
    """
    payload = {
        'user_id': str(user.id),
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(days=settings.JWT_EXPIRATION_DAYS),
        'iat': datetime.utcnow(),
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def verify_jwt_token(token: str):
    """
    Verify JWT token and return user.
    Returns None if token is invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get('user_id')
        if not user_id:
            return None

        user = User.objects.get(id=user_id, is_active=True)
        return user

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None
