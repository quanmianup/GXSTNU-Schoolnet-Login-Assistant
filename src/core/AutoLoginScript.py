#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动登录脚本，用于无人值守环境下自动登录校园网
该脚本会尝试多次登录操作，直到成功或达到最大尝试次数
"""
import os
import sys
import time

# 设置项目根目录路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入网络管理模块
from src.core.NetworkManager import networkmanager

if __name__ == "__main__":
    """
    主程序入口，实现校园网自动登录功能
    
    功能说明：
    1. 导入必要的模块和网络管理器实例
    2. 尝试执行登录操作，最多尝试5次
    3. 每次尝试间隔1秒
    4. 登录成功后立即退出循环
    
    注意事项：
    - 该脚本需要配合已保存的凭证使用
    - 通常作为计划任务或开机启动项运行
    - 如需修改尝试次数和间隔时间，可以调整下方代码中的参数
    """
    # 最大尝试登录次数
    max_attempts = 5
    # 尝试间隔时间（秒）
    attempt_interval = 1
    
    for i in range(max_attempts):
        try:
            # 执行登录操作
            # 注意：这里使用的是默认凭证，需要提前通过主程序保存
            login_result = networkmanager.login()
            
            # 检查登录是否成功
            if isinstance(login_result, tuple) and login_result[0]:
                # 登录成功，退出循环
                break
        except Exception as e:
            # 捕获异常，继续下一次尝试
            pass
        
        # 如果不是最后一次尝试，则等待一段时间后再试
        if i < max_attempts - 1:
            time.sleep(attempt_interval)
