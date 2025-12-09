from collections.abc import Callable, Coroutine
from datetime import datetime
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.redis import get_redis
from app.models.user import UserVO
from app.service import AuthService, get_auth_service
from app.utils.jwt import decode_token

# OAuth2密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    redis=Depends(get_redis),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token 无效',
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
    if not (exp := payload.get('exp')):
        raise credentials_exception
    if exp < datetime.now().timestamp():  # 令牌已过期
        raise credentials_exception

    user = await auth_service.get_authenticated_user(username)
    if user is None:
        raise credentials_exception

    return user


def has_authority(perms: str):
    """
    检查当前用户是否具有权限，支持通配符模式
    例如：如果用户有sys:user:*权限，那么请求sys:user:read时应该匹配成功
    """

    async def check_permission(user: Annotated[UserVO, Depends(get_current_user)]) -> bool:
        # 检查精确匹配
        if perms in user.permissions:
            return True

        for perm in user.permissions:
            if perm.endswith('*'):
                prefix = perm[:-1]
                if perms.startswith(prefix):
                    return True

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='无权限')

    return check_permission


def has_role(role: str) -> Callable[[Annotated[UserVO, Depends(get_current_user)]], Coroutine[Any, Any, bool]]:
    """
    检查当前用户是否具有角色
    """

    async def check_role(user: Annotated[UserVO, Depends(get_current_user)]) -> bool:
        if role in user.roles:
            return True

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='无权限')

    return check_role
