from collections.abc import AsyncGenerator
from datetime import datetime

from loguru import logger
from sqlalchemy import insert, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.base import Base
from app.models.user import SUPERUSER_ID, SUPERUSER_NAME, SUPERUSER_PASSWORD, User
from app.utils.pwd import get_password_hash

# engine = create_async_engine(str(settings.DATABASE_URL))
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # 30分钟回收连接
    pool_pre_ping=True,  # 重要：连接前健康检查
)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话的依赖项
    """
    async with AsyncSessionLocal() as current_db:
        try:
            yield current_db
            await current_db.commit()
        except Exception:
            logger.exception('数据库会话提交失败')
            await current_db.rollback()
            raise
        finally:
            await current_db.close()


async def create_superuser():
    async with AsyncSessionLocal() as db:
        user = await db.scalar(select(User).where(User.id == SUPERUSER_ID))

        if not user:
            hashed_password = await get_password_hash(SUPERUSER_PASSWORD)
            await db.execute(
                insert(User).values(
                    id=SUPERUSER_ID,
                    username=SUPERUSER_NAME,
                    password=hashed_password,
                    email='admin@admin.com',
                    birthday=datetime.now(),
                    created_by=SUPERUSER_ID,
                    updated_by=SUPERUSER_ID,
                )
            )
            await db.execute(text('SELECT setval(\'user_id_seq\', (SELECT MAX(id) FROM "user"));'))
            await db.commit()
            logger.info('超级用户创建成功')
        else:
            logger.info('超级用户已存在')


async def init_create_table():
    """
    初始化数据库表
    """
    logger.info('初始化数据库连接...')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info('数据库连接成功')
    await create_superuser()

    # 初始化RBAC数据
    # async with AsyncSessionLocal() as db:
    #     await init_rbac_data(db)
