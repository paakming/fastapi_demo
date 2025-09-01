from datetime import UTC, datetime

from fastapi import Depends

from app.exception import ServiceException
from app.models.response import TokenResponse
from app.models.security import SecurityUser
from app.models.user import User, UserVO
from app.repository.user import UserRepository, get_user_repository
from app.utils.jwt import (
    JwtPayload,
    create_two_token,
    decode_token,
)
from app.utils.pwd import verify_password


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends(get_user_repository)):
        self.user_repository = user_repository

    async def authenticate_user(self, username: str, password: str) -> TokenResponse | None:
        user = await self.user_repository.get_one_by_field('username', username)

        if not user:
            return None

        if not await verify_password(password, user.password):
            return None
        payload: JwtPayload = {'subject': user.username}
        access_token, refresh_token = await create_two_token(payload)

        return TokenResponse.success(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='bearer',
        )

    async def get_authenticated_user(self, username: str) -> SecurityUser | None:
        user: User | None = await self.user_repository.get_one_by_field(field_name='username', field_value=username)
        if not user:
            return None

        security_user = SecurityUser(user=UserVO.model_validate(user))
        return security_user

    async def refresh_token(self, refresh_token: str) -> TokenResponse | None:
        payload = await decode_token(refresh_token)
        refresh_token_error = ServiceException(500, '无效的刷新令牌')
        if payload is None or payload.get('type') != 'refresh':
            raise refresh_token_error

        # 检查令牌是否过期
        exp = payload.get('exp')
        if exp is not None and exp < datetime.now(UTC).timestamp():
            raise refresh_token_error

        if not (username := payload.get('subject')):
            raise refresh_token_error
        user = await self.user_repository.get_one_by_field('username', username)
        if user is None:
            raise refresh_token_error
        access, refresh = await create_two_token(payload)
        return TokenResponse.success(
            access_token=access,
            refresh_token=refresh,
            token_type='bearer',
        )


async def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repository)
