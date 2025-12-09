from datetime import datetime, timedelta
from typing import Any, TypedDict

import jwt
from jwt import PyJWTError

from app.core.config import settings

# JWT配置
SECRET_KEY = settings.SECRET_KEY if hasattr(settings, 'SECRET_KEY') else 'your-secret-key'
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES


class JwtPayload(TypedDict, total=False):
    subject: str
    exp: Any
    type: str


async def create_access_token(data: JwtPayload, expires_delta: timedelta | None = None) -> str:
    """
    创建访问令牌

    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量

    Returns:
        编码后的JWT访问令牌
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire, 'type': 'access'})
    encoded_jwt: str = jwt.encode(dict(to_encode), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: JwtPayload, expires_delta: timedelta | None = None) -> str:
    """
    创建刷新令牌

    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量

    Returns:
        编码后的JWT刷新令牌
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire, 'type': 'refresh'})
    encoded_jwt: str = jwt.encode(dict(to_encode), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_two_token(data: JwtPayload) -> tuple[str, str]:
    """
    创建访问令牌和刷新令牌

    Args:
        data: 要编码的数据

    Returns:
        访问令牌和刷新令牌
    """
    access_token, refresh_token = await create_access_token(data), await create_refresh_token(data)
    return access_token, refresh_token


async def decode_token(token: str) -> JwtPayload | None:
    """
    解码JWT令牌

    Args:
        token: JWT令牌

    Returns:
        解码后的数据，如果解码失败返回None
    """
    try:
        payload: JwtPayload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        return None


async def add_token_to_blacklist(redis, token: str, expires_delta: timedelta) -> bool:
    """
    将令牌添加到黑名单中

    Args:
        redis: Redis客户端
        token: 要加入黑名单的令牌
        expires_delta: 过期时间

    Returns:
        添加成功返回True，否则返回False
    """
    try:
        # 使用JWT的jti( JWT ID)作为键，但如果没有jti，则使用令牌本身
        payload = await decode_token(token)
        if payload is None:
            return False

        jti = payload.get('jti')
        if jti is None:
            # 如果没有jti，使用令牌的前32个字符作为标识符
            jti = token[:32] if len(token) > 32 else token

        # 将令牌添加到Redis黑名单中
        await redis.setex(f'blacklist:{jti}', int(expires_delta.total_seconds()), 'true')
        return True
    except Exception:
        return False


async def is_token_blacklisted(redis, token: str) -> bool:
    """
    检查令牌是否在黑名单中

    Args:
        redis: Redis客户端
        token: 要检查的令牌

    Returns:
        如果令牌在黑名单中返回True，否则返回False
    """
    try:
        payload = await decode_token(token)
        if payload is None:
            return True  # 无法解码的令牌视为已列入黑名单

        jti = payload.get('jti')
        if jti is None:
            jti = token[:32] if len(token) > 32 else token

        # 检查令牌是否在Redis黑名单中
        result = await redis.get(f'blacklist:{jti}')
        return result is not None
    except Exception:
        return True  # 出现异常时保守地认为令牌已列入黑名单
