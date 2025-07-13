import os
import subprocess


def schedule_login(task_name="CampusNetworkAutoLogin",
                   exe_path="dist/autologin.exe",
                   trigger_time="08:00"):
    """创建Windows计划任务"""
    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"EXE文件不存在: {exe_path}")

    cmd = f'schtasks /create /tn "{task_name}" /tr "{os.path.abspath(exe_path)}" /sc DAILY /st {trigger_time} /f'
    subprocess.run(cmd, shell=True, check=True)


def unschedule_login(task_name="CampusNetworkAutoLogin"):
    """删除计划任务"""
    cmd = f'schtasks /delete /tn "{task_name}" /f'
    subprocess.run(cmd, shell=True)
