from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.menu import Menu

from .base import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    def __init__(self, db: AsyncSession):
        super().__init__(Menu, db)

    async def get_by_ids(self, ids: list[int]) -> list[Menu]:
        result = await self.db.scalars(select(self.clazz).where(self.clazz.id.in_(ids)))
        records = result.all()
        if not records:
            return []
        return list(records)


async def get_menu_repository(db: AsyncSession = Depends(get_db)) -> MenuRepository:
    return MenuRepository(db)
