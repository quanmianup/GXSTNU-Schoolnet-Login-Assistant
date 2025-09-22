"""
主界面程序，负责创建和管理 GUI 界面。
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path
import time

from PySide6.QtCore import Qt, QPoint, QTime, QEvent, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem

from src.core.AsyncTaskExecutor import AsyncTaskExecutor
from src.core.NetworkManager import networkmanager
from src.gui.main_ui import *
from src.utils.logger import logger, setup_logger
from src.core.TaskScheduler import TaskScheduler
from config.credentials import credentials



class MainWindow(QMainWindow):
    """
    主窗口类，负责创建和管理 GUI 界面。
    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.time_edit.setTime(QTime.currentTime())
        self.ui.lineEdit_username.setText(credentials.get('username', ''))
        self.ui.lineEdit_password.setText(credentials.get('password', ''))
        self.ui.label_black_message.setText("")

        self.task_manager = TaskScheduler()
        self.task_executor = AsyncTaskExecutor()
        # 连接信号槽
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
    
    def _init_ui_connect_(self):
        """
        初始化 UI 组件的事件连接。
        """
        self.ui.select_file_btn.clicked.connect(self.select_file)
        self.ui.create_btn.clicked.connect(self.create_task)
        self.ui.query_btn.clicked.connect(self.query_tasks)
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
        self.ui.pushButton_tab_main.clicked.connect(
            lambda: self.ui.stackedWidget_tab.setCurrentIndex(0))
        self.ui.pushButton_tab_manege.clicked.connect(
            lambda: (
                self.ui.stackedWidget_tab.setCurrentIndex(1),
                self.query_tasks()
            ))
        
        # 连接保活按钮信号
        self.ui.pushButton_keeplogin.clicked.connect(self._toggle_keep_network_online)

    def eventFilter(self, obj, event):
        """
        事件过滤器，处理标题栏的鼠标事件。
        """
        if obj == self.ui.frame_title:
            if event.type() == QEvent.MouseButtonPress:
                self.mousePressEvent(event)
            elif event.type() == QEvent.MouseMove:
                self.mouseMoveEvent(event)
            elif event.type() == QEvent.MouseButtonRelease:
                self.mouseReleaseEvent(event)
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        """
        鼠标按下事件，记录鼠标按下时的位置。
        """
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        """
        鼠标移动事件，根据鼠标移动的偏移量移动窗口。
        """
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件，停止拖动。
        """
        if event.button() == Qt.LeftButton:
            self.dragging = False
    
    def _toggle_keep_network_online(self):
        """
        切换保持网络在线功能的开关
        """
        if self.ui.pushButton_keeplogin.isChecked():
            logger.info("保持网络功能已开启")
        else:
            logger.info("保持网络功能已关闭")
    
    def _check_network_status_and_update_tabwiget(self):
        """
        检查网络状态，先更新UI显示，再根据保活按钮状态决定是否尝试登录
        """
        # # 检查当前时间是否在00:00-7:00之间
        # current_time = QTime.currentTime()
        # if (current_time.hour() >= 0 and current_time.hour() < 7):
        #     # 在禁用时间段，不执行保活操作
        #     return
        self.task_executor.execute_task(
            func=lambda: networkmanager.check_network(), 
            op_type="keep_alive_check"
        )

    def setup_log_context_menu(self):
        """
        设置日志控件的右键菜单
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
        保存用户凭证到配置文件。
        """
        username = self.ui.lineEdit_username.text()
        setup_logger(username=username)
        if self.ui.checkBox.isChecked():
            credentials.set('username', self.ui.lineEdit_username.text().strip())
            credentials.set('password', self.ui.lineEdit_password.text().strip())
        else:
            credentials.set('username', '')
            credentials.set('password', '')

    def handle_general_finished(self, success, message, op_type="unknown"):
        """
        处理异步任务完成后的回调。
        """
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
            
            elif op_type == "exe_generation":
                # EXE生成结果处理
                self.ui.pushButton_generate.setEnabled(True)
                if success:
                    self.ui.stackedWidget_message.setCurrentIndex(1)
                    self.ui.label_green_message.setText("EXE文件生成成功...")

                    # 构建EXE文件的完整路径
                    username = self.ui.lineEdit_username.text().strip()
                    exe_name = f"login{username}.exe"
                    exe_path = self.task_manager.task_folder / exe_name

                    # 弹出提示框
                    msg_box = QMessageBox(self)
                    msg_box.setWindowTitle("生成成功")
                    msg_box.setText(f"EXE 文件已成功生成，保存路径为：\n{exe_path}")
                    logger.info(f"EXE 文件已成功生成，保存路径为：{exe_path}")
                    open_folder_btn = msg_box.addButton(
                        "打开文件目录", QMessageBox.ActionRole)
                    close_btn = msg_box.addButton("关闭", QMessageBox.RejectRole)
                    msg_box.exec_()

                    if msg_box.clickedButton() == open_folder_btn:
                        # 打开任务文件夹
                        if sys.platform.startswith('win'):
                            os.startfile(self.task_manager.task_folder)
                        elif sys.platform.startswith('darwin'):
                            subprocess.run(['open', self.task_manager.task_folder])
                        elif sys.platform.startswith('linux'):
                            subprocess.run(['xdg-open', self.task_manager.task_folder])

                    # 自动清理build目录和.spec文件
                    build_dir = self.task_manager.task_folder / "build"
                    spec_file = self.task_manager.task_folder / f"{exe_name.replace('.exe', '')}.spec"
                    if build_dir.exists():
                        shutil.rmtree(build_dir)
                    if spec_file.exists():
                        spec_file.unlink()

                    # 不删除auto_login.py脚本
                    auto_login_script_path = self.task_manager.task_folder / "auto_login.py"
                    if auto_login_script_path.exists():
                        auto_login_script_path.unlink()

                else:
                    logger.error(f"生成EXE文件失败: {message}")
                    QMessageBox.critical(self, "错误", f"生成EXE文件失败: {message}")
            
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
                    QMessageBox.critical(self, "错误", f"创建任务失败:\n{message}")
                    logger.error(f"创建任务失败: {message}")
            
            elif op_type == "query_tasks":
                # 查询任务结果处理
                query_success ,task_list = message
                if query_success:
                    if not isinstance(task_list, list):
                        logger.error(f"查询任务返回结果不是列表类型，实际类型: {type(task_list).__name__}，结果内容: {task_list}")
                        QMessageBox.critical(
                            self, "错误", "查询任务返回结果格式错误")
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
                        QMessageBox.information(self, "提示", "查询任务成功")
                    except Exception as e:
                        QMessageBox.critical(
                            self, "错误", f"更新任务列表失败:\n{str(e)}")
                        logger.error(f"更新任务列表失败: {str(e)}")
                    if not task_list:
                        QMessageBox.information(
                            self, "提示", "没有查询到匹配的任务")
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
            
            elif op_type == "keep_alive_check":
                # 保持网络在线检查结果处理
                # 解析返回结果，格式为(success_status, status_message)
                if isinstance(message, tuple) and len(message) == 2:
                    status_success, status_message = message
                else:
                    status_success, status_message = success, message
                
                # 更新UI显示网络状态
                if status_success:
                    # 网络在线，显示成功状态
                    self.ui.stackedWidget_message_netstatus.setCurrentIndex(1)
                    logger.info(f"保持网络检查结果: {status_message}")
                else:
                    # 网络离线，显示失败状态
                    self.ui.stackedWidget_message_netstatus.setCurrentIndex(2)
                    logger.error(f"保持网络检查失败: {status_message}")
                    
                    # 检查保活按钮是否开启，如果开启则尝试登录
                    if self.ui.pushButton_keeplogin.isChecked():
                        # 在后台线程执行登录尝试
                        def try_login():
                            logger.warning("网络连接已断开，尝试重新登录")
                            
                            # 尝试登录5次直到成功
                            username = self.ui.lineEdit_username.text().strip()
                            password = self.ui.lineEdit_password.text().strip()
                            
                            for attempt in range(1, 6):
                                logger.info(f"第 {attempt} 次登录尝试")
                                if networkmanager.login(username, password):
                                    logger.info("登录成功，网络已恢复连接")
                                    return True, "登录成功"
                                
                                # 最后一次尝试失败后不再等待
                                if attempt < 5:
                                    # 等待一段时间后再次尝试
                                    time.sleep(2)
                            
                            logger.error("连续5次登录尝试均失败")
                            return False, "登录失败: 连续5次尝试均失败"
                        
                        # 立即执行登录尝试
                        self.task_executor.execute_task(
                            func=try_login, 
                            op_type="keep_alive_check"
                        )
        except Exception as e:
            logger.error(f"处理异步任务 {op_type} 结果失败: {e}")
            QMessageBox.critical(self, "错误", f"处理异步任务 {op_type} 结果失败: {e}")
            self.ui.label_red_message.setText("登录失败！")
            self.ui.stackedWidget_message.setCurrentIndex(2)
            self.ui.pushButton_login.setEnabled(True)
            self.ui.pushButton_dislogin.setEnabled(True)

    def login(self):
        """
        执行登录操作。
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
        执行下线操作。
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
        选择要执行的文件。
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择要执行的文件", "", "所有文件 (*.*)"
        )

        if file_path:
            self.ui.file_path_edit.setText(file_path)
            file_name = os.path.basename(file_path)
            self.ui.task_name_label.setText(file_name)

    def create_task(self):
        """
        异步创建计划任务。
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

    def query_tasks(self):
        """
        异步查询计划任务。
        """
        self.task_executor.execute_task(
            func=lambda: self.task_manager.query_tasks(), 
            op_type="query_tasks"
        )

    def delete_task(self):
        """
        异步删除计划任务。
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
        """
        username = self.ui.lineEdit_username.text().strip()
        password = self.ui.lineEdit_password.text().strip()

        # 输入验证
        if not username or not password:
            QMessageBox.critical(self, "错误", "请输入账号和密码")
            return False

        try:
            # 确保任务文件夹存在
            self.task_manager.task_folder.mkdir(parents=True, exist_ok=True)

            # 生成自动登录脚本，将脚本放在 task_folder 目录下
            auto_login_script = self._generate_auto_login_script(username, password)
            auto_login_script_path = self.task_manager.task_folder.joinpath("auto_login.py")
            with open(auto_login_script_path, "w", encoding="utf-8") as f:
                f.write(auto_login_script)

            # 确认脚本路径
            logger.info(f"自动登录脚本路径: {auto_login_script_path}")

            exe_name = f"login{username}"
            logger.info("开始生成EXE文件...")
            self.ui.stackedWidget_message.setCurrentIndex(0)
            self.ui.label_black_message.setText("正在生成EXE文件...")
            self.ui.pushButton_generate.setEnabled(False)

            # 使用 cx_Freeze 生成 EXE 文件
            # generate_exe_with_cx_freeze(str(auto_login_script_path), exe_name, str(self.task_manager.task_folder))

            self.ui.pushButton_generate.setEnabled(True)
            self.ui.stackedWidget_message.setCurrentIndex(1)
            self.ui.label_green_message.setText("EXE文件生成成功")

            # 构建 EXE 文件的完整路径
            exe_path = self.task_manager.task_folder.joinpath(f"{exe_name}.exe")

            # 弹出提示框
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("生成成功")
            msg_box.setText(f"EXE 文件已成功生成，保存路径为：\n{exe_path}")
            logger.info(f"EXE 文件已成功生成，保存路径为：{exe_path}")
            open_folder_btn = msg_box.addButton(
                "打开文件目录", QMessageBox.ActionRole)
            close_btn = msg_box.addButton("关闭", QMessageBox.RejectRole)
            msg_box.exec_()

            if msg_box.clickedButton() == open_folder_btn:
                # 打开任务文件夹
                if sys.platform.startswith('win'):
                    os.startfile(self.task_manager.task_folder)
                elif sys.platform.startswith('darwin'):
                    subprocess.run(['open', self.task_manager.task_folder])
                elif sys.platform.startswith('linux'):
                    subprocess.run(['xdg-open', self.task_manager.task_folder])

            # 自动清理 build 目录和 .spec 文件
            build_dir = self.task_manager.task_folder / "build"
            if build_dir.exists():
                shutil.rmtree(build_dir)

            # 不删除 auto_login.py 脚本
            auto_login_script_path = self.task_manager.task_folder / "auto_login.py"
            if auto_login_script_path.exists():
                auto_login_script_path.unlink()

        except Exception as e:
            logger.critical(f"生成EXE文件失败: {str(e)}, 错误详情: {getattr(e, 'stderr', '')}")
            QMessageBox.critical(self, "错误", f"生成EXE文件失败: {str(e)}")
            self.ui.pushButton_generate.setEnabled(True)
            self.ui.stackedWidget_message.setCurrentIndex(2)
            self.ui.label_red_message.setText("EXE文件生成失败")

    @staticmethod
    def _generate_auto_login_script(username, password):
        """
        生成自动登录脚本内容。
        """
        # 使用单引号构建整个脚本内容，避免三引号嵌套导致的解析问题
        script_content = '''
import sys
import time
import socket
from pathlib import Path
from typing import Optional

# 设置编码
import io
import os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class LoginHelper:
    """自动登录助手类，封装登录逻辑和工具方法"""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.setup_project_paths()
        self._import_required_modules()
        
    def setup_project_paths(self) -> None:
        """设置项目路径，处理开发环境和打包环境的差异"""
        # 确定基础路径，处理不同运行环境
        if getattr(sys, 'frozen', False):
            # 打包后的环境，从临时解压目录获取路径
            self.base_path = Path(sys._MEIPASS)
        else:
            # 开发环境，从代码文件位置获取路径
            self.base_path = Path(__file__).parent.parent.parent
            
        # 动态构建模块路径
        for path_segment in ['app', 'app/core', 'app/utils']:
            sys.path.insert(0, str(self.base_path / path_segment))
    
    def _import_required_modules(self) -> None:
        """动态导入必要的模块，确保在运行时可用"""
        global networkmanager, logger, setup_logger
        try:
            from app.core.network import networkmanager
            from app.utils.logger import logger, setup_logger
            setup_logger(username=self.username)
        except ImportError as e:
            print(f"导入模块失败: {{str(e)}}")
            # 尝试备用导入路径
            try:
                # 尝试直接导入，适用于独立运行场景
                import networkmanager
                import logger
                setup_logger = logger.setup_logger
                setup_logger(username=self.username)
            except ImportError:
                print("无法导入必要的模块，请确保程序目录结构正确。")
                sys.exit(1)
    
    def check_network_connectivity(self, host: str = "www.baidu.com", port: int = 80, timeout: int = 3) -> bool:
        """检查网络连接是否正常"""
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False
    
    def login(self, max_retries: int = 3, retry_delay: int = 2) -> bool:
        """执行登录操作，支持重试机制"""
        retries = 0
        
        # 首先检查网络连接
        if not self.check_network_connectivity():
            print("网络连接不可用，请检查网络设置。")
            logger.error("网络连接不可用，请检查网络设置。")
            return False
            
        while retries < max_retries:
            try:
                print(f"{{'重试' if retries > 0 else '尝试'}}登录账号: {{self.username}}")
                result = networkmanager.login(self.username, self.password)
                
                if result:
                    print("登录成功！")
                    logger.info("自动登录成功！")
                    return True
                else:
                    retries += 1
                    error_msg = f"登录失败{{', 将重试' if retries < max_retries else ''}}！"
                    print(error_msg)
                    logger.error(error_msg)
                    
                    if retries < max_retries:
                        print(f"等待 {{retry_delay}} 秒后重试...")
                        time.sleep(retry_delay)
            except Exception as e:
                retries += 1
                error_msg = f"登录过程中出错: {{str(e)}}{{', 将重试' if retries < max_retries else ''}}"
                print(error_msg)
                logger.error(error_msg)
                
                if retries < max_retries:
                    print(f"等待 {{retry_delay}} 秒后重试...")
                    time.sleep(retry_delay)
        
        return False

    def run(self) -> None:
        """运行自动登录流程"""
        try:
            print("=== 校园网自动登录工具 ===")
            print(f"当前时间: {{time.strftime('%Y-%m-%d %H:%M:%S')}}")
            
            # 执行登录
            success = self.login()
            
            # 登录结果后显示状态信息
            if success:
                print("自动登录流程已完成。")
                logger.info("自动登录流程已完成。")
            else:
                print("自动登录流程失败，请检查账号密码或网络状态。")
                logger.error("自动登录流程失败，请检查账号密码或网络状态。")
                
        except KeyboardInterrupt:
            print("\n程序已被用户中断。")
            logger.info("程序已被用户中断。")
        except Exception as e:
            print(f"程序运行时发生未预期错误: {{str(e)}}")
            logger.error(f"程序运行时发生未预期错误: {{str(e)}}")

if __name__ == '__main__':
    # 创建并运行登录助手
    login_helper = LoginHelper(username='{0}', password='{1}')
    login_helper.run()
    
    # 保持终端打开，方便查看错误信息
    try:
        input("\n按回车键退出...")
    except (KeyboardInterrupt, EOFError):
        pass  # 允许用户通过Ctrl+C或Ctrl+D退出
'''
        
        # 使用format方法进行变量替换，确保正确处理字符串
        return script_content.format(username, password)

    def _build_pyinstaller_params(self, script_path, exe_name):
        """
        构建 PyInstaller 打包参数。
        """
        # 判断是否为打包后的环境
        if getattr(sys, 'frozen', False):
            project_root = Path(sys._MEIPASS)
        else:
            project_root = Path(__file__).parent.parent.parent

        config_path = project_root / "config"
        app_path = project_root / "app"
        core_path = project_root / "app" / "core"
        utils_path = project_root / "app" / "utils"
        icon_path = project_root / "assets" / "images" / "main_icon.ico"
        logger.debug(f"项目根目录: {project_root}")
        pyinstaller_path = shutil.which('pyinstaller')
        if not pyinstaller_path:
            logger.error("未找到 pyinstaller 可执行文件，请检查是否已安装。")
            raise FileNotFoundError("未找到 pyinstaller 可执行文件，请检查是否已安装。")
        data_sep = ';' if sys.platform.startswith('win') else ':'
        return [
            pyinstaller_path,
            # '--onefile',
            '--console',
            f'--name={exe_name}',
            '--debug=all',
            '--hidden-import=app',  # 显式添加 app 隐藏依赖
            '--hidden-import=app.core',  # 显式添加 app.core 隐藏依赖
            '--hidden-import=app.core.network',
            '--hidden-import=app.utils.logger',
            '--hidden-import=requests',
            '--collect-all=app',  # 收集 app 模块及其所有子模块
            '--collect-all=requests',
            '--log-level=DEBUG',
            f'--add-data={app_path.as_posix().strip()}{data_sep}app',
            f'--add-data={config_path.as_posix().strip()}{data_sep}config',
            f'--icon={icon_path.as_posix().strip()}' if icon_path.exists() else '--noconsole',
            f'--distpath={str(self.task_manager.task_folder)}',
            str(script_path)
        ]

    @staticmethod
    def _generate_exe(script_path, params):
        """
        执行 PyInstaller 命令生成 EXE 文件。
        """
        try:
            logger.info(f"执行命令: {' '.join(params)}")
            result = subprocess.run(
                params,
                capture_output=True,
                text=True,
                check=True,
                cwd=script_path.parent
            )
            logger.info("EXE文件生成成功")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(
                f"生成EXE文件失败: {e.stderr}, 命令: {' '.join(params)}")
            return False
        except Exception as e:
            logger.error(
                f"生成EXE文件时发生未知错误: {str(e)}, 命令: {' '.join(params)}")
            return False


def run():
    """
    启动主界面。
    """
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())
