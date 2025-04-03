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
import sys  # 新增导入
from urllib.parse import parse_qs
from config_secret import USERNAME, PASSWORD  # 新增导入

import requests


# 创建一个日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建一个文件处理器，并将日志写入到文件
file_handler = logging.FileHandler(f'login{USERNAME}.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# 创建一个控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 定义日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)
data_login = {
    'pageid': 5,
    'templatetype': 1,
    'isRemind': 1,
    'url': 'http://1.1.1.1',
    'userId': USERNAME,
    'passwd': PASSWORD,
    'remInfo': 'on'
}
data_check = {  # 检查登录状态请求体
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Content-Length': 26,
    'Host': 'auth.gxstnu.edu.cn',
    'pageId': '5',
    'userId': USERNAME,
}
data_discon = {  # 下线请求体
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


def login():
    url_temp = (requests.get('http://1.1.1.1')).url  # 获取登录网址，里面包含错误信息
    query_params = parse_qs(url_temp)  # 切分网址
    ip = query_params.get('wlanuserip')  # 获取本机ip
    mac = query_params.get('mac')  # 获取本机mac
    url_login = (f'https://auth.gxstnu.edu.cn/webauth.do?wlanacip=172.16.1.82&wlanacname='
                 f'GXSTNU-BRAS&wlanuserip={ip[0]}&mac={mac[0]}&vlan=0&url=http://1.1.1.1')  # 登录网址
    url_discon = (f'https://auth.gxstnu.edu.cn/webdisconn.do?wlanacip=172.16.1.82&wlanacname'
                  f'=GXSTNU-BRAS&wlanuserip={ip[0]}&mac={mac[0]}&vlan=0&url=http://1.1.1.1')  # 下线网址
    url_check = "https://auth.gxstnu.edu.cn/getAuthResult.do"  # 检查登录状态网址
    if 'errorMsg=' in url_temp:  # 如果账号在线就执行离线操作
        requests.post(url=url_discon, data=data_discon)
        url_temp = (requests.get('http://1.1.1.1')).url  # 获取登录网址，里面包含错误信息
    logger.info(f'正在尝试登录校园网{USERNAME}.请稍等...')
    for i in range(4):
        requests.post(url=url_login, data=data_login)  # 登录校园网操作
        time.sleep(1.5)
        result = requests.post(url_check, data=data_check)  # 检查登录状态
        if result.status_code == 200:  # 连接状态是否正常
            if '运营商网络拨号成功' in result.text:  # 检查结果是否成功
                logger.info(f'运营商网络拨号成功{USERNAME}')
                break
            elif ('errorMsg=' in url_temp) and (i >= 3):  # 账号在线网址才会包含“errorMsg=”
                logger.warning(f'请先离线账号{USERNAME}')
            elif i == 3:
                logger.warning(f'请输入正确的用户名{USERNAME}和密码')
        logger.info(f'正在尝试登录校园网{USERNAME}.请稍等...')
    time.sleep(2)  # 延迟关闭控制台


def run():
    url_bilibili = 'http://www.bilibili.com'
    test_request = requests.get(url_bilibili,
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36 Core/1.116.489.400 QQBrowser/13.7.6351.400'},
                                timeout=8,
                                )
    if test_request.status_code == 200 and "auth.gxstnu.edu.cn" not in test_request.url:
        logger.info('网络正常')
    else:
        login()


def build_exe():
    """仅在直接运行脚本时生成exe文件"""
    import os
    import subprocess

    logger.info("开始生成exe文件...")
    command = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        f"--name=login{USERNAME}",
        "--icon=666.png",
        "--clean",
        "--exclude-module=build_exe",  # 确保不包含生成exe的代码
        "login.py"
    ]

    try:
        subprocess.run(command, check=True)
        logger.info("exe文件生成成功！可在dist目录中找到")
    except subprocess.CalledProcessError as e:
        logger.error(f"生成exe文件失败: {e}")
    except FileNotFoundError:
        logger.error("未找到pyinstaller，请先安装: pip install pyinstaller")


if __name__ == "__main__":
    run()
    # 只有在直接运行python脚本时才生成exe
    if not getattr(sys, 'frozen', False):
        build_exe()
