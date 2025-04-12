from urllib.parse import parse_qs

import requests

from config_secret import AUTH_DOMAIN, BASE_URL, USERNAME, PASSWORD, TEST_URL
from logger import logger


class NetworkManager:
    @staticmethod
    def check_network():
        """
        检查网络连接状态

        该函数通过发送HTTP请求来检查网络是否连接正常，并且是否能够访问指定的域名。
        它使用了requests库来发送请求，并设置了User-Agent头信息和请求超时时间。

        Returns:
            bool: 如果网络连接正常且不重定向到认证域名，则返回True，否则返回False。
        """
        try:
            # 发送HTTP请求以检查网络连接状态
            response = requests.get(
                url=TEST_URL,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=8
            )
            # 判断响应状态码是否为200且不重定向到认证域名
            return response.status_code == 200 and AUTH_DOMAIN not in response.url
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            # 捕获网络连接异常和超时异常
            logger.warning(f'网络检测异常: {e}')
            return False

    @staticmethod
    def get_auth_urls():
        """
        获取认证相关URL

        该函数通过发送HTTP请求到基础URL，解析响应URL中的查询参数，生成认证相关的URL。
        这些URL包括登录、断开连接和检查认证状态的URL。

        Returns:
            dict: 包含认证相关URL的字典，键为'login'、'disconnect'和'check'，值为对应的URL。
        """
        # 发送HTTP请求以获取认证相关URL
        response = requests.get(BASE_URL)
        # 解析响应URL中的查询参数
        query_params = parse_qs(response.url)

        # 从查询参数中获取IP和MAC地址
        ip = query_params.get('wlanuserip', [''])[0]
        mac = query_params.get('mac', [''])[0]

        # 返回包含认证相关URL的字典
        return {
            'login': f'https://{AUTH_DOMAIN}/webauth.do?wlanacip=172.16.1.82&wlanuserip={ip}&mac={mac}',
            'disconnect': f'https://{AUTH_DOMAIN}/webdisconn.do?wlanacip=172.16.1.82&wlanuserip={ip}&mac={mac}',
            'check': f'https://{AUTH_DOMAIN}/getAuthResult.do'
        }

    @staticmethod
    def get_auth_request_data():
        return {
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
