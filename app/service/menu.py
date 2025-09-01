from typing import Annotated

from fastapi import Depends

from app.core.deps import get_current_user
from app.models.menu import MenuUpdateDTO, MenuVO
from app.models.security import SecurityUser
from app.repository.menu import MenuRepository, get_menu_repository

from .utils import set_update_field


class MenuService:
    def __init__(
        self,
        menu_repository: Annotated[MenuRepository, Depends(get_menu_repository)],
        current_user: Annotated[SecurityUser, Depends(get_current_user)],
    ):
        self.menu_repository = menu_repository
        self.current_user = current_user

    async def get_menu_by_id(self, role_id: int):
        menu = await self.menu_repository.get_by_id(role_id)
        if not menu:
            return None
        return MenuVO.model_validate(menu)

    async def get_menus_by_ids(self, role_ids: list[int]):
        menus = await self.menu_repository.get_by_ids(role_ids)
        return menus

    async def update_role(self, role_dto: MenuUpdateDTO) -> bool:
        await set_update_field(role_dto, self.current_user)
        menu = await self.menu_repository.update(role_dto)
        return bool(menu)

    async def delete_role(self, role_id: int) -> bool:
        return await self.menu_repository.delete(role_id)


async def get_menu_service(
    menu_repository: Annotated[MenuRepository, Depends(get_menu_repository)],
    current_user: Annotated[SecurityUser, Depends(get_current_user)],
) -> MenuService:
    return MenuService(menu_repository, current_user)
