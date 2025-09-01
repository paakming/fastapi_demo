from __future__ import annotations

from typing import TYPE_CHECKING

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.role import Role

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Menu(Base):
    __tablename__ = 'menu'

    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='菜单名称')
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False, comment='菜单编码')
    path: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='路由地址')
    component: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='组件名称')
    perms: Mapped[str | None] = mapped_column(String(200), nullable=True, comment='权限标识')
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True, comment='图标')
    parent_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True, comment='父级菜单ID')
    sequence: Mapped[int] = mapped_column(Integer, default=0, comment='序列')
    is_visible: Mapped[int] = mapped_column(Integer, default=0, comment='是否可见, 0-隐藏 1-显示')

    roles: Mapped[list[Role]] = relationship(
        'Role',
        secondary='role_menu',
        back_populates='menus',
        primaryjoin='Menu.id == role_menu.c.menu_id',
        secondaryjoin='Role.id == role_menu.c.role_id',
        lazy='selectin',
    )
