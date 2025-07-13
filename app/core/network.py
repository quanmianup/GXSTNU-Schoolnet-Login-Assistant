import time
from urllib.parse import urlparse, parse_qs

import requests

from app.utils.logger import logger
# 导入配置
from config.credentials import credentials


class NetworkManager:
    """
    网络管理类，采用单例模式实现，用于管理校园网的网络连接、登录和登出等操作。
    该类从配置文件中读取必要的参数，提供网络状态检查、获取认证链接、登录和登出等功能。

    使用方法：
    1. 获取全局单例：
        >>> from app.core.network import networkmanager
    3. 检查网络状态：
        调用 `check_network` 方法检查网络是否连接且不在认证页面。
        >>> is_connected = networkmanager.check_network()
        >>> if is_connected:
        >>>     print("网络已连接且不在认证页")
        >>> else:
        >>>     print("网络未连接或处于认证页")

    4. 登录校园网：
        调用 `login` 方法进行登录操作，可传入自定义的用户名和密码，若不传则使用配置文件中的默认值。
        # 使用默认用户名和密码登录
        >>> login_success = networkmanager.login()
        >>> if login_success:
        >>>     print("登录成功")
        >>> else:
        >>>     print("登录失败")

        # 使用自定义用户名和密码登录
        >>> custom_login_success = networkmanager.login(username="your_username", password="your_password")
        >>> if custom_login_success:
        >>>     print("自定义账号登录成功")
        >>> else:
        >>>     print("自定义账号登录失败")

    5. 登出校园网：
        调用 `logout` 方法进行登出操作，可传入自定义的用户名，若不传则使用配置文件中的默认值。
        # 使用默认用户名登出
        >>> logout_success = networkmanager.dislogin()
        >>> if logout_success:
        >>>     print("登出成功")
        >>> else:
        >>>     print("登出失败")

        # 使用自定义用户名登出
        >>> custom_logout_success = networkmanager.dislogin(username="your_username")
        >>> if custom_logout_success:
        >>>     print("自定义账号登出成功")
        >>> else:
        >>>     print("自定义账号登出失败")

    """
    _instance = None  # 类级别私有变量，用于保存类的唯一实例
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式，确保类只有一个实例被创建。

        Returns:
            NetworkManager: 类的唯一实例。
        """
        if cls._instance is None:
            # 若实例不存在，则创建一个新实例
            cls._instance = super(NetworkManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化网络管理类，从配置文件中获取必要的网络参数。
        """
        self.TEST_URL = credentials.get("TEST_URL")
        self.BASE_URL = credentials.get("BASE_URL")
        self.USERNAME = credentials.get("USERNAME")
        self.PASSWORD = credentials.get("PASSWORD")
        self.MAX_RETRY = credentials.get("MAX_RETRY")
        self.AUTH_DOMAIN = credentials.get("AUTH_DOMAIN")
        self.RETRY_INTERVAL = credentials.get("RETRY_INTERVAL")

    def lazy_init(self):
        """
        懒加载初始化方法，仅在第一次调用时从配置文件加载参数，避免不必要的初始化开销。
        """
        if not self._initialized:
            # 从配置加载参数
            self.TEST_URL = credentials.get("TEST_URL")
            self.BASE_URL = credentials.get("BASE_URL")
            self.USERNAME = credentials.get("USERNAME")
            self.PASSWORD = credentials.get("PASSWORD")
            self.MAX_RETRY = credentials.get("MAX_RETRY")
            self.AUTH_DOMAIN = credentials.get("AUTH_DOMAIN")
            self.RETRY_INTERVAL = credentials.get("RETRY_INTERVAL")
            self._initialized = True

    def check_network(self):
        """
        检查网络连接状态，判断网络是否连接成功且不在认证页面。

        Returns:
            bool: 若网络连接成功且不在认证页返回 True，否则返回 False。
        """
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            # 发送 GET 请求检测网络状态
            response = requests.get(url=self.TEST_URL, headers=headers, timeout=self.RETRY_INTERVAL)
            # 判断状态码是否为 200 且响应 URL 不包含认证域名
            is_connected = response.status_code == 200 and self.AUTH_DOMAIN not in response.url
            if not is_connected:
                logger.warning("网络未连接或处于认证页面")
                return False
            return True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            logger.error(f'网络检测异常: {e}')
            return False

    def get_auth_urls(self):
        """
        获取认证相关的 URL，包括登录、登出和检查状态的 URL，其中包含本机的 IP 和 MAC 地址。

        Returns:
            dict: 包含 'login'、'disconnect'、'check' 三个键的 URL 字典，若获取失败则返回 None。
        """
        try:
            # 发送 GET 请求获取认证相关信息
            response = requests.get(self.BASE_URL, timeout=self.RETRY_INTERVAL)
            # 解析响应 URL
            parsed_url = urlparse(response.url)
            # 解析 URL 中的查询参数
            query_params = parse_qs(parsed_url.query)
            ip = query_params.get('wlanuserip', '')
            mac = query_params.get('mac', '')
            return {
                'login': f'https://{self.AUTH_DOMAIN}/webauth.do?wlanacip=172.16.1.82&wlanuserip={ip}&mac={mac}',
                'disconnect': f'https://{self.AUTH_DOMAIN}/webdisconn.do?wlanacip=172.16.1.82&wlanuserip={ip}&mac={mac}',
                'check': f'https://{self.AUTH_DOMAIN}/getAuthResult.do'
            }
        except Exception as e:
            logger.error(f"获取认证链接失败: {e}")

    def get_data(self, username=None, password=None):
        """
        获取登录、登出和检查状态请求的数据体。

        Args:
            username (str, optional): 登录用户名，默认为配置文件中的用户名。
            password (str, optional): 登录密码，默认为配置文件中的密码。

        Returns:
            dict: 包含 'check'、'login'、'disconnect' 三个键的数据体字典。
        """
        username = self.USERNAME if username is None else username
        password = self.PASSWORD if password is None else password

        data = {
            'check': {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Content-Length': 26,
                'Host': 'auth.gxstnu.edu.cn',
                'pageId': '5',
                'userId': username,
            },
            'login': {
                'pageid': 5,
                'templatetype': 1,
                'isRemind': 1,
                'url': self.BASE_URL,
                'userId': username,
                'passwd': password,
                'remInfo': 'on'
            },
            'disconnect': {
                'hostIp': 'http://127.0.0.1:8080/',
                'auth_type': 0,
                'isBindMac1': 0,
                'pageid': 5,
                'templatetype': 1,
                'listbindmac': 0,
                'recordmac': 0,
                'isRemind': 1,
                'distoken': "3f2bb10a720f2bffd060423453a0fa15",
                'userId': username,
                'other1': 'disconn'
            }
        }
        return data

    def login(self, username=None, password=None):
        """
        执行登录操作，支持重试机制。若账号已在线，会先执行下线操作。

        Args:
            username (str, optional): 登录用户名，默认为配置文件中的用户名。
            password (str, optional): 登录密码，默认为配置文件中的密码。

        Returns:
            bool: 若登录成功返回 True，否则返回 False。
        """
        username = self.USERNAME if username is None else username
        password = self.PASSWORD if password is None else password
        # 获取登录 URL
        login_url = self.get_auth_urls()['login']
        # 获取登录请求数据体
        login_data = self.get_data(username, password)['login']
        # 获取检查状态 URL
        check_url = self.get_auth_urls()['check']
        # 获取检查状态请求数据体
        check_data = self.get_data(username, password)['check']
        # 如果账号已在线，先执行下线
        if 'errorMsg=' in requests.get(url=check_url, data=check_data, timeout=self.RETRY_INTERVAL).text:
            logger.info(f"{username}账号已在线，执行下线操作")
            self.logout(username)
        logger.info(f'正在尝试登录校园网账号: {username}')

        for attempt in range(self.MAX_RETRY):
            # 发送登录请求
            requests.post(url=login_url, data=login_data, timeout=self.RETRY_INTERVAL)
            # 等待一段时间后检查登录状态
            time.sleep(self.RETRY_INTERVAL)
            response = requests.post(url=check_url, data=check_data, timeout=self.RETRY_INTERVAL)
            if response.status_code == 200:
                if '运营商网络拨号成功' in response.text and self.check_network():
                    logger.info(f'登录成功: {username}')
                    return True
                if attempt + 1 == self.MAX_RETRY:
                    logger.warning('请检查账号密码或先下线已登录账号')
                    return False
            logger.info(f'第 {attempt + 1} 次登录失败，状态码: {response.status_code}')
        logger.warning(f"{username}登录失败")
        return False

    def logout(self, username=None):
        """
        执行登出操作，支持重试机制。

        Args:
            username (str, optional): 登出的用户名，默认为配置文件中的用户名。

        Returns:
            bool: 若登出成功返回 True，否则返回 False。
        """
        username = self.USERNAME if username is None else username
        # 获取登出请求数据体
        logout_data = self.get_data(username)['disconnect']
        # 获取登出 URL
        disconnect_url = self.get_auth_urls()['disconnect']
        for i in range(self.MAX_RETRY):
            # 发送登出请求
            response = requests.post(url=disconnect_url, data=logout_data, timeout=self.RETRY_INTERVAL)
            if response.status_code == 200 and not self.check_network():
                logger.info("登出成功")
                return True
            else:
                logger.warning(f"第 {i + 1} 次登出失败，状态码: {response.status_code}")
        return False


networkmanager = NetworkManager()
