from ..base import BaseCreateDTO, BaseUpdateDTO


class RoleCreateDTO(BaseCreateDTO):
    name: str
    code: str
    is_admin: bool = False
    is_super_admin: bool = False


class RoleUpdateDTO(BaseUpdateDTO):
    id: int
    name: str | None = None
    code: str | None = None
    is_admin: bool | None
