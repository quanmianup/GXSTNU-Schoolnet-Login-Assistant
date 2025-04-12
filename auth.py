import time

import requests

import network_manager
from config_secret import USERNAME, MAX_RETRY, RETRY_INTERVAL
from logger import logger
from network_manager import NetworkManager


def do_login():
    """
    执行登录流程。

    该函数尝试登录校园网账号，如果账号已在线则直接返回成功。否则，它会多次尝试登录，
    直到成功或达到最大重试次数。每次尝试后，会检查登录状态，并根据响应结果决定是否继续尝试。

    返回值:
        bool: 登录成功返回True，否则返回False。
    """
    urls = NetworkManager.get_auth_urls()
    REQUEST_DATA = NetworkManager.get_auth_request_data()
    # 如果账号已在线，直接退出
    if NetworkManager.check_network():
        logger.info(f'网络正常')
        return True
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
            else:
                logger.error(
                    f'网络异常: 状态码 {response.status_code}, 响应内容: {response.text},请确定当前是否处于校园网环境！')
        except requests.exceptions.RequestException as e:
            logger.error(f'登录请求失败: {e}')

    return False


def do_dislogin():
    """
    执行下线流程。

    该函数尝试下线校园网账号。它会多次尝试下线，直到成功或达到最大重试次数。每次尝试后，
    会检查下线状态，并根据响应结果决定是否继续尝试。

    返回值:
        bool: 下线成功返回True，否则返回False。
    """
    urls = NetworkManager.get_auth_urls()
    REQUEST_DATA = NetworkManager.get_auth_request_data()
    logger.info(f'正在尝试下线校园网账号: {USERNAME}')

    for attempt in range(MAX_RETRY):
        try:
            # 下线请求
            requests.post(urls['disconnect'], data=REQUEST_DATA['disconnect'])
            time.sleep(RETRY_INTERVAL)

            # 检查状态
            if not NetworkManager.check_network():
                logger.info(f'下线成功: {USERNAME}')
                return True
            elif attempt == MAX_RETRY - 1:
                logger.warning('请检查账号密码或先下线已登录账号')  # 修改此处的提示信息
        except requests.exceptions.RequestException as e:
            logger.error(f'登录请求失败: {e}')  # 修改此处的提示信息
    return False
