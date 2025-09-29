import sys
import os
import shutil
import subprocess
from pathlib import Path

# Windows 终端颜色支持
class ConsoleColors:
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



# 清理临时文件
def clean_cache_files(build_dir, spec_file):
    """清理打包过程中生成的临时文件"""
    print(f"\n{ConsoleColors.GREEN}正在清理临时文件...{ConsoleColors.ENDC}")
    
    shutil.rmtree(build_dir)
    spec_file.unlink()

    print(f"{ConsoleColors.GREEN}临时文件清理完成。{ConsoleColors.ENDC}")

# 主打包函数
def invoke_packaging():
    """执行PyInstaller打包命令"""

    # 获取项目根目录（从当前脚本位置向上两级，因为脚本在src/tool目录下）
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.parent
    pyinstaller_path = shutil.which('pyinstaller')
    if not pyinstaller_path:
        print(f"{ConsoleColors.RED}错误：未找到pyinstaller可执行文件，请先安装pyinstaller：uv pip install pyinstaller{ConsoleColors.ENDC}")
        sys.exit(1)
    # 定义打包参数
    source_script = project_root / 'src' / 'core' / 'AutoLoginScript.py'
    dist_dir = project_root / 'dist'
    build_dir = project_root / 'build'
    spec_file = project_root / 'AutoLoginScript.spec'
    icon_file = project_root / 'assets' / 'images' / 'main_icon.ico'
    
    # 构建PyInstaller命令参数
    pyinstaller_args = [
        pyinstaller_path,
        '--onefile',              # 生成单个可执行文件
        '--console',              # 显示控制台窗口，用于输出日志
        '--name=AutoLoginScript', # 可执行文件名称
        '--log-level=WARN',
        '--icon', str(icon_file), # 设置应用图标（使用.ico格式）
        '--distpath', str(dist_dir),
        '--workpath', str(build_dir),
        # 添加隐藏的导入以确保所有依赖都被包含
        '--hidden-import=src.core.NetworkManager',
        '--hidden-import=src.utils.logger',
        '--hidden-import=requests',
        '--hidden-import=Crypto',
        '--hidden-import=loguru',
        str(source_script)
    ]
    
    print(f"{ConsoleColors.GREEN}正在使用PyInstaller打包: {source_script}{ConsoleColors.ENDC}")
    print(f"{ConsoleColors.YELLOW}命令: \n{' '.join(pyinstaller_args)}{ConsoleColors.ENDC}")
    
    try:
        # 切换到项目根目录执行命令
        original_dir = os.getcwd()
        os.chdir(str(project_root))
        print(f"{ConsoleColors.GREEN}正在打包中...{ConsoleColors.ENDC}")
        subprocess.run(pyinstaller_args, check=True)
        # 恢复原始目录
        os.chdir(original_dir)
        
        print(f"\n{ConsoleColors.GREEN}打包成功！可执行文件已生成在: {dist_dir / 'AutoLoginScript.exe'}{ConsoleColors.ENDC}")
        
        # 清理临时文件
        clean_cache_files(build_dir, spec_file)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"{ConsoleColors.RED}错误：打包过程中出现问题，错误代码: {e.returncode}{ConsoleColors.ENDC}")
        os.chdir(original_dir)  # 确保恢复目录
        return False
    except Exception as e:
        print(f"{ConsoleColors.RED}错误：打包过程中发生异常: {str(e)}{ConsoleColors.ENDC}")
        os.chdir(original_dir)  # 确保恢复目录
        return False

# 主函数
if __name__ == "__main__":
    print(f"{ConsoleColors.GREEN}GXSTNU校园网登录助手 - AutoLoginScript打包脚本{ConsoleColors.ENDC}")
    
    # 执行打包
    packaging_success = invoke_packaging()