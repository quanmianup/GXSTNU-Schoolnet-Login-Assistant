import sys
import os
import time
# 将项目根目录添加到sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.NetworkManager import networkmanager

if __name__ == '__main__':
    networkmanager.login()
    time.sleep(2)