from .auth import router as auth_router
from .role import router as role_router
from .user import router as user_router

__all__ = [
    'user_router',
    'auth_router',
    'role_router',
]
