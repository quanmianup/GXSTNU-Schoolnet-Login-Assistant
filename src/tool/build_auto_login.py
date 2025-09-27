import os
import sys
import shutil
from pathlib import Path

# 确保在虚拟环境中运行
if not hasattr(sys, 'base_prefix') or sys.base_prefix == sys.prefix:
    print("警告：建议在虚拟环境中运行此打包脚本。")

# 获取项目根目录（从当前脚本位置向上两级，因为脚本在src/tool目录下）
script_dir = Path(__file__).parent.resolve()
project_root = script_dir.parent.parent

# 获取PyInstaller可执行文件路径
pyinstaller_path = shutil.which('pyinstaller')
if not pyinstaller_path:
    print("错误：未找到pyinstaller可执行文件，请先安装pyinstaller：pip install pyinstaller")
    sys.exit(1)

# 定义打包参数
source_script = project_root / 'src' / 'core' / 'AutoLoginScript.py'
dist_dir = project_root / 'dist'
build_dir = project_root / 'build'
spec_file = project_root / 'AutoLoginScript.spec'

# 确保输出目录存在
dist_dir.mkdir(parents=True, exist_ok=True)

# 构建PyInstaller命令参数
pyinstaller_args = [
    pyinstaller_path,
    '--onefile',              # 生成单个可执行文件
    '--console',              # 显示控制台窗口，用于输出日志
    '--name=AutoLoginScript', # 可执行文件名称
    '--icon', str(project_root / 'assets' / 'images' / 'main_icon.ico'), # 设置应用图标（使用.ico格式）
    '--distpath', str(dist_dir),
    '--workpath', str(build_dir),
    # 添加隐藏的导入以确保所有依赖都被包含
    '--hidden-import=src.core.NetworkManager',
    '--hidden-import=src.utils.logger',
    '--hidden-import=requests',
    '--hidden-import=pycryptodome',
    '--hidden-import=loguru',
    str(source_script)
]

print(f"正在使用PyInstaller打包...")
print(f"命令: {' '.join(pyinstaller_args)}")

# 执行PyInstaller命令
try:
    import subprocess
    subprocess.run(pyinstaller_args, check=True)
    print(f"\n打包成功！可执行文件已生成在: {dist_dir}")
    print("注意：运行生成的exe文件时，控制台会显示日志输出。")
    
    # 清理临时文件
    print("\n正在清理临时文件...")
    
    # 删除build目录
    if build_dir.exists() and build_dir.is_dir():
        print(f"删除build目录: {build_dir}")
        shutil.rmtree(build_dir)
    
    # 删除spec文件
    if spec_file.exists() and spec_file.is_file():
        print(f"删除spec文件: {spec_file}")
        spec_file.unlink()
    
    print("临时文件清理完成。")
    

except subprocess.CalledProcessError as e:
    print(f"错误：打包过程中出现问题，错误代码: {e.returncode}")
    sys.exit(1)
except Exception as e:
    print(f"错误：打包过程中发生异常: {str(e)}")
    sys.exit(1)