from typing import Annotated

from fastapi import Depends

from app.core.deps import get_current_user
from app.models.menu import MenuVO
from app.models.security import SecurityUser
from app.repository.menu import MenuRepository, get_menu_repository


class MenuService:
    def __init__(
        self,
        menu_repository: MenuRepository,
        current_user: SecurityUser,
    ):
        self.menu_repository = menu_repository
        self.current_user = current_user

    async def get_menu_by_id(self, menu_id: int):
        menu = await self.menu_repository.get_by_id(menu_id)
        if not menu:
            return None
        return MenuVO.model_validate(menu)

    async def get_menus_by_ids(self, menu_ids: list[int]):
        menus = await self.menu_repository.get_by_ids(menu_ids)
        return menus


async def get_menu_service(
    menu_repository: Annotated[MenuRepository, Depends(get_menu_repository)],
    current_user: Annotated[SecurityUser, Depends(get_current_user)],
) -> MenuService:
    return MenuService(menu_repository, current_user)
