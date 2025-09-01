from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.deps import has_authority
from app.models.response import ResultResponse
from app.models.role import RoleCreateDTO, RoleUpdateDTO, RoleVO
from app.service import RoleService, get_role_service

router = APIRouter(prefix='/api/v1/role', tags=['role'])


RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]


@router.get(
    '/{role_id}',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:role:read'))],
    summary='获取角色',
    description='获取角色',
)
async def get_role(role_id: int, role_service: RoleServiceDep):
    role: RoleVO | None = await role_service.get_role_by_id(role_id)
    if role:
        return ResultResponse.success(data=role)
    return ResultResponse.error(message='角色不存在')


@router.post(
    '/',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:role:create'))],
    summary='添加角色',
    description='添加角色',
)
async def add_role(role: RoleCreateDTO, role_service: RoleServiceDep):
    new_role = await role_service.add_role(role)
    if new_role:
        return ResultResponse.success(data=new_role)
    return ResultResponse.error(message='添加角色失败')


@router.put(
    '/',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:role:update'))],
    summary='更新角色',
    description='更新角色信息',
)
async def update_role(role: RoleUpdateDTO, role_service: RoleServiceDep):
    success = await role_service.update_role(role)
    if success:
        return ResultResponse.success()
    return ResultResponse.error()


@router.delete(
    '/{role_id}',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:role:delete'))],
    summary='删除角色',
    description='删除角色',
)
async def delete_role(role_id: int, role_service: RoleServiceDep):
    success = await role_service.delete_role(role_id)
    if success:
        return ResultResponse.success()
    return ResultResponse.error()


@router.post(
    '/menus/update',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:role:update'))],
    summary='更新角色菜单权限',
    description='更新角色菜单权限',
)
async def update_role_menus(role_id: int, menu_ids: list[int], role_service: RoleServiceDep):
    success = await role_service.update_role_menus(role_id, menu_ids)
    return ResultResponse.success() if success else ResultResponse.error()
