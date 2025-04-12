"""
这是一个登录GKS校园网的程序
输出日志文件到当前文件目录的login+账号.log
"""
from auth import do_login, do_dislogin
from config_secret import USERNAME, PASSWORD
from gui import run_gui
from logger import logger


def build_executable():
    """构建可执行文件"""
    try:
        import subprocess
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--noconsole",
            f"--name=login_{USERNAME}",
            "--icon=icon.ico",
            "--clean",
            "main.py"
        ], check=True)
        logger.info("EXE文件生成成功")
        '''
        导出命令：
        pyinstaller [选项] 脚本文件.py
        常用选项：
        -D, --onedir：生成一个包含可执行文件的文件夹（默认）
        -F, --onefile：生成一个单独的可执行文件
        -n NAME, --name NAME：指定生成的可执行文件和.spec文件的名称
        -c, --console, --nowindowed：打开控制台窗口（默认）
        -w, --windowed, --noconsole：不提供控制台窗口
        -i, --icon < FILE.ico or FILE.exe, ID or FILE.icns or Image or "NONE" >：设置应用程序图标
        --version - file FILE：添加版本资源到可执行文件中
        --clean：在构建前清理PyInstaller缓存和临时文件
        --log - level LEVEL：设置构建时控制台消息的详细程度
        '''
    except Exception as e:
        logger.error(f"构建失败: {e}")


def main():
    # 修改为启动GUI界面
    run_gui()


if __name__ == "__main__":
    main()
