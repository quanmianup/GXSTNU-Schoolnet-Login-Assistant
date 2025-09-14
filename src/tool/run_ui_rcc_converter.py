#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UI和QRC文件转换工具
用于同时将Qt Designer生成的.ui文件和.qrc资源文件转换为Python文件
"""

import os
import sys
import subprocess
from pathlib import Path


def find_project_root(current_dir):
    """查找项目根目录"""
    current_path = Path(current_dir)
    
    # 检查当前目录是否包含pyproject.toml
    if (current_path / "pyproject.toml").exists():
        return current_path
    
    # 获取父目录并递归搜索
    parent_path = current_path.parent
    if parent_path == current_path:  # 已到达根目录
        print("错误: 未找到pyproject.toml，无法确定项目根目录。")
        return None
    
    return find_project_root(str(parent_path))


def convert_file(tool_path, input_file, output_dir, output_suffix):
    """转换单个文件"""
    file_name = input_file.stem
    output_file = output_dir / f"{file_name}{output_suffix}.py"
    
    print(f"转换 {input_file} -> {output_file}")
    
    try:
        subprocess.run(
            [str(tool_path), "-o", str(output_file), str(input_file)],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"转换成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"转换失败: 错误代码 {e.returncode}, {e.stderr}")
        return False


def main():
    """主函数"""
    print("===== Qt UI和QRC文件转换工具 =====")
    
    # 查找项目根目录
    project_root = find_project_root(os.getcwd())
    if not project_root:
        sys.exit(1)
    
    # 设置工具和目录路径
    venv_scripts = project_root / ".venv" / "Scripts"
    uic_tool = venv_scripts / "pyside6-uic.exe"
    rcc_tool = venv_scripts / "pyside6-rcc.exe"
    qtfile_dir = project_root / "assets" / "qtfile"
    output_dir = project_root / "src" / "gui"
    
    # 检查工具是否存在
    if not uic_tool.exists() or not rcc_tool.exists():
        print("错误: 未找到PySide6工具，请确保PySide6已正确安装。")
        sys.exit(1)
    
    # 创建输出目录（如果不存在）
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 收集并转换文件
    success_count = 0
    fail_count = 0
    
    # 转换UI文件
    ui_files = list(qtfile_dir.glob("*.ui"))
    if ui_files:
        print(f"找到 {len(ui_files)} 个UI文件")
        for ui_file in ui_files:
            if convert_file(uic_tool, ui_file, output_dir, "_ui"):
                success_count += 1
            else:
                fail_count += 1
    
    # 转换QRC文件
    qrc_files = list(qtfile_dir.glob("*.qrc"))
    if qrc_files:
        print(f"找到 {len(qrc_files)} 个QRC文件")
        for qrc_file in qrc_files:
            if convert_file(rcc_tool, qrc_file, output_dir, "_rc"):
                success_count += 1
            else:
                fail_count += 1
    
    # 输出转换结果统计
    print("\n转换结果摘要:")
    print(f"成功: {success_count} 个文件")
    if fail_count > 0:
        print(f"失败: {fail_count} 个文件")
    
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()