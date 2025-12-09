from typing import Annotated

from fastapi import Depends

from app.core.deps import get_current_user
from app.exception import ServiceException
from app.models.response import Pagination, ResponseCode
from app.models.security import SecurityUser
from app.models.user import PassWordChangeDTO, UserCreateDTO, UserUpdateDTO, UserVO
from app.repository.user import UserRepository, get_user_repository
from app.utils.pwd import get_password_hash, verify_password

from .role import RoleService, get_role_service
from .utils import set_create_field, set_update_field


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        role_service: RoleService,
        current_user: SecurityUser,
    ):
        self.user_repository = user_repository
        self.role_service = role_service
        self.current_user = current_user

    async def get_users(self, page_index, page_size) -> Pagination[UserVO]:
        result = await self.user_repository.paginate(page_index, page_size)
        users = result.data
        user_vos = [UserVO.model_validate(user) for user in users]
        result.data = user_vos
        return result

    async def get_user_by_id(self, user_id: int) -> UserVO | None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        return UserVO.model_validate(user)

    async def add_user(self, user_dto: UserCreateDTO) -> UserVO | bool:
        user_dto.password = await get_password_hash(user_dto.password)
        await set_create_field(user_dto, self.current_user)
        new_user = await self.user_repository.create(user_dto)
        return UserVO.model_validate(new_user)

    async def update_user(self, user_dto: UserUpdateDTO) -> bool:
        await set_update_field(user_dto, self.current_user)
        user = await self.user_repository.update(user_dto)
        return bool(user)

    async def delete_user(self, user_id: int) -> bool:
        return await self.user_repository.delete(user_id)

    async def batch_delete_user(self, user_ids: list[int]) -> bool:
        return await self.user_repository.batch_delete(user_ids)

    async def change_password(self, password_change_dto: PassWordChangeDTO) -> bool:
        old_pwd, new_pwd = password_change_dto.old_password, password_change_dto.new_password
        if old_pwd == new_pwd:
            raise ServiceException(code=ResponseCode.ERROR, message='新密码不能与旧密码相同')
        user = await self.user_repository.get_by_id(password_change_dto.id)
        if user is None:
            raise ServiceException(code=ResponseCode.ERROR, message='用户不存在')
        if not await verify_password(old_pwd, user.password):
            raise ServiceException(code=ResponseCode.ERROR, message='旧密码错误')
        user.password = await get_password_hash(new_pwd)
        await self.user_repository.db.flush()
        # TODO: 密码修改后，需要重新登录
        return True

    async def reset_password(self, user_id: int, pwd: str) -> bool:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise ServiceException(code=ResponseCode.ERROR, message='用户不存在')
        user.password = await get_password_hash(pwd)
        await self.user_repository.db.flush()
        # TODO: 密码重置后，需要重新登录
        return True

    async def update_roles(self, user_id: int, role_ids: list[int]) -> bool:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise ServiceException(code=ResponseCode.ERROR, message='用户不存在')
        user.roles = await self.role_service.get_roles_by_ids(role_ids)
        await set_update_field(user, self.current_user)
        await self.user_repository.db.flush()
        return True

    async def get_perms(self, user_id: int) -> list[str]:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise ServiceException(code=ResponseCode.ERROR, message='用户不存在')
        menus = [menu for role in user.roles for menu in role.menus]
        perms = [menu.perms for menu in menus]
        return perms


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    role_service: Annotated[RoleService, Depends(get_role_service)],
    current_user: Annotated[SecurityUser, Depends(get_current_user)],
) -> UserService:
    return UserService(user_repository, role_service, current_user)
