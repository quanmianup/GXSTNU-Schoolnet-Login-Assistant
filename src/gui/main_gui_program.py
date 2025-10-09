"""
主界面程序，负责创建和管理 GUI 界面。

此模块实现了校园网登录助手的主界面，提供了以下功能：
- 用户登录和下线操作
- 网络状态实时监控
- 计划任务管理（创建、查询、删除）
- 生成一键登录可执行文件
- 密码保护功能

依赖项:
- PySide6: 用于构建GUI界面
- AsyncTaskExecutor: 处理异步任务
- NetworkManager: 管理网络连接
- TaskScheduler: 管理Windows计划任务
- Credentials: 处理凭证存储
- logger: 日志记录

使用示例:
```python
from src.gui.main_gui_program import run

# 启动主程序
run()
```
"""
import os
import shutil
import subprocess
import sys
import webbrowser
import tomllib
import requests
from PySide6.QtCore import Qt, QPoint, QTime, QEvent, QTimer, QMetaObject, Q_ARG
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QDialog, QDialogButtonBox

from src.core.AsyncTaskExecutor import AsyncTaskExecutor
from src.core.NetworkManager import networkmanager
from src.gui.main_ui import Ui_MainWindow
from src.gui.PswdInput_ui import Ui_Dialog
from src.utils.logger import logger, setup_logger
from src.core.TaskScheduler import TaskScheduler
from src.core.Credentials import credentials


