import sys
import os
import time
# 将项目根目录添加到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.NetworkManager import networkmanager

if __name__ == '__main__':
    for i in range(1,6):
        networkmanager.login()
        print(f'尝试第{i}次登录...')
        if networkmanager.check_network():
            print('登录成功')
            break
        time.sleep(1)
