import os
import subprocess
import shutil
import json
from datetime import datetime

# 项目路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
MAIN_SCRIPT = os.path.join(PROJECT_ROOT, 'run.py')
DIST_DIR = os.path.join(PROJECT_ROOT, 'dist')
BUILD_DIR = os.path.join(PROJECT_ROOT, 'build')
SPEC_FILE = os.path.join(PROJECT_ROOT, 'schoolnet.spec')

# 版本信息
VERSION_INFO = {
    "version": "1.0.0",
    "build_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "author": "YourName"
}

# 图标路径（可选）
ICON_PATH = os.path.join(PROJECT_ROOT, 'resources', 'icon.ico')


def create_version_file():
    version_path = os.path.join(PROJECT_ROOT, 'config', 'version.json')
    with open(version_path, 'w') as f:
        json.dump(VERSION_INFO, f, indent=2)
    print("✅ 版本信息已写入 config/version.json")


def build_executable():
    # 构建命令
    cmd = [
        'pyinstaller',
        MAIN_SCRIPT,
        '--name=schoolnet',
        '--clean',
        '--noconfirm',
        '--windowed',  # 不显示控制台窗口（适用于 GUI 应用）
        '--add-data', f'{os.path.join(PROJECT_ROOT, "config")};config',
        '--add-data', f'{os.path.join(PROJECT_ROOT, "resources")};resources',
        '--hidden-import=cryptography.hazmat.backends.openssl.backend'
    ]

    if os.path.exists(ICON_PATH):
        cmd.extend(['--icon', ICON_PATH])

    print("📦 正在构建可执行文件...")
    subprocess.run(cmd, check=True)
    print("🎉 构建完成！可执行文件位于 dist/schoolnet/")


def clean_up():
    """清理不必要的文件"""
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    if os.path.exists(SPEC_FILE):
        os.remove(SPEC_FILE)
    print("🧹 清理中间文件完成。")


if __name__ == '__main__':
    create_version_file()
    build_executable()
    clean_up()