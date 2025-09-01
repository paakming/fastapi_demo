from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.role import Role

from .base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self, db: AsyncSession):
        super().__init__(Role, db)

    async def get_by_ids(self, ids: list[int]) -> list[Role]:
        result = await self.db.scalars(select(self.clazz).where(self.clazz.id.in_(ids)))
        records = result.all()
        if not records:
            return []
        return list(records)


async def get_role_repository(db: AsyncSession = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)
