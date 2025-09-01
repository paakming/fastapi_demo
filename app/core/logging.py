from loguru import logger

logger.remove()

colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# 添加控制台输出（带颜色）
logger.add(
    sink=lambda msg: print(msg, end=''),
    level='DEBUG',
    format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | '
    '<level>{level: <8}</level> | '
    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
    '<level>{message}</level>',
    colorize=True,  # 启用颜色
    backtrace=True,
    diagnose=True,
)

# 添加文件输出（无颜色）
logger.add(
    sink='logs/app.log',
    level='INFO',
    rotation='00:00',
    retention='1 days',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}',
    enqueue=True,
    backtrace=True,
    diagnose=True,
)


__all__ = ['logger']
