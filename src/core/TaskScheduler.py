"""
任务管理模块，负责计划任务的创建、查询和删除。
"""
import os
import subprocess
from pathlib import Path
from src.utils.logger import logger
from PySide6.QtCore import QTime

class TaskScheduler:
    """
    任务计划管理类，封装计划任务的创建、查询和删除操作。
    """
    def __init__(self):
        self.task_prefix = "FileScheduler_"
        self.task_folder = Path(os.environ['SYSTEMDRIVE'], os.sep, "ScheduledTasks").resolve()

    def get_full_task_name(self, original_name):
        """
        根据原始文件名生成完整的任务名称。
        """
        return f"{self.task_prefix}{original_name}"

    def create_task(self, file_path):
        """
        创建计划任务。
        """
        file_name = os.path.basename(file_path)
        task_name = self.get_full_task_name(file_name)
        try:
            time_str = QTime.currentTime().toString("HH:mm:ss")
            cmd = [
                "schtasks", "/Create", "/TN", task_name,
                "/TR", file_path,
                "/SC", "DAILY",
                "/ST", time_str,
                "/F"
            ]

            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True, file_name
        except Exception as e:
            err_msg = e.stderr if isinstance(e, subprocess.CalledProcessError) else str(e)
            return False, err_msg

    def query_tasks(self):
        """
        查询任务计划。
        """
        try:
            list_cmd = ["schtasks", "/Query", "/FO", "LIST"]
            filter_cmd = ["findstr", f"^{self.task_prefix}"]
            # 在 Windows 系统下使用 shell 来执行管道命令
            full_cmd = " ".join(
                map(lambda x: f'"{x}"' if " " in x else x, list_cmd)) + " | " + " ".join(
                map(lambda x: f'"{x}"' if " " in x else x, filter_cmd))

            task_names_list_result = subprocess.run(
                full_cmd, capture_output=True, text=True, shell=True, encoding='utf8')

            if not task_names_list_result.stdout.strip():
                return True, []

            task_names = self._parse_task_names(task_names_list_result.stdout)
            tasks = self._get_task_details(task_names)
            return True, tasks
        except Exception as e:
            err_msg = e.stderr if isinstance(e, subprocess.CalledProcessError) else str(e)
            return False, err_msg

    @staticmethod
    def _parse_task_names(output):
        """
        解析任务名称。
        """
        task_names = []
        for line in output.strip().split('\n'):
            if line.startswith(("任务名:", "TaskName:")):
                task_name = line.split(":", maxsplit = 1)[1].strip().lstrip('\\')
                task_names.append(task_name)
        return task_names

    def _get_task_details(self, task_names):
        """
        获取任务详细信息。
        """
        tasks = []
        for task_name in task_names:
            detail_cmd = ["schtasks", "/Query", "/TN", task_name, "/V", "/FO", "LIST"]
            detail_result = subprocess.run(
                detail_cmd, capture_output=True, text=True, shell=True, encoding='utf8')
            stdout_content = detail_result.stdout
            if detail_result.stdout is None:
                return tasks
            next_run = status = filepath = "N/A"
            for detail_line in stdout_content.strip().split('\n'):
                if detail_line.startswith(("Next Run Time:", "下次运行时间")):
                    next_run = detail_line.split(":", 1)[1].strip()
                elif detail_line.startswith(("Status:", "模式")):
                    status = detail_line.split(":", 1)[1].strip()
                elif detail_line.startswith(("Actions:", "要运行的任务", "Task To Run:")):
                    filepath = detail_line.split(":", 1)[1].strip()

            original_name = task_name[len(self.task_prefix):]
            tasks.append({
                "name": original_name,
                "next_run": next_run,
                "status": status,
                "filepath": filepath
            })
        return tasks

    @staticmethod
    def delete_task(full_task_name):
        """
        删除计划任务。
        """
        try:
            cmd = ["schtasks", "/Delete", "/TN", full_task_name, "/F"]
            logger.info(f"执行删除任务命令: {' '.join(cmd)}")  # 记录执行的命令
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True)
            logger.info(f"删除任务命令执行结果: {result.stdout}")  # 记录命令执行结果
            return True, "任务已删除！"
        except subprocess.CalledProcessError as e:
            err_msg = f"删除任务失败，退出代码 {e.returncode}，错误信息: {e.stderr}"
            logger.error(err_msg)
            return False, err_msg
        except Exception as e:
            err_msg = str(e)
            logger.error(f"删除任务时发生未知错误: {err_msg}")
            return False, err_msg
