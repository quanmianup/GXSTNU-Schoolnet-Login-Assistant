import os
import sys
from pathlib import Path

from loguru import logger
from config.credentials import credentials

# 日志配置
LOG_FILE_NAME = f"{credentials.get('USERNAME', 'default')}.log"  # 默认按用户名命名
LOG_LEVEL = "DEBUG"
LOG_ROTATION = "10 MB"  # 每个日志文件最大 10MB
# LOG_RETENTION = "7 days"        # 保留最近 7 天的日志
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>"
    "{line}</cyan> - <level>{message}</level>")


def setup_logger(username=None):
    """
    动态设置日志用户名，用于登录切换场景，同时获取日志文件路径并配置日志。
    兼容开发环境和打包成 exe 的环境，若未找到项目根目录则报错。

    Args:
        username (str, optional): 日志文件名使用的用户名，默认为 None。

    Raises:
        FileNotFoundError: 开发环境下未找到项目根目录标识文件。
    """
    username = username or credentials.get("username", "default")
    log_file_name = f"{username}.log"

    if getattr(sys, 'frozen', False):
        # 打包成 exe 的环境，将日志目录放到 self.task_folder 对应的目录下
        from src.utils.task_manager import TaskManager
        base_path = TaskManager().task_folder
        log_dir = base_path / "logs"
    else:
        # 开发环境，获取项目根目录
        current_path = os.path.abspath(__file__)
        base_path = os.path.dirname(current_path)

        while True:
            # 检查当前目录是否有 requirements.txt
            if os.path.isfile(os.path.join(base_path, 'requirements.txt')):
                break
            parent_path = os.path.dirname(base_path)
            if parent_path == base_path:
                # 到达文件系统根目录，仍未找到项目根目录标识，抛出错误
                raise FileNotFoundError("在开发环境下未找到项目根目录标识文件 'requirements.txt'")
            base_path = parent_path

        log_dir = os.path.join(base_path, "logs")

    # 创建日志目录，若不存在
    os.makedirs(log_dir, exist_ok=True)
    new_log_path = os.path.join(log_dir, log_file_name)

    # 清除已有处理器
    logger.configure(handlers=[])

    # 添加控制台输出（彩色）
    logger.add(
        sink=lambda msg: print(msg, end=''),
        level=LOG_LEVEL,
        colorize=True,
        format=LOG_FORMAT,
        backtrace=True,
        diagnose=True
    )

    # 添加文件日志输出（带轮转、编码、异步）
    logger.add(
        sink=new_log_path,
        rotation=LOG_ROTATION,
        # retention=LOG_RETENTION,
        level=LOG_LEVEL,
        encoding="utf-8",
        enqueue=True,  # 支持异步写入
        format=LOG_FORMAT
    )


# 初始化默认 logger
try:
    setup_logger()
except FileNotFoundError as e:
    print(f"日志初始化失败: {e}")

# 导出 logger 实例供其他模块调用
__all__ = ["logger", "setup_logger"]
