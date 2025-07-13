import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from PyQt5.QtCore import pyqtSignal, QObject, QTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem

from app.core.test_network import networkmanager
from app.core.task_scheduler import schedule_login
from app.utils.logger import logger, setup_logger
from config.credentials import credentials
from main_ui import *


class AsyncTaskExecutor(QObject):
    finished = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.thread_pool = ThreadPoolExecutor(max_workers=5)

    def execute_task(self, task, *args):
        future = self.thread_pool.submit(self._run_task, task, *args)
        future.add_done_callback(lambda _: self._handle_future_result(future))

    @staticmethod
    def _run_task(task, *args):
        try:
            result = task(*args)
            return True, str(result)
        except Exception as e:
            return False, str(e)

    def _handle_future_result(self, future):
        try:
            success, message = future.result()
            self.finished.emit(success, message)
        except Exception as e:
            pass  # 静默处理异常


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.time_edit.setTime(QTime.currentTime())
        self.ui.lineEdit_username.setText(credentials.get('username', ''))
        self.ui.lineEdit_password.setText(credentials.get('password', ''))
        self.ui.checkBox.setChecked(True)

        self.TASK_PREFIX = "FileScheduler_"
        self.task_folder = os.path.join(os.environ['SYSTEMDRIVE'], "ScheduledTasks")
        os.makedirs(self.task_folder, exist_ok=True)

        self.ui.select_file_btn.clicked.connect(self.select_file)
        self.ui.create_btn.clicked.connect(self.create_task)
        self.ui.query_btn.clicked.connect(self.query_tasks)
        self.ui.delete_btn.clicked.connect(self.delete_task)

        self.task_list = []
        self.task_executor = AsyncTaskExecutor()
        self.task_executor.finished.connect(self.show_result)

        self.ui.pushButton_login.clicked.connect(self.login)
        self.ui.pushButton_dislogin.clicked.connect(self.dislogin)
        self.ui.pushButton_tab_main.clicked.connect(lambda: self.ui.stackedWidget_tab.setCurrentIndex(0))
        self.ui.pushButton_tab_manege.clicked.connect(lambda: (
            self.ui.stackedWidget_tab.setCurrentIndex(1),
            self.query_tasks()
        ))

    def save_credentials(self):
        if self.ui.checkBox.isChecked():
            credentials.set('username', self.ui.lineEdit_username.text().strip())
            credentials.set('password', self.ui.lineEdit_password.text().strip())
        else:
            credentials.set('username', '')
            credentials.set('password', '')

    def show_result(self, success, message):
        try:
            op_type, result = eval(message)
        except:
            op_type, result = "unknown", message

        status_map = {
            "login": ("登录成功！", "登录失败！", self.ui.pushButton_login),
            "dislogin": ("登出成功！", "登出失败", self.ui.pushButton_dislogin)
        }

        if op_type in status_map:
            success_text, fail_text, button = status_map[op_type]
            if result:
                self.ui.label_green_message.setText(success_text)
                self.ui.stackedWidget_message.setCurrentIndex(1)
            else:
                self.ui.label_red_message.setText(fail_text)
                self.ui.stackedWidget_message.setCurrentIndex(2)
            button.setEnabled(True)

    def generate_exe(self):
        try:
            subprocess.run([
                "pyinstaller", "--onefile", "--name=autologin",
                "--distpath=dist", "scripts/autologin.py"
            ], check=True)
            QtWidgets.QMessageBox.information(self, "成功", "EXE已生成在dist目录")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", f"生成失败: {str(e)}")

    def enable_schedule(self):
        exe_path = os.path.abspath("dist/autologin.exe")
        if not os.path.exists(exe_path):
            QtWidgets.QMessageBox.warning(self, "警告", "请先生成EXE文件")
            return

        try:
            schedule_login(
                trigger_time=self.time_edit.time().toString("HH:mm"),
                exe_path=exe_path
            )
            QtWidgets.QMessageBox.information(self, "成功", "定时任务已创建")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", f"任务创建失败: {str(e)}")

    def login(self):
        self.ui.stackedWidget_message.setCurrentIndex(0)
        self.ui.label_black_message.setText("登录中...")
        self.ui.pushButton_login.setEnabled(False)

        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()
        setup_logger(username=username)
        self.task_executor.execute_task(
            lambda: ("login", networkmanager.login(username, password))
        )
        self.save_credentials()

    def dislogin(self):
        self.ui.stackedWidget_message.setCurrentIndex(0)
        self.ui.label_black_message.setText("下线中...")
        self.ui.pushButton_dislogin.setEnabled(False)

        username = self.ui.lineEdit_username.text()
        self.task_executor.execute_task(
            lambda: ("dislogin", networkmanager.dislogin(username))
        )
        self.save_credentials()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择要执行的文件", "", "所有文件 (*.*)"
        )

        if file_path:
            self.ui.file_path_edit.setText(file_path)
            file_name = os.path.basename(file_path)
            self.ui.task_name_label.setText(file_name)

    def create_task(self):
        file_path = self.ui.file_path_edit.text().strip()

        if not os.path.exists(file_path):
            QMessageBox.warning(self, "警告", "请选择有效的文件")
            logger.warning("请选择有效的文件")
            return

        file_name = os.path.basename(file_path)
        task_name = f"{self.TASK_PREFIX}{file_name}"
        try:
            time_str = self.ui.time_edit.time().toString("HH:mm:ss")
            cmd = [
                "schtasks", "/Create", "/TN", task_name,
                "/TR", file_path,
                "/SC", "DAILY",
                "/ST", time_str,
                "/F"
            ]

            subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.query_tasks()
            QMessageBox.information(self, "成功", f"计划任务 '{file_name}' 创建成功！")
            logger.info(f"计划任务'{file_name}'创建成功！")

        except Exception as e:
            err_msg = e.stderr if isinstance(e, subprocess.CalledProcessError) else str(e)
            QMessageBox.critical(self, "错误", f"创建任务失败:\n{err_msg}")
            logger.error(f"创建任务失败: {err_msg}")

    def query_tasks(self):
        try:
            list_cmd = ["schtasks", "/Query", "/FO", "LIST"]
            filter_cmd = ["findstr", f"^{self.TASK_PREFIX}"]
            full_cmd = " ".join(map(lambda x: f'"{x}"' if " " in x else x, list_cmd)) + " | " + " ".join(
                map(lambda x: f'"{x}"' if " " in x else x, filter_cmd))

            task_names_list_result = subprocess.run(full_cmd, capture_output=True, text=True, shell=True)

            if not task_names_list_result.stdout.strip():
                self.update_task_list([])
                QMessageBox.information(self, "提示", "没有查询到匹配的任务")
                return

            task_names = []
            for line in task_names_list_result.stdout.strip().split('\n'):
                if line.startswith(("任务名:", "TaskName:")):
                    task_name = line.split(":", 1)[1].strip().lstrip('\\')
                    task_names.append(task_name)

            tasks = []
            for task_name in task_names:
                detail_cmd = ["schtasks", "/Query", "/TN", task_name, "/V", "/FO", "LIST"]
                detail_result = subprocess.run(detail_cmd, capture_output=True, text=True, check=True)

                next_run = status = filepath = "N/A"
                for detail_line in detail_result.stdout.strip().split('\n'):
                    if detail_line.startswith(("Next Run Time:", "下次运行时间")):
                        next_run = detail_line.split(":", 1)[1].strip()
                    elif detail_line.startswith(("Status:", "模式")):
                        status = detail_line.split(":", 1)[1].strip()
                    elif detail_line.startswith(("Actions:", "要运行的任务")):
                        filepath = detail_line.split(":", 1)[1].strip()

                original_name = task_name[len(self.TASK_PREFIX):]
                tasks.append({
                    "name": original_name,
                    "next_run": next_run,
                    "status": status,
                    "filepath": filepath
                })

            self.update_task_list(tasks)
        except Exception as e:
            err_msg = e.stderr if isinstance(e, subprocess.CalledProcessError) else str(e)
            QMessageBox.critical(self, "错误", f"查询任务失败:\n{err_msg}")
            logger.error(f"查询任务失败: {err_msg}")

    def update_task_list(self, tasks: list):
        try:
            self.ui.task_table.setRowCount(0)
            self.ui.task_table.setColumnCount(4)
            self.ui.task_table.setHorizontalHeaderLabels(["任务名称", "文件路径", "状态", "下次运行时间"])
            self.ui.task_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            COLUMN_KEYS = {
                0: "name",
                1: "filepath",
                2: "status",
                3: "next_run"
            }

            for row, task in enumerate(tasks):
                self.ui.task_table.insertRow(row)
                for col, key in COLUMN_KEYS.items():
                    item = QTableWidgetItem(task[key])
                    item.setToolTip(task[key])
                    self.ui.task_table.setItem(row, col, item)

            self.ui.task_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"更新任务列表失败:\n{str(e)}")
            logger.error(f"更新任务列表失败: {str(e)}")

    def delete_task(self):
        selected_items = self.ui.task_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请先选择要删除的任务")
            return

        original_name = selected_items[0].text()
        full_task_name = f"{self.TASK_PREFIX}{original_name}"

        if QMessageBox.Yes == QMessageBox.question(
            self, "确认删除",
            f"确定要删除任务 '{original_name}' 吗？",
            QMessageBox.Yes | QMessageBox.No
        ):
            try:
                cmd = ["schtasks", "/Delete", "/TN", full_task_name, "/F"]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                self.query_tasks()
                QMessageBox.information(self, "成功", "任务已删除！")
            except Exception as e:
                err_msg = e.stderr if isinstance(e, subprocess.CalledProcessError) else str(e)
                QMessageBox.critical(self, "错误", f"删除任务失败:\n{err_msg}")


def run():
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    run()
