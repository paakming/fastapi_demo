import sys

from loguru import logger

from app.core.config import settings

is_dev = settings.APP_ENV.lower().startswith('dev')

logger.remove()

colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# 添加控制台输出

logger.add(
    sink=sys.stdout,
    level='DEBUG',
    format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | '
    '<level>{level: <8}</level> | '
    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
    '<level>{message}</level>',
    colorize=True,  # 启用颜色
    backtrace=is_dev,
    diagnose=is_dev,
    enqueue=True,
)

# 添加文件输出
logger.add(
    sink='logs/app_{time:YYYY-MM-DD}.log',  # 日志文件名包含日期
    level='INFO',
    rotation='00:00',
    retention='7 days',  # 保留7天日志 30 days/1 month/1 year
    compression='zip',  # 压缩旧日志
    format='{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}',
    enqueue=True,
    backtrace=is_dev,
    diagnose=is_dev,
    delay=True,
)


__all__ = ['logger']
