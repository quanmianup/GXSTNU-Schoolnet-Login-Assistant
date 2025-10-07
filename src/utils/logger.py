#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志管理模块
提供日志配置、输出和界面显示功能
使用loguru库实现灵活的日志管理系统
"""
import sys
import os
from PySide6.QtCore import QMetaObject, Qt, Q_ARG
from loguru import logger
from src.core.Credentials import credentials
from src.core.TaskScheduler import TaskScheduler

# 日志配置常量
LOG_LEVEL = "DEBUG"  # 日志级别
LOG_ROTATION = "10 MB"  # 每个日志文件最大 10MB
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>"\
    "{line}</cyan> - <level>{message}</level>")

# 全局变量，用于存储界面日志控件和处理器的引用
_ui_log_widget = None  # Qt界面的日志显示控件
_ui_log_handler = None  # 界面日志处理器

class QTextBrowserSink:
    """
    自定义的QTextBrowser日志接收器类
    用于将日志消息显示在Qt界面的QTextBrowser控件中，并支持彩色显示
    
    Attributes:
        text_browser (QTextBrowser): Qt的文本浏览器控件，用于显示日志
        LEVEL_COLORS (dict): 日志级别到HTML颜色的映射字典
    
    Methods:
        __init__: 初始化日志接收器
        write: 向界面控件写入日志消息
        flush: 兼容Python标准io的刷新方法
    
    Example:
        >>> from PySide6.QtWidgets import QTextBrowser
        >>> text_browser = QTextBrowser()
        >>> sink = QTextBrowserSink(text_browser)
        >>> logger.add(sink=sink, level="INFO")
    """
    
    # 日志级别到HTML颜色的映射
    LEVEL_COLORS = {
        'DEBUG': '#6495ED',  # 蓝色
        'INFO': '#008000',   # 绿色
        'WARNING': '#FFA500', # 橙色
        'ERROR': '#FF0000',  # 红色
        'CRITICAL': '#8B0000' # 深红色
    }
    
    def __init__(self, text_browser):
        """
        初始化QTextBrowserSink实例
        
        Args:
            text_browser (QTextBrowser): Qt的文本浏览器控件，用于显示日志
        """
        self.text_browser = text_browser
        self.text_browser.setAcceptRichText(True)  # 确保文本浏览器支持HTML
    
    def write(self, message):
        """
        向界面控件写入日志消息，支持彩色显示
        
        Args:
            message (str): 要显示的日志消息
            
        处理流程：
        1. 检查消息是否包含LEVEL前缀
        2. 解析日志级别和内容
        3. 根据日志级别选择对应的HTML颜色
        4. 在主线程中更新UI控件，确保线程安全
        5. 异常情况下静默忽略错误，避免影响主程序
        """
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
        """
        flush方法(保持与Python标准io兼容)
        此方法在本实现中为空，因为QTextBrowser不需要额外的刷新操作
        """
        pass


def setup_logger(username=None, log_widget=None):
    """
    动态设置日志用户名，用于登录切换场景，同时获取日志文件路径并配置日志。
    兼容开发环境和打包成exe的环境，若开发环境未找到项目根目录则报错。

    Args:
        username (str, optional): 日志文件名使用的用户名，默认为None，此时会从credentials中获取
        log_widget (QTextBrowser, optional): Qt的QTextBrowser控件，用于显示日志

    Raises:
        FileNotFoundError: 开发环境下未找到项目根目录标识文件
        
    功能说明：
    1. 更新UI日志控件引用
    2. 设置用户名和日志文件路径
    3. 重置日志系统，移除所有现有处理器
    4. 添加控制台输出（如果可用）
    5. 添加文件日志输出（带轮转、编码、异步功能）
    6. 添加界面日志处理器（如果提供了日志控件）
    
    Example:
        >>> from PySide6.QtWidgets import QTextBrowser
        >>> text_browser = QTextBrowser()
        >>> setup_logger(username="user123", log_widget=text_browser)
    """
    global _ui_log_widget, _ui_log_handler
    
    # 更新UI日志控件引用
    if log_widget is not None:
        _ui_log_widget = log_widget
    
    # 设置用户名和日志文件路径
    username = username or credentials.get("username", "default")
    log_file_name = f"{username}.log"

    # 日志目录为系统盘根目录下的ScheduledTasks/logs文件夹
    log_dir = TaskScheduler().task_folder / "logs"
    # 创建日志目录，若不存在
    os.makedirs(log_dir, exist_ok=True)
    new_log_path = os.path.join(log_dir, log_file_name)

    # 完全重置日志系统
    logger.remove()  # 移除所有现有的处理器
    
    # 添加控制台输出（彩色）- 仅当stdout可用时
    try:
        if sys.stdout is not None:
            logger.add(
                sink=sys.stdout,
                level=LOG_LEVEL,
                colorize=True,
                format=LOG_FORMAT,
                backtrace=True,
                diagnose=True
            )
    except Exception as e:
        # 在无控制台环境中，控制台输出可能会失败
        pass

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


# 初始化默认logger
try:
    setup_logger()
except FileNotFoundError as e:
    print(f"日志初始化失败: {e}")


# 导出logger实例供其他模块调用
__all__ = ["logger", "setup_logger"]
