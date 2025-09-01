from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator


class UserVO(BaseModel):
    id: int
    username: str
    email: str | None = None
    birthday: str | None = None
    age: int | None = None
    nickname: str | None = None
    phone: str | None = None
    gender: str | None = None
    avatar: str | None = None
    roles: list[dict[str, str | bool]] | None = []

    @field_validator('birthday', mode='before')
    @classmethod
    def format_birthday(cls, v):
        """
        特殊处理birthday字段，将datetime对象转换为字符串格式
        """
        if v is None:
            return None
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d')
        return str(v)

    @model_validator(mode='after')
    def calculate_age(self) -> UserVO:
        """
        根据生日计算年龄
        """
        if self.birthday:
            try:
                birth_date = datetime.strptime(self.birthday, '%Y-%m-%d')
                today = datetime.today()
                self.age = (
                    today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                )
            except ValueError:
                # 如果日期格式不正确，则年龄为None
                self.age = None
        return self

    @field_validator('roles', mode='before')
    @classmethod
    def validate_roles(cls, v):
        if v is None:
            return []
        return [
            {'name': role.name, 'code': role.code, 'is_admin': role.is_admin, 'is_super_admin': role.is_super_admin}
            for role in v
        ]

    class Config:
        from_attributes = True
