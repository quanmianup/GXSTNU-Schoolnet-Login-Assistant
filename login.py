"""
这是一个登录GKS校园网的程序，需要填写code中的配置信息
输出日志文件到当前文件目录的login+账号.log
"""
import time

import requests

from config_secret import USERNAME, PASSWORD
from logger import logger
from network_manager import NetworkManager  # 新增导入

# 常量定义
# BASE_URL用于指定基础的URL地址
BASE_URL = "http://1.1.1.1"
# AUTH_DOMAIN用于指定认证域，用于用户身份验证
AUTH_DOMAIN = "auth.gxstnu.edu.cn"
# MAX_RETRY定义最大重试次数，以处理网络请求失败的情况
MAX_RETRY = 4
# RETRY_INTERVAL定义重试间隔时间，单位为秒
RETRY_INTERVAL = 1.5


# 请求数据模板
REQUEST_DATA = {
    'login': {
        'pageid': 5,
        'templatetype': 1,
        'isRemind': 1,
        'url': BASE_URL,
        'userId': USERNAME,
        'passwd': PASSWORD,
        'remInfo': 'on'
    },
    'check': {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Content-Length': 26,
        'Host': 'auth.gxstnu.edu.cn',
        'pageId': '5',
        'userId': USERNAME,
    },
    'disconnect': {
        'hostIp': ' http://127.0.0.1:8080/',
        'auth_type': 0,
        'isBindMac1': 0,
        'pageid': 5,
        'templatetype': 1,
        'listbindmac': 0,
        'recordmac': 0,
        'isRemind': 1,
        'distoken': '3f2bb10a720f2bffd060423453a0fa15',
        'userId': USERNAME,
        'other1': 'disconn'
    }
}


def login():
    """执行登录流程"""
    urls = NetworkManager.get_auth_urls()

    # 如果账号已在线，先执行下线
    if 'errorMsg=' in requests.get(url=urls['check'], data=REQUEST_DATA['check']):
        requests.post(urls['disconnect'], data=REQUEST_DATA['disconnect'])

    logger.info(f'正在尝试登录校园网账号: {USERNAME}')

    for attempt in range(MAX_RETRY):
        try:
            # 登录请求
            requests.post(urls['login'], data=REQUEST_DATA['login'])
            time.sleep(RETRY_INTERVAL)

            # 检查状态
            response = requests.post(urls['check'], data=REQUEST_DATA['check'])

            if response.status_code == 200:
                if '运营商网络拨号成功' in response.text:
                    logger.info(f'登录成功: {USERNAME}')
                    return True
                elif attempt == MAX_RETRY - 1:
                    logger.warning('请检查账号密码或先下线已登录账号')
        except requests.exceptions.RequestException as e:
            logger.error(f'登录请求失败: {e}')

    return False


def dislogin():
    """执行下线流程"""
    urls = NetworkManager.get_auth_urls()

    logger.info(f'正在尝试下线校园网账号: {USERNAME}')

    for attempt in range(MAX_RETRY):
        try:
            # 登录请求
            requests.post(urls['disconnect'], data=REQUEST_DATA['disconnect'])
            time.sleep(RETRY_INTERVAL)

            # 检查状态
            response = requests.post(urls['check'], data=REQUEST_DATA['check'])  # 修改此处的URL为检查状态的URL
            if response.status_code == 200:
                if '运营商网络拨号成功' in response.text:
                    logger.info(f'登录成功: {USERNAME}')
                    return True
                elif attempt == MAX_RETRY - 1:
                    logger.warning('请检查账号密码或先下线已登录账号')  # 修改此处的提示信息
        except requests.exceptions.RequestException as e:
            logger.error(f'登录请求失败: {e}')  # 修改此处的提示信息
    return False


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
            "login.py"
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
    if NetworkManager.check_network():
        logger.info("网络连接正常")
    else:
        login()

    # 直接运行时构建EXE
    # if not getattr(sys, 'frozen', False):
    #     build_executable()


if __name__ == "__main__":
    main()
