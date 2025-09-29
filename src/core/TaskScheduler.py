"""
任务管理模块，负责计划任务的创建、查询和删除。
"""
import os
import subprocess
from pathlib import Path
from src.utils.logger import logger
from PySide6.QtCore import QTime

if os.name == 'nt':
    try:
        CREATE_NO_WINDOW = 0x08000000
    except ImportError:
        CREATE_NO_WINDOW = 0

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
                "schtasks", "/Create", 
                "/TN", task_name,
                "/TR", file_path,
                "/SC", "DAILY",
                "/ST", time_str,
                "/F"
            ]

            # 添加creationflags参数来隐藏控制台窗口，不使用text=True避免编码问题
            subprocess.run(cmd, capture_output=True, check=True, 
                          creationflags=CREATE_NO_WINDOW if os.name == 'nt' else 0)
            return True, file_name
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode('cp936', errors='replace') if e.stderr else str(e)
            return False, err_msg
        except Exception as e:
            err_msg = str(e)
            return False, err_msg

    def query_tasks(self):
        """
        查询任务计划。
        """
        try:
            list_cmd = ["schtasks", "/Query", "/FO", "LIST", "/V"]
            
            # 在Windows系统上使用系统默认编码（通常是CP936或GBK）而不是强制使用UTF-8
            # 添加creationflags参数来隐藏控制台窗口
            task_names_list_result = subprocess.run(
                list_cmd, capture_output=True, shell=False, 
                creationflags=CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            # 解码输出，使用系统默认编码
            stdout = task_names_list_result.stdout.decode('cp936', errors='replace')

            if not stdout.strip():
                return True, []

            tasks = self._get_task_details(stdout)
            return True, tasks
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode('cp936', errors='replace') if e.stderr else str(e)
            return False, err_msg
        except Exception as e:
            err_msg = str(e)
            return False, err_msg


    def _get_task_details(self, task_text: str):
        """
        获取任务详细信息。
        """

        task_start = False
        tasks = []
        current_task = {
                "name": '',
                "next_run": '',
                "status": '',
                "filepath": ''
        }
        for line in task_text.split('\r\n'):
            line = line.strip()
            if line.startswith(("TaskName","任务名")):
                task_name = line.split(":", 1)[1].strip().replace("\\", "")
                if task_name.startswith(self.task_prefix):
                    task_start = True
                    original_name = task_name[len(self.task_prefix):]
                    current_task["name"] = original_name
                    continue
            elif line.startswith(("Next Run Time", "下次运行时间")) and task_start:
                next_run = line.split(":", 1)[1].strip()
                current_task["next_run"] = next_run
                continue
            elif line.startswith(("Status", "模式")) and task_start:
                status = line.split(":", 1)[1].strip()
                current_task["status"] = status
                continue
            elif line.startswith(("Task To Run", "要运行的任务")) and task_start:
                filepath = line.split(":", 1)[1].strip()
                current_task["filepath"] = filepath
                tasks.append(current_task)
                current_task = {
                    "name": '',
                    "next_run": '',
                    "status": '',
                    "filepath": ''
                }
                task_start = False
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
                cmd, capture_output=True, check=True,
                creationflags=CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            # 手动解码输出
            stdout = result.stdout.decode('cp936', errors='replace')
            logger.info(f"删除任务命令执行结果: {stdout}")  # 记录命令执行结果
            return True, "任务已删除！"
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.decode('cp936', errors='replace') if e.stderr else str(e)
            logger.error(f"删除任务失败，退出代码 {e.returncode}，错误信息: {err_msg}")
            return False, err_msg
        except Exception as e:
            err_msg = str(e)
            logger.error(f"删除任务时发生未知错误: {err_msg}")
            return False, err_msg
