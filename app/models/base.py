from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment='自增id')
    created_by: Mapped[int] = mapped_column(Integer, comment='创建人id')
    updated_by: Mapped[int] = mapped_column(Integer, comment='更新人id')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间'
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment='删除时间')


class BaseUpdateDTO(BaseModel):
    updated_at: datetime | None = Field(default=None)
    updated_by: int | None = Field(default=None)


class BaseCreateDTO(BaseUpdateDTO):
    created_at: datetime | None = Field(default=None)
    created_by: int | None = Field(default=None)
