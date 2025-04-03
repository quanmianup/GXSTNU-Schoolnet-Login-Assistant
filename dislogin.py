import time
from urllib.parse import parse_qs

import requests

from config_secret import USERNAME, PASSWORD

url_temp = (requests.get('http://1.1.1.1')).url  # 获取登录网址，里面包含错误信息
query_params = parse_qs(url_temp)  # 切分网址
ip = query_params.get('wlanuserip')  # 获取本机ip
mac = query_params.get('mac')  # 获取本机mac
data_login = {
    'pageid': 5,
    'templatetype': 1,
    'isRemind': 1,
    'url': 'http://1.2.1.1',
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
url_login = f'https://auth.gxstnu.edu.cn/webauth.do?wlanacip=172.16.1.82&wlanacname=GXSTNU-BRAS&wlanuserip={ip[0]}&mac={mac[0]}&vlan=0&url=http://1.1.1.1'  # 登录网址
url_discon = f'https://auth.gxstnu.edu.cn/webdisconn.do?wlanacip=172.16.1.82&wlanacname=GXSTNU-BRAS&wlanuserip={ip[0]}&mac={mac[0]}&vlan=0&url=http://1.1.1.1'  # 下线网址
url_check = "https://auth.gxstnu.edu.cn/getAuthResult.do"  # 检查登录状态网址

for i in range(4):
    requests.post(url=url_discon, data=data_discon)  # 离线校园网操作
    time.sleep(1.5)
    result = requests.post(url_check, data=data_check)  # 检查登录状态
    if result.status_code == 200:  # 连接状态是否正常
        if '运营商网络拨号成功' not in result.text:  # 检查结果是否成功
            print(f'运营商网络下线成功{USERNAME}')
            break
    print(f'正在尝试下线校园网{USERNAME}.请稍等...')
time.sleep(2)  # 延迟关闭控制台