class MainWindow(QMainWindow):
    """
    主窗口类，负责创建和管理 GUI 界面。
    
    此类实现了校园网登录助手的主界面功能，包括登录/下线操作、网络状态监控、
    计划任务管理和一键登录文件生成等功能。
    
    属性:
        ui: UI界面实例
        task_manager: 任务调度管理器实例
        task_executor: 异步任务执行器实例
        keep_alive_timer: 网络保活定时器
        dragging: 窗口拖动状态标志
        offset: 窗口拖动偏移量
    """

    def __init__(self):
        """
        初始化主窗口，设置UI界面和相关组件。
        
        功能:
        - 加载UI界面
        - 设置无边框窗口和透明背景
        - 初始化凭证管理器和任务管理器
        - 设置网络保活定时器
        - 配置日志系统
        - 连接UI组件信号和槽函数
        - 设置窗口拖动功能
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.lineEdit_username.setText(credentials.get('username', ''))
        self.ui.lineEdit_password.setText(credentials.get('password', ''))
        self.ui.label_black_message.setText("")
        
        # 从配置中加载启动时检查更新的状态
        check_update_status = credentials.get('UPDATE_ON_START', True)
        self.ui.checkBox_update.setChecked(check_update_status)
        # 连接checkBox_update的状态变化信号，实现持久化保存
        self.ui.checkBox_update.stateChanged.connect(
            lambda :self._save_check_update_state())
        
        # 设置关于页面的内容
        self.set_about_text()

        self.task_manager = TaskScheduler()
        self.task_executor = AsyncTaskExecutor()
        self.task_executor.finished.connect(self.handle_general_finished)
        
        # 初始化保活功能相关变量
        self.keep_alive_timer = QTimer(self)
        self.keep_alive_timer.setInterval(5000)  # 5秒
        self.keep_alive_timer.timeout.connect(self._check_network_status_and_update_tabwiget)
        self.keep_alive_timer.start()
        
        # 设置界面日志输出，连接到右侧的日志控件
        setup_logger(log_widget=self.ui.textBrowser_log)
        
        # 设置日志控件的右键清空日志菜单
        self.setup_log_context_menu()

        self._init_ui_connect_()

        # 初始化拖动相关变量
        self.dragging = False
        self.offset = QPoint()

        # 为标题栏添加事件过滤器
        self.ui.frame_title.installEventFilter(self)
        
        
        # 检查是否在启动时检查更新
        if check_update_status:
            self.check_for_updates()
    
    def _init_ui_connect_(self):
        """
        初始化 UI 组件的事件连接。
        
        功能:
        - 连接按钮点击事件到相应的处理函数
        - 初始化任务表格的列标题和对齐方式
        """
        self.ui.select_file_btn.clicked.connect(self.select_file)
        self.ui.create_btn.clicked.connect(self.create_task)
        self.ui.query_btn.clicked.connect(
            lambda: (self.query_tasks(), 
            QMessageBox.information(self, "提示", "查询任务成功")))
        self.ui.delete_btn.clicked.connect(self.delete_task)
        self.ui.pushButton_generate.clicked.connect(self.create_exe)
        self.ui.task_table.setColumnCount(4)
        self.ui.task_table.horizontalHeader().setVisible(True)
        self.ui.task_table.setHorizontalHeaderLabels(
            ["任务名称", "文件路径", "状态", "下次运行时间"])
        self.ui.task_table.horizontalHeader().setDefaultAlignment(
            Qt.AlignLeft | Qt.AlignVCenter)

        self.ui.pushButton_login.clicked.connect(self.login)
        self.ui.pushButton_dislogin.clicked.connect(self.dislogin)
        self.ui.pushButton_tab_main.clicked.connect(lambda: self.ui.stackedWidget_tab.setCurrentIndex(0))
        self.ui.pushButton_tab_manege.clicked.connect(
            lambda: (
                self.ui.stackedWidget_tab.setCurrentIndex(1),
                self.ui.time_edit.setTime(QTime.currentTime()),
                self.query_tasks()
        ))
        self.ui.pushButton_tab_other.clicked.connect(lambda: self.ui.stackedWidget_tab.setCurrentIndex(2))
        self.ui.pushButton_help.clicked.connect(lambda: self.ui.stackedWidget_other.setCurrentIndex(0))
        self.ui.pushButton_update.clicked.connect(
            lambda: (
            self.ui.stackedWidget_other.setCurrentIndex(1),
            self.check_for_updates(from_button=True),
        ))
        self.ui.pushButton_disclaimer.clicked.connect(lambda: self.ui.stackedWidget_other.setCurrentIndex(2))
        self.ui.pushButton_about.clicked.connect(lambda: self.ui.stackedWidget_other.setCurrentIndex(3))

        # 连接保活按钮信号
        self.ui.pushButton_keeplogin.clicked.connect(self._toggle_keep_network_online)
        
    def eventFilter(self, obj, event):
        """
        事件过滤器，处理标题栏的鼠标事件以实现窗口拖动。
        
        参数:
            obj: 事件源对象
            event: 事件对象
        
        返回:
            bool: 事件是否被处理
        """
        if obj == self.ui.frame_title:
            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.dragging = True
                    self.offset = event.globalPos() - self.pos()
            elif event.type() == QEvent.MouseMove:
                if self.dragging:
                    self.move(event.globalPos() - self.offset)
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self.dragging = False
        return super().eventFilter(obj, event)
    
    def check_for_updates(self, from_button=False):
        """
        检查应用程序是否有更新。
        
        参数:
            from_button (bool): 是否从按钮点击触发的检查更新
        
        功能:
        - 从Gitee仓库获取最新版本信息
        - 与当前版本进行比较
        - 根据比较结果显示相应的提示信息
        """
        try:
            logger.info("正在检查更新...")
            # 显示进度条并重置进度，使用主线程更新方法
            self._update_progress_bar(20)
            # 在异步任务中执行网络请求，避免阻塞UI
            self.task_executor.execute_task(
                func=self._fetch_latest_version,
                op_type="check_updates",
                extra_data={'from_button': from_button}
            )
        except Exception as e:
            logger.error(f"检查更新失败: {str(e)}")
            # 确保进度条重置为0
            self._update_progress_bar(0)
            QMessageBox.critical(self, "错误", f"检查更新失败: {str(e)}")
    
    def set_about_text(self):
        """
        设置关于页面的内容，包括版本号、作者信息、代码仓库链接等。
        
        功能:
        - 获取当前程序版本号
        - 设置textBrowser_about的文本内容，包括版本号、作者信息、代码仓库链接等
        """
        # 获取当前版本号
        version = self._get_current_version()
        if not version:
            version = "error"
        
        # 设置关于页面的内容，使用简单的字符串格式以避免Qt绘画错误
        about_text = "\n"
        about_text += "\n"
        about_text += "\n"
        about_text += "广西科师校园网登录助手\n"
        about_text += f"版本号：v{version}\n"
        about_text += "作者：quanmianup\n\n"
        about_text += "Gitee：https://gitee.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant（主推）\n"
        about_text += "Github：https://github.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant\n\n"
        about_text += "开源协议：MIT License\n\n"
        about_text += "本工具仅供学习交流使用"
        
        self.ui.textBrowser_about.setPlainText(about_text)
    
    def _get_current_version(self):
        """
        从pyproject.toml文件中读取当前程序的版本号。
        
        返回:
            str: 当前程序的版本号(如"1.0.0")，如果读取失败则返回None
        """

        
        try:
            # 检查是否在PyInstaller打包后的环境中运行
            if getattr(sys, 'frozen', False):
                # 在打包后的环境中，使用sys._MEIPASS获取临时解压目录
                # 尝试在临时目录中查找pyproject.toml
                pyproject_path = os.path.join(sys._MEIPASS, "pyproject.toml")
            else:
                # 在开发环境中，使用相对路径
                pyproject_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pyproject.toml")
            
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomllib.load(f)
            # 从pyproject.toml中获取版本号
            current_version = pyproject_data.get("project", {}).get("version", "1.0.0")
            return current_version
        except Exception as e:
            logger.error(f"读取pyproject.toml文件失败: {str(e)}")
            # 读取失败时返回默认版本号
            return None
            
    def _update_progress_bar(self, value):
        """
        在主线程中更新进度条，避免Qt绘画错误
        
        参数:
            value (int): 进度条值(0-100)
        """
        # 使用QMetaObject.invokeMethod确保UI更新在主线程中执行
        QMetaObject.invokeMethod(
            self.ui.progressBar, 
            "setValue", 
            Qt.QueuedConnection,
            Q_ARG(int, value)
        )
        
    def _fetch_latest_version(self):
        """
        从Gitee仓库获取最新版本信息。
        
        返回:
            dict: 包含最新版本信息的字典
        """

        try:
            # 模拟进度更新
            # 获取URL阶段
            self._update_progress_bar(30)
            url = "https://gitee.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant/releases/latest"
            # 允许重定向，并获取最终的URL
            self._update_progress_bar(50)
            response = requests.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            # 从重定向后的URL中提取版本号
            self._update_progress_bar(70)
            redirected_url = response.url
            # 通过分割URL字符串获取版本号,去除版本号前的'v'字符
            latest_version = redirected_url.rsplit('/', 1)[-1][1:]
            latest_version = latest_version
            current_version = self._get_current_version()
            self._update_progress_bar(80)
            
            if not latest_version:
                self._update_progress_bar(0)
                return {"success": False, "message": "未找到版本信息"}
            # 获取当前版本号
            if current_version is None:
                self._update_progress_bar(0)
                return {"success": False, "message": "无法获取当前版本号"}

            is_newer = self.compare_versions(latest_version, current_version)
            self._update_progress_bar(100)
            
            return {
                "success": True,
                "latest_version": latest_version,
                "current_version": current_version,
                "is_newer": is_newer
            }
            
        except requests.RequestException as e:
            self._update_progress_bar(0)
            return {"success": False, "message": f"网络请求失败: {str(e)}"}
        except Exception as e:
            self._update_progress_bar(0)
            return {"success": False, "message": f"获取版本信息失败: {str(e)}"}
    
    def _save_check_update_state(self):
        """
        保存启动时检查更新的状态到配置文件中。
        """
        is_checked = self.ui.checkBox_update.isChecked()
        credentials.set('UPDATE_ON_START', is_checked)
        logger.info(f"已{'启用' if is_checked else '禁用'}启动时检查更新功能")
            
    def _toggle_keep_network_online(self):
        """
        切换保持网络在线功能的开关，记录日志。
        """
        if self.ui.pushButton_keeplogin.isChecked():
            logger.info("保持网络功能已开启")
        else:
            logger.info("保持网络功能已关闭")
    
    def compare_versions(self, v1, v2):
        """
        比较两个版本号，返回v1是否大于v2。
        
        参数:
            v1 (str): 第一个版本号，格式为x.y.z
            v2 (str): 第二个版本号，格式为x.y.z
        
        返回:
            bool: 如果v1大于v2则返回True，否则返回False
        """
        v1_parts = list(map(int, v1.split('.')))
        v2_parts = list(map(int, v2.split('.')))
        return v1_parts > v2_parts
    
    def _check_network_status_and_update_tabwiget(self):
        """
        定期检查网络状态，更新UI显示，并在需要时自动尝试登录。
        
        功能:
        - 检查网络连接状态
        - 更新UI中的网络状态显示
        - 在网络离线且保活功能开启时，自动尝试重新登录
        """
        self.task_executor.execute_task(
            func=lambda: networkmanager.check_network(), 
            op_type="keep_alive_check"
        )

    def setup_log_context_menu(self):
        """
        设置日志控件的右键菜单，用于清空日志内容。
        """
        self.ui.menuBar.hide()
        
        # 直接使用lambda表达式显示右键菜单，避免单独的show_log_context_menu方法
        self.ui.textBrowser_log.customContextMenuRequested.connect(
            lambda position: self.ui.menulogMenu.exec_(self.ui.textBrowser_log.mapToGlobal(position))
        )
        # 连接action_clear_log的triggered信号到清空日志的槽函数
        self.ui.action_clear_log.triggered.connect(self.ui.textBrowser_log.clear)

    def save_credentials(self):
        """
        保存用户凭证到配置文件，根据用户选择决定是否保存密码。
        """
        username = self.ui.lineEdit_username.text().strip()
        password = self.ui.lineEdit_password.text().strip()
        setup_logger(username=username)
        if self.ui.checkBox.isChecked():
            credentials.set('username', username)
            credentials.set('password', password)
        else:
            credentials.set('username', '')
            credentials.set('password', '')

    def handle_general_finished(self, success, message, op_type="unknown", extra_data=None):
        """
        处理异步任务完成后的回调，根据任务类型更新UI状态。
        
        参数:
            success: 任务是否执行成功的布尔值
            message: 任务执行返回结果或错误信息
            op_type: 操作类型标识
            extra_data: 额外的数据，包含触发来源等信息
        
        支持的操作类型:
        - "login": 登录操作
        - "dislogin": 下线操作
        - "create_task": 创建计划任务
        - "query_tasks": 查询计划任务
        - "delete_task": 删除计划任务
        - "check_updates": 版本更新检查
        - "keep_alive_check": 网络保活检查
        """
        # 确保extra_data是字典
        if extra_data is None:
            extra_data = {}
        
        try:
            if op_type == "login":
                # 登录结果处理
                if success and message == True:
                    self.ui.label_green_message.setText("登录成功！")
                    self.ui.stackedWidget_message.setCurrentIndex(1)
                else:
                    self.ui.label_red_message.setText("登录失败！")
                    self.ui.stackedWidget_message.setCurrentIndex(2)
                self.ui.pushButton_login.setEnabled(True)
            
            elif op_type == "dislogin":
                # 下线结果处理
                if success and message == True:
                    self.ui.label_green_message.setText("下线成功！")
                    self.ui.stackedWidget_message.setCurrentIndex(1)
                else:
                    self.ui.label_red_message.setText("下线失败")
                    self.ui.stackedWidget_message.setCurrentIndex(2)
                self.ui.pushButton_dislogin.setEnabled(True)
            
            elif op_type == "create_task":
                # 创建任务结果处理
                if isinstance(message, tuple):
                    create_success, file_name = message
                else:
                    create_success, file_name = success, message

                if create_success:
                    self.query_tasks()
                    QMessageBox.information(
                        self, "成功", f"计划任务 '{file_name}' 创建成功！")
                    logger.info(f"计划任务'{file_name}'创建成功！")
                else:
                    QMessageBox.critical(self, "错误", f"创建任务失败:\n{str(message[1])}")
                    logger.error(f"创建任务失败: {str(message[1])}")
            
            elif op_type == "query_tasks":
                # 查询任务结果处理
                query_success ,task_list = message
                if query_success:
                    if not isinstance(task_list, list):
                        logger.error(f"查询任务返回结果不是列表类型，实际类型: {type(task_list).__name__}，结果内容: {task_list}")
                        QMessageBox.critical(
                            self, "错误", "查询任务返回结果格式错误")
                        return
                    if not task_list:
                        # 当没有查询到任务时，清空表格并在第一行显示提示信息
                        self.ui.task_table.setRowCount(1)
                        item = QTableWidgetItem("没有查询到匹配的任务")
                        item.setToolTip("没有查询到匹配的任务")
                        # 合并单元格，让提示信息显示在整行
                        self.ui.task_table.setItem(0, 0, item)
                        self.ui.task_table.setSpan(0, 0, 1, self.ui.task_table.columnCount())
                        return
                    # 更新任务列表
                    try:
                        self.ui.task_table.setRowCount(0)
                        column_keys = {
                            0: "name",
                            1: "filepath",
                            2: "status",
                            3: "next_run"
                        }
                        
                        for row, task in enumerate(task_list):
                            self.ui.task_table.insertRow(row)
                            for col, key in column_keys.items():
                                item = QTableWidgetItem(task[key])
                                item.setToolTip(task[key])
                                self.ui.task_table.setItem(row, col, item)
                        self.ui.task_table.resizeColumnsToContents()
                        
                    except Exception as e:
                        QMessageBox.critical(
                            self, "错误", f"更新任务列表失败:\n{str(e)}")
                        logger.error(f"更新任务列表失败: {str(e)}")
                else:
                    QMessageBox.critical(self, "错误", f"查询任务失败:\n{task_list}")
                    logger.error(f"查询任务失败: {task_list}")
            
            elif op_type == "delete_task":
                # 删除任务结果处理
                if isinstance(message, tuple):
                    delete_message = message[1] if len(message) > 1 else str(message)
                else:
                    delete_message = str(message)

                if success:
                    self.query_tasks()
                    QMessageBox.information(self, "成功", delete_message)
                else:
                    QMessageBox.critical(self, "错误", f"删除任务失败:\n{delete_message}")
                    logger.error(f"删除任务失败: {delete_message}")
            
            elif op_type == "check_updates":
                # 检查更新结果处理
                if success and message and message.get("success"):
                    if message.get("is_newer"):
                        latest_version = message.get("latest_version")
                        current_version = message.get("current_version")
                        
                        logger.info(f"发现新版本: {latest_version}")
                        
                        msg_box = QMessageBox(self)
                        msg_box.setWindowTitle("发现新版本")
                        msg_box.setText(f"发现新版本 {latest_version}，当前版本 {current_version}\n\n是否前往Gitee查看更新内容？")
                        msg_box.setIcon(QMessageBox.Information)
                        
                        yes_btn = msg_box.addButton("前往下载", QMessageBox.ActionRole)
                        msg_box.addButton("取消", QMessageBox.RejectRole)
                        
                        msg_box.exec_()
                        
                        if msg_box.clickedButton() == yes_btn:
                            # 打开浏览器访问Gitee仓库
                            webbrowser.open("https://gitee.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant/releases/latest")
                    else:
                        # 已是最新版本
                        logger.info(f"当前已是最新版本 {message.get('current_version')}")
                        # 判断是否从按钮点击触发的检查更新
                        from_button = extra_data.get('from_button', False)
                        if from_button:
                            # 从按钮点击触发的检查更新，显示已是最新版本的提示
                            QMessageBox.information(self, "提示", f"当前已是最新版本 {message.get('current_version')}")
                else:
                    # 检查更新失败
                    error_msg = message.get("message", "未知错误") if isinstance(message, dict) else str(message)
                    logger.error(f"检查更新失败: {error_msg}")
                    QMessageBox.critical(self, "错误", f"检查更新失败: {error_msg}")
            
            elif op_type == "keep_alive_check":
                # 网络在线检测结果处理
                current_time = QTime.currentTime()
                if success:
                    if message:
                        # 网络在线，显示成功状态
                        self.ui.stackedWidget_message_netstatus.setCurrentIndex(1)
                        # 检查是否需要记录网络在线日志：
                        # 1. 如果是首次检测（_last_network_status不存在）
                        # 2. 或者之前是离线状态（_last_network_status为False）
                        if not hasattr(self, '_last_network_status') or not self._last_network_status:
                            logger.info(f"网络在线")
                        # 更新网络状态记录
                        self._last_network_status = True
                    else:
                        # 网络离线，显示失败状态
                        self.ui.stackedWidget_message_netstatus.setCurrentIndex(2)
                        # 更新网络状态记录
                        self._last_network_status = False
                        # 检查保活按钮是否开启，如果开启则尝试登录,检查当前时间是否在00:00-7:00之间
                        # if self.ui.pushButton_keeplogin.isChecked() :
                        if self.ui.pushButton_keeplogin.isChecked() and (current_time.hour() <= 24 and current_time.hour() > 7):
                            # 在后台线程执行登录尝试
                            username = self.ui.lineEdit_username.text().strip()
                            password = self.ui.lineEdit_password.text().strip()
                            networkmanager.login(username=username, password=password)
       
        except Exception as e:
            logger.error(f"处理异步任务 {op_type} 结果失败: {e}")
            QMessageBox.critical(self, "错误", f"处理异步任务 {op_type} 结果失败: {e}")
            self.ui.label_red_message.setText("登录失败！")
            self.ui.stackedWidget_message.setCurrentIndex(2)
            self.ui.stackedWidget_message_netstatus.setCurrentIndex(0)
            self.ui.pushButton_login.setEnabled(True)
            self.ui.pushButton_dislogin.setEnabled(True)

    def login(self):
        """
        执行登录操作，异步调用NetworkManager进行校园网登录。
        
        功能:
        - 更新UI状态为"登录中"
        - 禁用登录按钮防止重复点击
        - 获取用户名和密码
        - 异步执行登录任务
        - 保存用户凭证
        """
        self.ui.stackedWidget_message.setCurrentIndex(0)
        self.ui.label_black_message.setText("登录中...")
        self.ui.pushButton_login.setEnabled(False)

        username = self.ui.lineEdit_username.text().strip()
        password = self.ui.lineEdit_password.text().strip()
        # 使用lambda函数绑定参数，直接传递已绑定参数的函数
        self.task_executor.execute_task(
            func=lambda: networkmanager.login(username, password), 
            op_type="login"
        )
        self.save_credentials()

    def dislogin(self):
        """
        执行下线操作，异步调用NetworkManager进行校园网下线。
        
        功能:
        - 更新UI状态为"下线中"
        - 禁用下线按钮防止重复点击
        - 获取用户名
        - 异步执行下线任务
        - 保存用户凭证
        """
        self.ui.stackedWidget_message.setCurrentIndex(0)
        self.ui.label_black_message.setText("下线中...")
        self.ui.pushButton_dislogin.setEnabled(False)

        username = self.ui.lineEdit_username.text()
        # 直接传递函数和参数
        self.task_executor.execute_task(
            func=lambda: networkmanager.dislogin(username), 
            op_type="dislogin"
        )
        self.save_credentials()

    def select_file(self):
        """
        选择要执行的文件，用于创建计划任务。
        
        功能:
        - 打开文件选择对话框
        - 获取用户选择的文件路径
        - 更新UI中的文件路径和文件名显示
        """
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self, 
            caption="选择要执行的文件", 
            dir=str(self.task_manager.task_folder), 
            filter="所有文件 (*.*)"
        )

        if file_path:
            self.ui.file_path_edit.setText(file_path)
            file_name = os.path.basename(file_path)
            self.ui.task_name_label.setText(file_name)

    def create_task(self):
        """
        异步创建计划任务。
        
        功能:
        - 验证文件路径的有效性
        - 异步执行任务创建操作
        """
        file_path = self.ui.file_path_edit.text().strip()

        if not os.path.exists(file_path):
            QMessageBox.warning(self, "警告", "请选择有效的文件")
            logger.warning("请选择有效的文件")
            return

        self.task_executor.execute_task(
            func=lambda: self.task_manager.create_task(file_path), 
            op_type="create_task"
        )

    def query_tasks(self, from_source:str = None):
        """
        异步查询计划任务。
        
        功能:
        - 异步执行任务查询操作
        - 结果会通过handle_general_finished方法更新到任务表格中
        """
        self.task_executor.execute_task(
            func=lambda: self.task_manager.query_tasks(), 
            op_type="query_tasks",
            extra_data={"from_source": from_source}
        )
        
    def delete_task(self):
        """
        异步删除计划任务。
        
        功能:
        - 检查是否选择了要删除的任务
        - 显示确认对话框
        - 异步执行任务删除操作
        """
        selected_items = self.ui.task_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请先选择要删除的任务")
            return

        original_name = selected_items[0].text()
        full_task_name = self.task_manager.get_full_task_name(original_name)

        if QMessageBox.Yes == QMessageBox.question(
                self, "确认删除",
                f"确定要删除任务 '{original_name}' 吗？",
                QMessageBox.Yes | QMessageBox.No
        ):
            self.task_executor.execute_task(
                func=lambda: self.task_manager.delete_task(full_task_name), 
                op_type="delete_task"
            )

    def create_exe(self):
        """
        生成自动登录的 EXE 文件。
        
        功能:
        - 确保任务文件夹存在
        - 从源路径复制预先生成的 AutoLoginScript.exe 文件
        - 显示生成成功提示和文件路径
        - 提供打开文件目录的选项
        
        异常:
            FileNotFoundError: 当源EXE文件不存在时抛出
        """

        try:
            # 确保任务文件夹存在
            self.task_manager.task_folder.mkdir(parents=True, exist_ok=True)

            logger.info("开始生成EXE文件...")
            self.ui.stackedWidget_message.setCurrentIndex(0)
            self.ui.label_black_message.setText("正在生成EXE文件...")
            self.ui.pushButton_generate.setEnabled(False)

            # 定义源EXE文件路径（AutoLoginScript.exe）
            # 使用相对路径或打包时包含的资源路径
            # 首先尝试从当前可执行文件所在目录查找
            if getattr(sys, 'frozen', False):
                # 如果是打包后的exe文件
                current_dir = os.path.dirname(sys.executable)
                source_exe_path = os.path.join(current_dir, "AutoLoginScript.exe")
            else:
                # 如果是开发环境
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                source_exe_path = os.path.join(project_root, "dist", "AutoLoginScript.exe")
            
            # 确保源文件存在
            if not os.path.exists(source_exe_path):
                raise FileNotFoundError(f"源EXE文件不存在: {source_exe_path}\n请先运行build_auto_login.ps1脚本生成此文件")
            
            target_exe_path = self.task_manager.task_folder.joinpath("AutoLoginScript.exe")
            
            # 复制文件
            shutil.copy2(source_exe_path, target_exe_path)
            logger.info(f"文件生成成功: {target_exe_path}")

            # 弹出提示框
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("生成成功")
            msg_box.setText(f"EXE 文件已成功生成，保存路径为：\n{target_exe_path}")
            logger.info(f"EXE 文件已成功生成，保存路径为：{target_exe_path}")
            open_folder_btn = msg_box.addButton(
                "打开文件目录", QMessageBox.ActionRole)
            msg_box.addButton("关闭", QMessageBox.RejectRole)
            msg_box.exec_()

            if msg_box.clickedButton() == open_folder_btn:
                # 打开任务文件夹
                if sys.platform.startswith('win'):
                    os.startfile(self.task_manager.task_folder)
                elif sys.platform.startswith('darwin'):
                    subprocess.run(['open', self.task_manager.task_folder])
                elif sys.platform.startswith('linux'):
                    subprocess.run(['xdg-open', self.task_manager.task_folder])

            self.ui.stackedWidget_message.setCurrentIndex(1)
            self.ui.label_green_message.setText("EXE文件生成成功")
            self.ui.pushButton_generate.setEnabled(True)

        except Exception as e:
            logger.critical(f"生成EXE文件失败: {str(e)}, 错误详情: {getattr(e, 'stderr', '')}")
            QMessageBox.critical(self, "错误", f"生成EXE文件失败: {str(e)}")
            self.ui.pushButton_generate.setEnabled(True)
            self.ui.stackedWidget_message.setCurrentIndex(2)
            self.ui.label_red_message.setText("EXE文件生成失败")


class PasswordDialog(QDialog):
    """
    密码验证对话框，用于验证用户是否有权限使用程序。
    
    属性:
        ui: 对话框UI实例，包含密码输入框和提示信息
    """
    def __init__(self, parent=None):
        """
        初始化密码对话框
        
        参数:
            parent (QWidget, optional): 父窗口控件，默认为None
        """
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText("确认")
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("取消")


def run():
    """
    启动主界面程序
    
    功能说明：
    1. 创建QApplication实例
    2. 创建并显示主窗口
    3. 根据配置决定是否需要密码验证
    4. 运行应用程序主循环
    
    注意事项：
    - 程序启动时会检查是否设置了主界面锁定
    - 如果设置了锁定，会显示密码验证对话框
    - 密码验证成功后才能使用程序的全部功能
    - 验证失败次数超过限制可能会导致程序退出
    
    示例:
    ```python
    # 通过导入并调用此函数来启动应用程序
    from src.gui.main_gui_program import run
    run()
    ```
    """
    # 首先创建QApplication实例
    application = QApplication(sys.argv)
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    # # =================================================================
    # 禁用窗口功能，直到密码验证通过
    if credentials.get('MAIN_LOCK'):
        window.setEnabled(False)
        password_dialog = PasswordDialog(window)
        while True:
            if password_dialog.exec() == QDialog.Accepted:
                if password_dialog.ui.lineEdit_pswdInput.text() == 'pd11040870':
                    window.setEnabled(True)
                    credentials.set('MAIN_LOCK', False)
                    break
                QMessageBox.warning(window, '密码错误', '密码不正确，请重新输入！')
            else:
                sys.exit()
    # # =================================================================
    sys.exit(application.exec())
