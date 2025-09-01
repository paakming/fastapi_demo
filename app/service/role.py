from typing import Annotated

from fastapi import Depends

from app.core.deps import get_current_user
from app.models.role import RoleCreateDTO, RoleUpdateDTO, RoleVO
from app.models.security import SecurityUser
from app.repository.role import RoleRepository, get_role_repository
from app.service.menu import MenuService, get_menu_service

from .utils import set_create_field, set_update_field


class RoleService:
    def __init__(
        self,
        role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
        menu_service: Annotated[MenuService, Depends(get_menu_service)],
        current_user: Annotated[SecurityUser, Depends(get_current_user)],
    ):
        self.role_repository = role_repository
        self.current_user = current_user

    async def get_role_by_id(self, role_id: int):
        role = await self.role_repository.get_by_id(role_id)
        if not role:
            return None
        return RoleVO.model_validate(role)

    async def get_roles_by_ids(self, role_ids: list[int]):
        roles = await self.role_repository.get_by_ids(role_ids)
        return roles

    async def add_role(self, role_dto: RoleCreateDTO) -> RoleVO | bool:
        await set_create_field(role_dto, self.current_user)
        new_role = await self.role_repository.create(role_dto)
        return RoleVO.model_validate(new_role)

    async def update_role(self, role_dto: RoleUpdateDTO) -> bool:
        await set_update_field(role_dto, self.current_user)
        role = await self.role_repository.update(role_dto)
        return bool(role)

    async def delete_role(self, role_id: int) -> bool:
        return await self.role_repository.delete(role_id)

    async def update_role_menus(self, role_id: int, menu_ids: list[int]) -> bool:
        role = await self.role_repository.get_by_id(role_id)
        if not role:
            return False
        role.menus = []
        return False


async def get_role_service(
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
    menu_service: Annotated[MenuService, Depends(get_menu_service)],
    current_user: Annotated[SecurityUser, Depends(get_current_user)],
) -> RoleService:
    return RoleService(role_repository, menu_service, current_user)
