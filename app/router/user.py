from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.deps import has_authority
from app.models.response import ResultResponse
from app.models.user import PassWordChangeDTO, UserCreateDTO, UserUpdateDTO, UserVO
from app.service import UserService, get_user_service

router = APIRouter(prefix='/api/v1/user', tags=['user'])

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get(
    '/',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:user:list'))],
    summary='获取用户列表',
    description='获取用户列表',
)
async def get_users(
    user_service: UserServiceDep,
    page_index: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 10,
):
    users = await user_service.get_users(page_index, page_size)
    return ResultResponse.success(data=users)


@router.get(
    '/{user_id}',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:user:read'))],
    summary='获取用户',
    description='获取用户',
)
async def get_user(user_id: int, user_service: UserServiceDep):
    user: UserVO | None = await user_service.get_user_by_id(user_id)
    return ResultResponse.success(data=user) if user else ResultResponse.error(message='用户不存在')


@router.post(
    '/',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:user:create'))],
    summary='添加用户',
    description='添加用户',
)
async def add_user(user: UserCreateDTO, user_service: UserServiceDep):
    new_user = await user_service.add_user(user)
    return ResultResponse.success(data=new_user) if new_user else ResultResponse.error(message='添加用户失败')


@router.put(
    '/',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:user:update'))],
    summary='更新用户',
    description='更新用户信息',
)
async def update_user(user: UserUpdateDTO, user_service: UserServiceDep):
    success = await user_service.update_user(user)
    return ResultResponse.success() if success else ResultResponse.error()


@router.delete(
    '/{user_id}',
    response_model=ResultResponse,
    dependencies=[Depends(has_authority('sys:user:delete'))],
    summary='删除用户',
    description='逻辑删除用户',
)
async def delete_user(user_id: int, user_service: UserServiceDep):
    success = await user_service.delete_user(user_id)
    return ResultResponse.success() if success else ResultResponse.error()


@router.post(
    '/batch_delete',
    response_model=ResultResponse,
    summary='批量删除用户',
    description='批量逻辑删除用户',
    dependencies=[Depends(has_authority('sys:user:batch_delete'))],
)
async def batch_delete_user(user_ids: list[int], user_service: UserServiceDep):
    success = await user_service.batch_delete_user(user_ids)
    return ResultResponse.success() if success else ResultResponse.error()


@router.post(
    '/password/change',
    response_model=ResultResponse,
    summary='修改密码',
    description='修改密码',
    dependencies=[Depends(has_authority('sys:user:pwd_change'))],
)
async def change_password(password_change_dto: PassWordChangeDTO, user_service: UserServiceDep):
    success = await user_service.change_password(password_change_dto)
    return ResultResponse.success() if success else ResultResponse.error()


@router.post(
    '/password/reset',
    response_model=ResultResponse,
    summary='重置密码',
    description='重置密码',
    dependencies=[Depends(has_authority('sys:user:pwd_reset'))],
)
async def reset_password(user_id: int, pwd: str, user_service: UserServiceDep):
    success = await user_service.reset_password(user_id, pwd)
    return ResultResponse.success() if success else ResultResponse.error()


@router.post(
    '/roles/update',
    response_model=ResultResponse,
    summary='分配角色',
    description='为用户分配角色',
    dependencies=[Depends(has_authority('sys:user:role_update'))],
)
async def update_roles(user_id: int, role_ids: list[int], user_service: UserServiceDep):
    success = await user_service.update_roles(user_id, role_ids)
    return ResultResponse.success() if success else ResultResponse.error()
