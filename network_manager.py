from urllib.parse import parse_qs

import requests

from logger import logger

# 常量定义
BASE_URL = "http://1.1.1.1"
AUTH_DOMAIN = "auth.gxstnu.edu.cn"


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
                'http://www.bilibili.com',
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
