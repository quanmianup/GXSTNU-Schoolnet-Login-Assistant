#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
主程序打包工具

此脚本用于将校园网登录助手主程序(run.py)打包为可执行文件(.exe)，使用PyInstaller工具进行打包。
打包过程会自动生成并包含AutoLoginScript.exe作为内部资源，确保程序的完整功能。

依赖项:
- pyinstaller: 用于将Python脚本打包为可执行文件
- PySide6: GUI框架
- uv: 推荐使用的Python包管理器

使用说明:
1. 确保已激活虚拟环境
2. 安装pyinstaller: uv pip install pyinstaller
3. 运行此脚本: python build_main_ui.py
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

# Windows 终端颜色支持
class ConsoleColors:
    """终端颜色常量类，用于在控制台输出彩色文本"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'  # 重置颜色

# 确保在Windows上启用ANSI颜色支持
if os.name == 'nt':
    os.system('color')  # 启用cmd的颜色支持

# 确保在虚拟环境中运行
if not hasattr(sys, 'base_prefix') or sys.base_prefix == sys.prefix:
    print(f"{ConsoleColors.YELLOW}警告：建议在虚拟环境中运行此打包脚本。{ConsoleColors.ENDC}")

# 获取项目根目录（从当前脚本位置向上两级，因为脚本在src/tool目录下）
script_dir = Path(__file__).parent.resolve()
project_root = script_dir.parent.parent
ProjectName = "GXSTNU-Schoolnet-Login-Assistant"
SourceScript = project_root / 'run.py'
DistDir = project_root / 'dist'
BuildDir = project_root / 'build'
SpecFile = project_root / f'{ProjectName}.spec'
IconFile = project_root / 'assets' / 'images' / 'main_icon.ico'
AutoLoginScriptExe = DistDir / 'AutoLoginScript.exe'
build_auto_login_script = project_root / 'src' / 'tool' / 'build_auto_login.py'


def check_pyinstaller():
    """检查pyinstaller是否已安装

    返回:
        str: pyinstaller可执行文件的路径
        
    异常:
        SystemExit: 如果未找到pyinstaller，程序将退出
    """
    pyinstaller_path = shutil.which('pyinstaller')
    if not pyinstaller_path:
        print(f"{ConsoleColors.RED}错误：未找到pyinstaller可执行文件，请先安装pyinstaller：uv pip install pyinstaller{ConsoleColors.ENDC}")
        sys.exit(1)
    return pyinstaller_path


def generate_auto_login_script():
    """生成AutoLoginScript.exe（如果不存在）
    该程序用于实现网络保活功能的定时任务。

    返回:
        bool: AutoLoginScript.exe是否生成成功或已存在
    """
    # 检查并确保AutoLoginScript.exe存在
    if not AutoLoginScriptExe.exists():
        print(f"{ConsoleColors.RED}AutoLoginScript.exe未找到，正在生成...{ConsoleColors.ENDC}")
        if build_auto_login_script.exists():
            try:
                # 运行build_auto_login.py来生成AutoLoginScript.exe
                print(f"{ConsoleColors.YELLOW}运行脚本: {build_auto_login_script}{ConsoleColors.ENDC}")
                subprocess.run([sys.executable, str(build_auto_login_script)], check=True, cwd=str(project_root))
                
                if AutoLoginScriptExe.exists():
                    print(f"{ConsoleColors.GREEN}AutoLoginScript.exe生成成功。{ConsoleColors.ENDC}")
                    return True
                else:
                    print(f"{ConsoleColors.RED}生成AutoLoginScript.exe失败{ConsoleColors.ENDC}")
                    return False
            except subprocess.CalledProcessError as e:
                print(f"{ConsoleColors.RED}错误：生成AutoLoginScript.exe时出现问题，错误代码: {e.returncode}{ConsoleColors.ENDC}")
                return False
            except Exception as e:
                print(f"{ConsoleColors.RED}错误：生成AutoLoginScript.exe时发生异常: {str(e)}{ConsoleColors.ENDC}")
                return False
        else:
            print(f"{ConsoleColors.RED}错误：build_auto_login.py脚本未找到。{ConsoleColors.ENDC}")
            return False
    else:
        return True


def clean_cache_files():
    """清理打包过程中生成的临时文件
    包括build目录和.spec配置文件
    """
    print(f"\n{ConsoleColors.GREEN}正在清理临时文件...{ConsoleColors.ENDC}")
    try:
        shutil.rmtree(BuildDir, ignore_errors=True)
    except Exception as e:
        print(f"{ConsoleColors.YELLOW}警告：删除build目录时出错: {str(e)}{ConsoleColors.ENDC}")
    
    try:
        SpecFile.unlink()
    except Exception as e:
        print(f"{ConsoleColors.YELLOW}警告：删除spec文件时出错: {str(e)}{ConsoleColors.ENDC}")
    
    print(f"{ConsoleColors.GREEN}临时文件清理完成。{ConsoleColors.ENDC}")


def invoke_packaging():
    """执行PyInstaller打包命令，将主程序打包为单个可执行文件

    返回:
        bool: 打包是否成功完成
    """
    pyinstaller_path = check_pyinstaller()

    # 确保pyproject.toml文件存在
    pyproject_file = project_root / 'pyproject.toml'
    if not pyproject_file.exists():
        print(f"{ConsoleColors.RED}错误：未找到pyproject.toml文件，请确保该文件存在于项目根目录。{ConsoleColors.ENDC}")
        sys.exit(1)

    # 构建PyInstaller命令参数，包括AutoLoginScript.exe作为外部资源
    pyinstaller_args = [
        pyinstaller_path,
        '--onefile',             # 生成单个可执行文件
        '--windowed',            # 不显示控制台窗口（GUI应用程序）
        f'--name={ProjectName}', # 可执行文件名称
        f'--icon={IconFile}',    # 设置应用图标
        f'--distpath={DistDir}',
        f'--workpath={BuildDir}',
        '--log-level=WARN',
        '--clean',              # 清理PyInstaller缓存
        # 使用--add-data参数包含AutoLoginScript.exe作为外部资源
        f'--add-data={str(AutoLoginScriptExe)};.',
        f'--add-data={str(pyproject_file)};.',
        # 添加隐藏的导入以确保所有依赖都被包含
        '--hidden-import=src.core.NetworkManager',
        '--hidden-import=src.utils.logger',
        '--hidden-import=src.core.TaskScheduler',
        '--hidden-import=src.core.Credentials',
        '--hidden-import=src.gui.main_gui_program',
        '--hidden-import=src.gui.main_ui',
        '--hidden-import=src.gui.window_rc',
        '--hidden-import=PySide6',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=requests',
        '--hidden-import=Crypto',
        '--hidden-import=loguru',
        str(SourceScript)
    ]
    
    print(f"{ConsoleColors.GREEN}正在使用PyInstaller打包: {SourceScript}{ConsoleColors.ENDC}")
    print(f"{ConsoleColors.YELLOW}命令: {' '.join(pyinstaller_args)}{ConsoleColors.ENDC}")
    
    try:
        # 切换到项目根目录执行命令
        original_dir = os.getcwd()
        os.chdir(str(project_root))
        
        subprocess.run(pyinstaller_args, check=True)
        
        # 恢复原始目录
        os.chdir(original_dir)
        
        print(f"\n{ConsoleColors.GREEN}打包成功！可执行文件已生成在: {os.path.join(str(DistDir), f'{ProjectName}.exe')}{ConsoleColors.ENDC}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{ConsoleColors.RED}打包失败，退出代码: {e.returncode}{ConsoleColors.ENDC}")
        os.chdir(original_dir)  # 确保恢复目录
        return False
    except Exception as e:
        print(f"{ConsoleColors.RED}错误：打包过程中发生异常: {str(e)}{ConsoleColors.ENDC}")
        os.chdir(original_dir)  # 确保恢复目录
        return False

# 主函数
if __name__ == "__main__":
    """主程序入口，协调整个打包流程
    1. 检查并生成AutoLoginScript.exe
    2. 执行主程序打包
    3. 清理临时文件
    """
    print(f"{ConsoleColors.GREEN}GXSTNU校园网登录助手 - 主程序打包脚本{ConsoleColors.ENDC}")
    
    # 检查并生成AutoLoginScript.exe
    auto_login_generated = generate_auto_login_script()
    
    if auto_login_generated:
        # 执行打包
        packaging_success = invoke_packaging()
        
        # 如果打包成功，清理缓存文件
        if packaging_success:
            clean_cache_files()