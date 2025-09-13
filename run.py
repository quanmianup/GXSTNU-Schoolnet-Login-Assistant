"""
项目入口文件，启动主界面。
"""
import os
import sys

from src.gui.main_gui_program import run

# ==========解决No module named 'window_rc'问题==================
# 将src/gui目录添加到Python搜索路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_gui_path = os.path.join(project_root, 'src', 'gui')
sys.path.append(project_root, src_gui_path)
# ==============================================================

if __name__ == '__main__':
    run()
    