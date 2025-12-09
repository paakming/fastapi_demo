from datetime import datetime
from typing import Any

from pydantic import BaseModel
from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.models.response import Pagination


class BaseRepository[Clazz: Base]:
    def __init__(self, clazz: type[Clazz], db: AsyncSession):
        self.db = db
        self.clazz = clazz

    async def get_by_id(self, id: int) -> Clazz | None:
        """
        根据ID获取实体

        Args:
            id: 实体ID

        Returns:
            实体对象或None
        """
        # 检查模型是否有deleted_at字段
        has_deleted_at = hasattr(self.clazz, 'deleted_at')

        if has_deleted_at:
            result = await self.db.scalar(
                select(self.clazz).where((self.clazz.id == id) & (self.clazz.deleted_at.is_(None)))
            )
        else:
            result = await self.db.scalar(select(self.clazz).where(self.clazz.id == id))
        return result

    async def create(self, create_dto: BaseModel) -> Clazz:
        instance = self.clazz(**create_dto.model_dump())
        self.db.add(instance)
        await self.db.flush()
        return instance

    async def create_with_insert(self, create_dto: BaseModel) -> Clazz:
        """
        使用insert语句创建实体

        Args:
            create_dto: 创建数据传输对象

        Returns:
            创建的实体对象
        """
        # 获取模型数据
        data = create_dto.model_dump()

        # 执行insert语句
        stmt = insert(self.clazz).values(**data)
        result = await self.db.execute(stmt)

        # 获取插入的记录ID
        inserted_id = result.inserted_primary_key[0]  # type: ignore

        # 查询并返回插入的实体
        instance = await self.get_by_id(inserted_id)
        if instance is None:
            # 这种情况理论上不会发生，但为了类型检查需要处理
            raise Exception('Failed to retrieve inserted entity')
        return instance

    async def update(self, update_dto: BaseModel) -> Clazz | None:
        """
        更新实体

        Args:
            update_dto: 更新数据传输对象

        Returns:
            更新后的实体对象或None
        """
        dto = update_dto.model_dump(exclude_unset=True)
        id = dto.get('id')
        if id is None:
            return None
        instance = await self.get_by_id(id)
        dto.pop('id', None)
        if instance:
            for key, value in dto.items():
                # 只有当值不是None时才更新字段
                if value is not None:
                    setattr(instance, key, value)
        return instance

    async def delete(self, id: int) -> bool:
        """
        软删除实体（设置deleted_at字段）, 硬删除使用 hard_delete
        Args:
            id: 实体ID

        Returns:
            删除是否成功
        """
        instance = await self.get_by_id(id)
        if instance and hasattr(instance, 'deleted_at'):
            setattr(instance, 'deleted_at', datetime.now())
            return True
        return False

    async def hard_delete(self, id: int) -> bool:
        """
        硬删除实体（从数据库中永久删除）

        Args:
            id: 实体ID

        Returns:
            删除是否成功
        """
        instance = await self.get_by_id(id)
        if instance:
            await self.db.delete(instance)
            return True
        return False

    async def get_one_by_field(self, field_name: str, field_value: Any) -> Clazz | None:
        """
        根据字段名和字段值获取实体

        Args:
            field_name: 字段名
            field_value: 字段值

        Returns:
            实体对象或None
        """
        # 检查模型是否有deleted_at字段
        has_deleted_at = hasattr(self.clazz, 'deleted_at')

        if has_deleted_at:
            result = await self.db.scalar(
                select(self.clazz).where(
                    (getattr(self.clazz, field_name) == field_value) & (self.clazz.deleted_at.is_(None))
                )
            )
        else:
            result = await self.db.scalar(select(self.clazz).where(getattr(self.clazz, field_name) == field_value))
        return result

    async def get_all_by_field(self, field_name: str, field_value: Any) -> list[Clazz]:
        """
        根据字段名和字段值获取所有匹配的实体列表

        Args:
            field_name: 字段名
            field_value: 字段值

        Returns:
            匹配的实体对象列表
        """
        has_deleted_at = hasattr(self.clazz, 'deleted_at')

        if has_deleted_at:
            records = await self.db.scalars(
                select(self.clazz).where(
                    (getattr(self.clazz, field_name) == field_value) & (self.clazz.deleted_at.is_(None))
                )
            )
        else:
            records = await self.db.scalars(select(self.clazz).where(getattr(self.clazz, field_name) == field_value))
        return list(records.all())

    async def paginate(self, page_index: int = 1, page_size: int = 10) -> Pagination[Clazz]:
        """
        分页查询

        Args:
            page_index: 页码（从1开始）
            page_size: 每页大小

        Returns:
            包含数据和分页信息的字典
        """
        offset = (page_index - 1) * page_size

        # 检查模型是否有deleted_at字段
        has_deleted_at = hasattr(self.clazz, 'deleted_at')

        query = select(self.clazz).where(self.clazz.deleted_at.is_(None)) if has_deleted_at else select(self.clazz)

        # 获取总数量
        total_query = select(func.count()).select_from(self.clazz)
        total = await self.db.scalar(total_query) or 0

        # 获取数据
        result = await self.db.scalars(query.offset(offset).limit(page_size))
        data = list(result.all())
        return Pagination(
            data=data,
            total=total,
            page=page_index,
            size=page_size,
            pages=(total + page_size - 1) // page_size if page_size > 0 else 0,
        )

    async def batch_delete(self, ids: list[int]) -> bool:
        """
        批量删除实体

        Args:
            ids: 需要删除的实体ID列表

        Returns:
            删除操作是否成功执行
        """
        if not ids:
            return False

        has_deleted_at = hasattr(self.clazz, 'deleted_at')
        if has_deleted_at:
            result = await self.db.execute(
                update(self.clazz).where(self.clazz.id.in_(ids)).values(deleted_at=datetime.now())
            )
            await self.db.flush()
            return result.rowcount > 0
        else:
            # 对于没有deleted_at字段的模型，执行硬删除
            instances = await self.db.scalars(select(self.clazz).where(self.clazz.id.in_(ids)))
            for instance in instances:
                await self.db.delete(instance)
            await self.db.flush()
            return True
