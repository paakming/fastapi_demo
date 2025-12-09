from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.menu import Menu
    from app.models.user import User

from sqlalchemy import Boolean, Column, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, primary_key=True),
    Column('role_id', Integer, primary_key=True),
)

role_menu = Table(
    'role_menu',
    Base.metadata,
    Column('role_id', Integer, primary_key=True),
    Column('menu_id', Integer, primary_key=True),
)


class Role(Base):
    __tablename__ = 'role'

    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False, comment='角色名称')
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False, comment='角色编码')
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, comment='是否管理员')
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False, comment='是否为超级管理员')

    menus: Mapped[list[Menu]] = relationship(
        'Menu',
        secondary=role_menu,
        back_populates='roles',
        primaryjoin='Role.id == role_menu.c.role_id',
        secondaryjoin='Menu.id == role_menu.c.menu_id',
        lazy='selectin',
    )

    users: Mapped[list[User]] = relationship(
        'User',
        secondary=user_role,
        back_populates='roles',
        primaryjoin='Role.id == user_role.c.role_id',
        secondaryjoin='User.id == user_role.c.user_id',
        lazy='selectin',
    )

    def __repr__(self) -> str:
        return f'Role(id={self.id}, name={self.name}, code={self.code})'
