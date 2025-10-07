#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目主入口文件
负责启动图形界面程序并设置必要的环境
"""
import sys
import os

# ==========解决No module named 'window_rc'问题==================
# 将src/gui目录添加到Python搜索路径的前面
project_root = os.path.dirname(os.path.abspath(__file__))
src_gui_path = os.path.join(project_root, 'src', 'gui')
# 插入到搜索路径的最前面，确保优先查找
if src_gui_path not in sys.path:
    sys.path.insert(0, src_gui_path)
# ==============================================================

# 导入主程序运行函数
from src.gui.main_gui_program import run

if __name__ == "__main__":
    """
    程序主入口
    
    功能说明：
    1. 设置项目路径，确保可以正确导入所有模块
    2. 从主界面程序模块导入run函数
    3. 调用run函数启动GUI应用程序
    
    注意事项：
    - 该文件是项目的主要入口点
    - 通过命令行运行此文件将启动完整的GUI界面
    - 确保项目的所有依赖包已正确安装
    """
    run()
    