"""
项目入口文件，启动主界面。
"""
import os
import sys

# ==========解决No module named 'window_rc'问题==================
# 将src/gui目录添加到Python搜索路径的前面
project_root = os.path.dirname(os.path.abspath(__file__))
src_gui_path = os.path.join(project_root, 'src', 'gui')
# 插入到搜索路径的最前面，确保优先查找
if src_gui_path not in sys.path:
    sys.path.insert(0, src_gui_path)
if project_root not in sys.path:
    sys.path.append(project_root)
# ==============================================================

from src.gui.main_gui_program import run


if __name__ == '__main__':
    run()
    