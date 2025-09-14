"""
主界面程序，负责创建和管理 GUI 界面。
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QPoint, QTime, QEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem
# from cx_Freeze import setup, Executable

from src.core.AsyncTaskExecutor import AsyncTaskExecutor
from src.core.network import networkmanager
from src.gui.main_ui import *
from src.utils.logger import logger, setup_logger
from src.utils.task_manager import TaskManager
from config.credentials import credentials


def generate_exe_with_cx_freeze(script_path, exe_name, output_dir):
    base = None
    if sys.platform == "win32":
        # 如果不需要控制台窗口，使用 "Win32GUI"
        base = "Win32GUI" if not sys.platform.startswith('win') else None
    else:
        base = None

    build_exe_options = {
        "packages": ["app", "app.core", "app.utils", "requests"],
        "include_files": [("config", "config"), ("app", "app")],
        "excludes": ["tkinter", "unittest"],  # 排除不需要的模块，减小包体积
        "include_msvcr": True  # 包含 Microsoft Visual C++ 运行时库
    }

    try:
        setup(
            name=exe_name,
            version="0.1",
            description="Auto Login EXE",
            options={"build_exe": build_exe_options},
            executables=[Executable(script_path, base=base, target_name=exe_name)]
        )
    except Exception as e:
        logger.error(f"cx_Freeze 生成 EXE 文件失败: {str(e)}")
        raise


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
        self.ui.checkBox.setChecked(True)

        self.task_manager = TaskManager()
        self.task_executor = AsyncTaskExecutor()
        self.task_executor.finished.connect(self.handle_general_finished)

        self._setup_ui()

        # 初始化拖动相关变量
        self.dragging = False
        self.offset = QPoint()

        # 为标题栏添加事件过滤器
        self.ui.frame_title.installEventFilter(self)

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

    def _setup_ui(self):
        """
        初始化 UI 组件的事件连接。
        """
        self.ui.select_file_btn.clicked.connect(self.select_file)
        self.ui.create_btn.clicked.connect(self.create_task_async)
        self.ui.query_btn.clicked.connect(self.query_tasks_async)
        self.ui.delete_btn.clicked.connect(self.delete_task_async)
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
                self.query_tasks_async()
            ))

    def save_credentials(self):
        """
        保存用户凭证到配置文件。
        """
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
        result = message
        try:
            # 尝试解析 message 获取 op_type 和 result
            parsed_op_type, result = eval(message)
            # 如果解析成功，使用解析后的 op_type
            op_type = parsed_op_type
        except Exception as e:
            logger.error(f"解析异步任务结果失败: {e}")
            QMessageBox.critical(self, "错误", f"解析异步任务结果失败: {e}")
            if op_type == "login":
                self.show_login_result(False, False)  # 强制标记登录失败
            self._restore_button_state(op_type)
            if op_type == "dislogin":
                self.show_dislogin_result(False, False)
            return

        try:
            if op_type == "login":
                self.show_login_result(success, result)
            elif op_type == "dislogin":
                self.show_dislogin_result(success, result)
            elif op_type == "exe_generation":
                self.handle_exe_generation_finished(success, result)
            elif op_type == "create_task":
                self.handle_create_task_result(success, result)
            elif op_type == "query_tasks":
                # 解包 query_tasks 返回的结果
                query_success, task_list = result
                self.handle_query_tasks_result(query_success, task_list)
            elif op_type == "delete_task":
                self.handle_delete_task_result(success, result)
        except Exception as e:
            logger.error(f"处理异步任务 {op_type} 结果失败: {e}")
            QMessageBox.critical(self, "错误", f"处理异步任务 {op_type} 结果失败: {e}")
            if op_type == "login":
                self.show_login_result(False, False)  # 强制标记登录失败
            self._restore_button_state(op_type)

    def _restore_button_state(self, op_type):
        """
        根据操作类型恢复对应按钮的启用状态。
        """
        if op_type == "login":
            self.ui.pushButton_login.setEnabled(True)
        elif op_type == "dislogin":
            self.ui.pushButton_dislogin.setEnabled(True)
        # 可以根据需要添加其他操作类型的按钮恢复逻辑

    def show_login_result(self, success, result):
        """
        显示登录结果信息。
        """
        if result:
            self.ui.label_green_message.setText("登录成功！")
            self.ui.stackedWidget_message.setCurrentIndex(1)
        else:
            self.ui.label_red_message.setText("登录失败！")
            self.ui.stackedWidget_message.setCurrentIndex(2)
        self.ui.pushButton_login.setEnabled(True)

    def show_dislogin_result(self, success, result):
        """
        显示登出结果信息。
        """
        if result:
            self.ui.label_green_message.setText("登出成功！")
            self.ui.stackedWidget_message.setCurrentIndex(1)
        else:
            self.ui.label_red_message.setText("登出失败")
            self.ui.stackedWidget_message.setCurrentIndex(2)
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
        setup_logger(username=username)
        # 传递操作类型作为参数
        self.task_executor.execute_task(
            lambda: ("login", networkmanager.login(username, password)),
            op_type="login"
        )
        self.save_credentials()

    def dislogin(self):
        """
        执行登出操作。
        """
        self.ui.stackedWidget_message.setCurrentIndex(0)
        self.ui.label_black_message.setText("下线中...")
        self.ui.pushButton_dislogin.setEnabled(False)

        username = self.ui.lineEdit_username.text()
        # 传递操作类型作为参数
        self.task_executor.execute_task(
            lambda: ("dislogin", networkmanager.dislogin(username)),
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

    def create_task_async(self):
        """
        异步创建计划任务。
        """
        file_path = self.ui.file_path_edit.text().strip()

        if not os.path.exists(file_path):
            QMessageBox.warning(self, "警告", "请选择有效的文件")
            logger.warning("请选择有效的文件")
            return

        self.task_executor.execute_task(
            lambda: ("create_task", self.task_manager.create_task(file_path))
        )

    def handle_create_task_result(self, success, result):
        """
        处理创建任务的结果。
        """
        if isinstance(result, tuple):
            create_success, file_name = result
        else:
            create_success, file_name = success, result

        if create_success:
            self.query_tasks_async()
            QMessageBox.information(
                self, "成功", f"计划任务 '{file_name}' 创建成功！")
            logger.info(f"计划任务'{file_name}'创建成功！")
        else:
            QMessageBox.critical(self, "错误", f"创建任务失败:\n{result}")
            logger.error(f"创建任务失败: {result}")

    def query_tasks_async(self):
        """
        异步查询计划任务。
        """
        self.task_executor.execute_task(
            lambda: ("query_tasks", self.task_manager.query_tasks())
        )

    def handle_query_tasks_result(self, success, result):
        """
        处理查询任务的结果。
        """
        if success:
            if not isinstance(result, list):
                logger.error(f"查询任务返回结果不是列表类型，实际类型: {type(result).__name__}，结果内容: {result}")
                QMessageBox.critical(
                    self, "错误", "查询任务返回结果格式错误")
                return
            self.update_task_list(result)
            if not result:
                QMessageBox.information(
                    self, "提示", "没有查询到匹配的任务")
        else:
            QMessageBox.critical(self, "错误", f"查询任务失败:\n{result}")
            logger.error(f"查询任务失败: {result}")

    def update_task_list(self, tasks: list):
        """
        更新任务列表显示。
        """
        try:
            self.ui.task_table.setRowCount(0)

            column_keys = {
                0: "name",
                1: "filepath",
                2: "status",
                3: "next_run"
            }

            for row, task in enumerate(tasks):
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

    def delete_task_async(self):
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
                lambda: ("delete_task", self.task_manager.delete_task(full_task_name))
            )

    def handle_delete_task_result(self, success, result):
        """
        处理删除任务的结果。
        """
        if isinstance(result, tuple):
            message = result[1] if len(result) > 1 else str(result)
        else:
            message = str(result)

        if success:
            self.query_tasks_async()
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.critical(self, "错误", f"删除任务失败:\n{message}")
            logger.error(f"删除任务失败: {message}")

    def create_exe(self):
        """
        生成自动登录的 EXE 文件。
        """
        username = self.ui.lineEdit_username.text().strip()
        password = self.ui.lineEdit_password.text().strip()

        # 输入验证
        if not username or not password:
            QMessageBox.critical(self, "错误", "请输入账号和密码")
            return

        try:
            # 确保任务文件夹存在
            self.task_manager.task_folder.mkdir(parents=True, exist_ok=True)
            script_dir = Path(__file__).parent.absolute()
            project_root = script_dir.parent.parent

            # 生成自动登录脚本，将脚本放在 task_folder 目录下
            auto_login_script = self._generate_auto_login_script(username, password)
            auto_login_script_path = self.task_manager.task_folder / "auto_login.py"
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
            generate_exe_with_cx_freeze(str(auto_login_script_path), exe_name, str(self.task_manager.task_folder))

            self.ui.pushButton_generate.setEnabled(True)
            self.ui.stackedWidget_message.setCurrentIndex(1)
            self.ui.label_green_message.setText("EXE文件生成成功...")

            # 构建 EXE 文件的完整路径
            exe_path = self.task_manager.task_folder / f"{exe_name}.exe"

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
            logger.error(
                f"生成EXE文件失败: {str(e)}, 错误详情: {getattr(e, 'stderr', '')}")
            QMessageBox.critical(self, "错误", f"生成EXE文件失败: {str(e)}")

    @staticmethod
    def _generate_auto_login_script(username, password):
        """
        生成自动登录脚本内容。
        """
        return f"""
