from datetime import datetime

from app.models.base import BaseCreateDTO
from app.models.security import SecurityUser


async def set_create_field(record: BaseCreateDTO, current_user: SecurityUser):
    now = datetime.now()
    uid = current_user.user.id
    record.created_at = now
    record.updated_at = now
    record.created_by = uid
    record.updated_by = uid
    return record


async def set_update_field(record, current_user: SecurityUser):
    now = datetime.now()
    uid = current_user.user.id
    record.updated_at = now
    record.updated_by = uid
    return record
