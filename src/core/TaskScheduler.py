#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
校园网登录助手 - 任务调度模块

该模块负责管理Windows计划任务，提供任务的创建、查询和删除功能。
主要用于实现程序的开机自启动功能，支持将校园网登录助手设置为开机自动运行。

核心功能：
- 创建开机自启动计划任务
- 查询当前已创建的计划任务列表
- 删除指定的计划任务
- 获取任务的完整路径名称

依赖项：
- os, subprocess: 用于执行Windows命令和文件操作
- re: 用于解析命令输出结果
- logging: 日志记录
- datetime: 日期时间处理
- pathlib.Path: 跨平台路径处理

使用示例：
```python
# 获取任务管理器实例
from src.core.TaskScheduler import task_manager

# 创建开机自启动任务
success, message = task_manager.create_task("F:/code/py/schoolnet/src/main_gui_program.py")
if success:
    print(f"任务创建成功: {message}")
else:
    print(f"任务创建失败: {message}")

# 查询所有任务
result = task_manager.query_tasks()
if isinstance(result, list):
    print(f"共查询到 {len(result)} 个任务")
    for task in result:
        print(f"任务名称: {task['OriginalName']}, 状态: {task.get('Status', '未知')}")

# 删除任务
full_task_name = task_manager.get_full_task_name("main_gui_program.py")
success, message = task_manager.delete_task(full_task_name)
print(message)
```
"""
import os
import subprocess
import logging
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
    Windows计划任务管理类
    提供创建、查询和删除计划任务的功能，主要用于实现程序的开机自启动
    
    属性：
    - task_folder_name: 计划任务在Windows任务计划程序中的文件夹名称
    - task_folder: 程序相关文件在用户文档目录下的存储路径
    """
    
    def __init__(self):
        """
        初始化TaskScheduler实例
        
        参数：
            task_folder_name (str): 计划任务文件夹名称，默认为"GXSTNU_Schoolnet_Tasks"
        """
        self.task_prefix = "FileScheduler_"
        self.task_folder = Path(os.environ['SYSTEMDRIVE'], os.sep, "ScheduledTasks").resolve()
 
    def get_full_task_name(self, original_name):
        """
        获取任务的完整名称（包含路径）
        
        参数：
            original_name (str): 原始任务名称（不包含路径）
        
        返回：
            str: 任务的完整名称
        
        """
        return f"{self.task_prefix}{original_name}"
    
    def create_task(self, file_path):
        """
        创建计划任务，设置为开机自动执行指定文件
        
        参数：
            file_path (str): 要执行的文件路径
        
        返回：
            tuple: (bool, str) - 第一个元素表示操作是否成功，第二个元素是结果消息
        
        异常：
            Exception: 当创建任务过程中出现错误时
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
        查询所有计划任务
        
        返回：
            tuple or list: 如果查询成功，返回任务列表；如果失败，返回(失败标志, 错误消息)
            任务列表中的每个元素是包含任务信息的字典，包含OriginalName等键
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
    
    @staticmethod
    def delete_task(full_task_name):
        """
        删除计划任务
        
        参数：
            task_name (str): 要删除的任务名称，包含完整路径
        
        返回：
            tuple: (bool, str) - 第一个元素表示操作是否成功，第二个元素是结果消息
        
        示例：
            >>> task_scheduler = TaskScheduler()
            >>> full_task_name = task_scheduler.get_full_task_name("script.py")
            >>> success, message = task_scheduler.delete_task(full_task_name)
            >>> print(message)
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
    

    def _get_task_details(self, task_text: str):
        """
        解析任务查询输出，提取任务详细信息
        
        参数：
            task_output (str): 任务查询命令的输出结果
        
        返回：
            list: 任务详细信息列表，每个元素是包含任务信息的字典
        
        说明：
            该方法会从SchTasks命令的输出中解析出任务的各项属性，并添加OriginalName字段表示原始文件名
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



# 创建TaskScheduler全局实例，供其他模块直接使用
# 使用方式：from src.core.TaskScheduler import task_manager
task_manager = TaskScheduler()
