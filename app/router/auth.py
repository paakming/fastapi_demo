from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.redis import get_redis
from app.exception import ServiceException
from app.models.response import ResultResponse, TokenResponse
from app.models.user import UserLoginDTO
from app.service import AuthService, get_auth_service
from app.utils.jwt import (
    add_token_to_blacklist,
    decode_token,
)

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post('/login', response_model=TokenResponse, summary='用户登录', description='用户登录')
async def login(user: UserLoginDTO, auth_service: AuthServiceDep):
    token: TokenResponse | None = await auth_service.authenticate_user(user.username, user.password)
    if token:
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='用户名或密码错误',
        headers={'WWW-Authenticate': 'Bearer'},
    )


@router.post(
    '/token',
    response_model=TokenResponse,
    summary='swagger登录用',
    description='swagger登录用',
)
async def login_swagger(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
):
    username = form_data.username
    password = form_data.password
    if username is None or password is None:
        raise ServiceException(code=400, message='用户名或密码不能为空')
    token: TokenResponse | None = await auth_service.authenticate_user(username, password)
    if token:
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='用户名或密码错误',
        headers={'WWW-Authenticate': 'Bearer'},
    )


@router.post(
    '/refresh', response_model=ResultResponse, summary='刷新令牌', description='用refresh_token刷新access_token'
)
async def refresh_token(refresh_token: str, auth_service: AuthServiceDep, redis=Depends(get_redis)):
    """
    使用刷新令牌获取新的访问令牌
    """
    token = await auth_service.refresh_token(refresh_token)
    if token:
        return ResultResponse.success(data=token)
    else:
        return ResultResponse.error(message='刷新令牌失败')


@router.post('/logout', response_model=ResultResponse, summary='退出登录', description='退出登录')
async def logout(refresh_token: str, redis=Depends(get_redis)):
    """
    登出用户，将刷新令牌加入黑名单
    """
    # 解码刷新令牌以获取过期时间
    payload = await decode_token(refresh_token)
    if payload is None or payload.get('type') != 'refresh':
        raise ServiceException(
            status.HTTP_400_BAD_REQUEST,
            '无效的刷新令牌',
        )

    # 检查令牌是否过期
    exp = payload.get('exp')
    if exp is not None:
        expires_at = datetime.fromtimestamp(exp, tz=UTC)
        now = datetime.now(UTC)
        if expires_at > now:
            # 计算剩余有效时间并加入黑名单
            expires_delta = expires_at - now
            await add_token_to_blacklist(redis, refresh_token, expires_delta)

    return ResultResponse.success(message='登出成功')
