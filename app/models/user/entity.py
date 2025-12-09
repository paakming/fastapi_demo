from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.role import Role

from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

GENDER_MAPPING = {
    '0': '其他',
    '1': '女',
    '2': '男',
}


class User(Base):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, comment='用户名', index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, comment='邮箱')
    password: Mapped[str] = mapped_column(String, nullable=False, comment='密码')
    birthday: Mapped[date | None] = mapped_column(Date, nullable=True, comment='生日')
    gender: Mapped[str | None] = mapped_column(String, nullable=True, comment='性别, 0:其他, 1:男, 2:女')
    phone: Mapped[str | None] = mapped_column(String, nullable=True, comment='手机号')
    nickname: Mapped[str | None] = mapped_column(String, nullable=True, comment='昵称')
    avatar: Mapped[str | None] = mapped_column(String, nullable=True, comment='头像')

    roles: Mapped[list[Role]] = relationship(
        'Role',
        secondary='user_role',
        back_populates='users',
        primaryjoin='User.id == user_role.c.user_id',
        secondaryjoin='Role.id == user_role.c.role_id',
        lazy='selectin',
    )

    def __repr__(self) -> str:
        return f'User(id={self.id}, username={self.username}'
