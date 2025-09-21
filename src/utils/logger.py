import os
import sys
import time
import os
from pathlib import Path

from PySide6.QtCore import QMetaObject, Qt, Q_ARG
from PySide6.QtGui import QTextCursor
from loguru import logger
from config.credentials import credentials
from src.core.TaskScheduler import TaskScheduler

# 日志配置
LOG_LEVEL = "DEBUG"
LOG_ROTATION = "10 MB"  # 每个日志文件最大 10MB
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>"
    "{line}</cyan> - <level>{message}</level>")

# 用于存储界面日志控件和处理器的引用
_ui_log_widget = None
_ui_log_handler = None

# 自定义的QTextBrowser日志接收器类
class QTextBrowserSink:
    # 日志级别到HTML颜色的映射
    LEVEL_COLORS = {
        'DEBUG': '#6495ED',  # 蓝色
        'INFO': '#008000',   # 绿色
        'WARNING': '#FFA500', # 橙色
        'ERROR': '#FF0000',  # 红色
        'CRITICAL': '#8B0000' # 深红色
    }
    
    def __init__(self, text_browser):
        self.text_browser = text_browser
        self.text_browser.setAcceptRichText(True)  # 确保文本浏览器支持HTML
    
    def write(self, message):
        """向界面控件写入日志消息，支持彩色显示"""
        try:
            # 检查消息是否包含LEVEL前缀
            if message.startswith('LEVEL:'):
                # 解析级别和原始消息
                parts = message.split('|', 1)
                if len(parts) == 2:
                    level_part = parts[0].replace('LEVEL:', '').strip()
                    log_content = parts[1].strip()
                    
                    # 获取当前级别的颜色并创建HTML格式的消息
                    log_color = self.LEVEL_COLORS.get(level_part, '#000000')  # 默认黑色
                    html_message = f'<span style="color: {log_color};">{log_content}</span>'
                else:
                    html_message = message
            else:
                html_message = message
            
            # 确保在主线程更新UI
            QMetaObject.invokeMethod(
                self.text_browser,
                "append",
                Qt.QueuedConnection,
                Q_ARG(str, html_message)
            )
        except Exception:
            # 如果界面更新失败，静默忽略
            pass
    
    def flush(self):
        """flush方法(保持与Python标准io兼容)"""
        pass


def setup_logger(username=None, log_widget=None):
    """
    动态设置日志用户名，用于登录切换场景，同时获取日志文件路径并配置日志。
    兼容开发环境和打包成 exe 的环境，若开发环境未找到项目根目录则报错。

    Args:
        username (str, optional): 日志文件名使用的用户名，默认为 None。
        log_widget (QTextBrowser, optional): Qt的QTextBrowser控件，用于显示日志。

    Raises:
        FileNotFoundError: 开发环境下未找到项目根目录标识文件。
    """
    global _ui_log_widget, _ui_log_handler
    
    # 更新UI日志控件引用
    if log_widget is not None:
        _ui_log_widget = log_widget
    
    # 设置用户名和日志文件路径
    username = username or credentials.get("username", "default")
    log_file_name = f"{username}.log"

    # 确定日志目录
    if getattr(sys, 'frozen', False):
        # 打包成 exe 的环境
        log_dir = TaskScheduler().task_folder / "logs"
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

    # 完全重置日志系统
    logger.remove()  # 移除所有现有的处理器
    
    # 添加控制台输出（彩色）
    logger.add(
        sink=sys.stdout,
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
        level=LOG_LEVEL,
        encoding="utf-8",
        enqueue=True,  # 支持异步写入
        format=LOG_FORMAT
    )

    # 重新添加UI日志处理器（如果之前存在或提供了新的控件）
    if _ui_log_widget is not None:
        # 创建专门的UI日志格式化器（带级别信息用于彩色显示）
        def ui_log_formatter(record):
            """自定义UI日志格式化器，包含级别信息"""
            log_time = record["time"].strftime("%Y-%m-%d %H:%M:%S")
            log_level = record["level"].name
            log_content = record["message"]
            # 保存原始消息和级别信息，供write方法使用
            return f"LEVEL:{log_level}|[{log_time}] {log_content}\n"
        
        # 创建QTextBrowserSink实例并添加界面日志接收器
        ui_sink = QTextBrowserSink(_ui_log_widget)
        _ui_log_handler = logger.add(
            sink=ui_sink,
            level=LOG_LEVEL,
            format=ui_log_formatter,
            enqueue=True,  # 支持异步写入
            backtrace=False,  # 不显示回溯信息，保持界面日志简洁
            diagnose=False  # 不显示诊断信息
        )
        
        # 如果是首次设置UI日志或更换了日志控件，发送初始化成功日志
        if log_widget is not None:
            logger.info("界面日志系统已初始化成功")
    else:
        _ui_log_handler = None


# 初始化默认 logger
try:
    print("初始化默认日志系统...")
    setup_logger()
except FileNotFoundError as e:
    print(f"日志初始化失败: {e}")


# 导出 logger 实例供其他模块调用
__all__ = ["logger", "setup_logger"]
