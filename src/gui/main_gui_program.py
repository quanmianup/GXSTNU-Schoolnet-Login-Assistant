"""
主界面程序，负责创建和管理 GUI 界面。
"""
import os
import shutil
import subprocess
import sys

from PySide6.QtCore import Qt, QPoint, QTime, QEvent, QTimer
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
    """

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
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
        self.ui.pushButton_tab_main.clicked.connect(
            lambda: self.ui.stackedWidget_tab.setCurrentIndex(0))
        self.ui.pushButton_tab_manege.clicked.connect(
            lambda: (
                self.ui.stackedWidget_tab.setCurrentIndex(1),
                self.ui.time_edit.setTime(QTime.currentTime()),
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
        # logger.LOG_LEVEL = "CRITICAL"
        # setup_logger()
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
        - finished: 任务完成信号，参数为(success: bool, message: str, op_type: str)
        # success: 任务是否执行成功的布尔值
        # message: 任务执行返回结果或错误信息
        # op_type: 操作类型标识
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
                        QMessageBox.information(
                            self, "提示", "没有查询到匹配的任务")
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
                            networkmanager.login()
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
        通过复制预先生成的AutoLoginScript.exe文件到任务文件夹
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText("确认")
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("取消")

def run():
    """
    启动主界面。
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
