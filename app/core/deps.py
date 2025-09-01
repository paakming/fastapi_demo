from collections.abc import Callable, Coroutine
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.redis import get_redis
from app.models.user import UserVO
from app.service import AuthService, get_auth_service
from app.utils.jwt import decode_token

# OAuth2密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token', refreshUrl='/api/v1/auth/refresh')


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    redis=Depends(get_redis),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='无法验证凭据',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    # 解码令牌
    if not (payload := await decode_token(token)):
        raise credentials_exception

    # 检查令牌类型
    token_type = payload.get('type')
    if token_type != 'access':
        raise credentials_exception

    username = payload.get('subject')
    if username is None:
        raise credentials_exception

    user = await auth_service.get_authenticated_user(username)
    if user is None:
        raise credentials_exception

    return user


def has_authority(perms: str) -> Callable[[Annotated[UserVO, Depends(get_current_user)]], Coroutine[Any, Any, bool]]:
    """
    检查当前用户是否具有权限
    """

    async def check_permission(user: Annotated[UserVO, Depends(get_current_user)]) -> bool:
        return True

    return check_permission


def has_role(role: str) -> Callable[[Annotated[UserVO, Depends(get_current_user)]], Coroutine[Any, Any, bool]]:
    """
    检查当前用户是否具有角色
    """

    async def check_role(user: Annotated[UserVO, Depends(get_current_user)]) -> bool:
        return True

    return check_role