import time
import sys
from pathlib import Path

# 确保正确获取项目根目录
if getattr(sys, 'frozen', False):
    # 打包后的环境，从临时解压目录获取路径
    base_path = Path(sys._MEIPASS)
else:
    # 开发环境，从代码文件位置获取路径
    base_path = Path(__file__).parent.parent.parent

# 动态构建模块路径
import sys
sys.path.insert(0, str(base_path / 'app'))
sys.path.insert(0, str(base_path / 'app' / 'core'))
sys.path.insert(0, str(base_path / 'app' / 'utils'))

from app.core.network import networkmanager
from app.utils.logger import logger, setup_logger

USERNAME = "{username}"
PASSWORD = "{password}"

def auto_login():
    setup_logger(username=USERNAME)
    try:
        result = networkmanager.login(USERNAME, PASSWORD)
        if result:
            print("登录成功！")
            logger.info("自动登录成功！")
        else:
            print("登录失败！")
            logger.error("自动登录失败！")
    except Exception as e:
        print(f"登录出错: {{str(e)}}")
        logger.error(f"自动登录出错: {{str(e)}}")

if __name__ == '__main__':
    try:
        auto_login()
    except Exception as e:
        print(f"程序运行出错: {{str(e)}}")
        logger.error(f"程序运行出错: {{str(e)}}")
    input("按回车键退出...")  # 保持终端打开，方便查看错误信息
            """

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

    def handle_exe_generation_finished(self, success, message):
        """
        处理 EXE 文件生成完成的结果。
        """
        self.ui.pushButton_generate.setEnabled(True)
        if success:
            self.ui.stackedWidget_message.setCurrentIndex(1)
            self.ui.label_green_message.setText("EXE文件生成成功...")

            # 构建 EXE 文件的完整路径
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

            # 自动清理 build 目录和 .spec 文件
            build_dir = self.task_manager.task_folder / "build"
            spec_file = self.task_manager.task_folder / f"{exe_name.replace('.exe', '')}.spec"
            if build_dir.exists():
                shutil.rmtree(build_dir)
            if spec_file.exists():
                spec_file.unlink()

            # 不删除 auto_login.py 脚本
            auto_login_script_path = self.task_manager.task_folder / "auto_login.py"
            if auto_login_script_path.exists():
                auto_login_script_path.unlink()

        else:
            logger.error(f"生成EXE文件失败: {message}")
            QMessageBox.critical(self, "错误", f"生成EXE文件失败: {message}")


def run():
    """
    启动主界面。
    """
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec())
