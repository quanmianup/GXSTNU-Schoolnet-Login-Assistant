"""
这是一个登录GKS校园网的程序，需要填写code中的配置信息
输出日志文件到当前文件目录的login+账号.log
导出命令：
pyinstaller [选项] 脚本文件.py
常用选项：
-D, --onedir：生成一个包含可执行文件的文件夹（默认）
-F, --onefile：生成一个单独的可执行文件
-n NAME, --name NAME：指定生成的可执行文件和 .spec 文件的名称
-c, --console, --nowindowed：打开控制台窗口（默认）
-w, --windowed, --noconsole：不提供控制台窗口
-i, --icon <FILE.ico or FILE.exe,ID or FILE.icns or Image or "NONE">：设置应用程序图标
--version-file FILE：添加版本资源到可执行文件中
--clean：在构建前清理 PyInstaller 缓存和临时文件
--log-level LEVEL：设置构建时控制台消息的详细程度
"""
import logging
import time
import sys
from urllib.parse import parse_qs
from config_secret import USERNAME, PASSWORD
import requests

# 常量定义
BASE_URL = "http://1.1.1.1"
AUTH_DOMAIN = "auth.gxstnu.edu.cn"
MAX_RETRY = 4
RETRY_INTERVAL = 1.5


# 日志配置
def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 文件处理器
    file_handler = logging.FileHandler(f'login_{USERNAME}.log', encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    console_handler.addHandler(console_handler)
    return logger


logger = setup_logger()

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
        'pageId': '5',
        'userId': USERNAME,
    },
    'disconnect': {
        'hostIp': 'http://127.0.0.1:8080/',
        'auth_type': 0,
        'pageid': 5,
        'userId': USERNAME,
        'other1': 'disconn'
    }
}


class NetworkManager:
    @staticmethod
    def check_network():
        """检查网络连接状态"""
        try:
            response = requests.get(
                'http://www.bilibili.com',
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=8
            )
            return response.status_code == 200 and AUTH_DOMAIN not in response.url
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logger.warning(f'网络检测异常: {e}')
            return False

    @staticmethod
    def get_auth_urls():
        """获取认证相关URL"""
        response = requests.get(BASE_URL)
        query_params = parse_qs(response.url)

        ip = query_params.get('wlanuserip', [''])[0]
        mac = query_params.get('mac', [''])[0]

        return {
            'login': f'https://{AUTH_DOMAIN}/webauth.do?wlanacip=172.16.1.82&wlanuserip={ip}&mac={mac}',
            'disconnect': f'https://{AUTH_DOMAIN}/webdisconn.do?wlanacip=172.16.1.82&wlanuserip={ip}&mac={mac}',
            'check': f'https://{AUTH_DOMAIN}/getAuthResult.do'
        }


def login():
    """执行登录流程"""
    urls = NetworkManager.get_auth_urls()

    # 如果账号已在线，先执行下线
    if 'errorMsg=' in urls.get('login', ''):
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
    except Exception as e:
        logger.error(f"构建失败: {e}")


def main():
    if not NetworkManager.check_network():
        login()

    # 直接运行时构建EXE
    # if not getattr(sys, 'frozen', False):
    #     build_executable()


if __name__ == "__main__":
    main()
