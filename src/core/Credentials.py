# -*- coding: utf-8 -*-
"""
校园网登录助手 - 凭证管理模块

该模块提供了安全的凭证存储与管理功能，支持密码的加密存储和解密访问。
主要功能：
- AES ECB模式对称加密，确保敏感信息安全存储
- 配置文件自动创建和持久化功能
- 凭证缓存机制，提高频繁访问性能
- 全局单例模式设计，确保系统中凭证管理的一致性

依赖项：
- Crypto (pycryptodome)：提供AES加密算法支持
- base64：用于编码解码二进制数据
- importlib：支持动态导入配置模块
- os, re：文件操作和正则表达式处理
- src.utils.logger：日志记录
- src.core.TaskScheduler：任务调度器，用于获取配置文件路径

使用示例：
```python
# 获取凭证管理器单例
from src.core.Credentials import credentials

# 读取凭证
username = credentials.get("username")
password = credentials.get("password")  # 自动解密

# 设置凭证
credentials.set("username", "new_username")
credentials.set("password", "new_password")  # 自动加密存储

# 保存配置（通常不需要手动调用，set方法会自动触发）
credentials.save_to_file()
```
"""
import base64
import importlib.util
import os
import re

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad

from src.core.TaskScheduler import TaskScheduler
from src.utils.logger import logger

# 全局CREDENTIALS变量，用于存储所有凭证信息
CREDENTIALS = {}


class CredentialManager:
    """
    凭证管理类，用于处理敏感信息的加密存储与访问
    使用AES ECB模式进行对称加密，支持用户名和密码的加密存储
    提供配置文件自动创建和持久化功能

    使用方法：
    1. 获取全局单例：
       >>> from src.core.Credentials import credentials

    2. 读取凭证：
       >>> password = credentials.get("password")    # 获取解密后的密码

    3. 写入凭证：
        >>> credentials.set("password", "new_pass")  # 自动加密存储
        >>> credentials.set("custom_key", "value")  # 设置自定义键值对

    4. 保存配置：
       >>> credentials.save_to_file()  # 持久化到本地配置文件

    注意事项：
    - 首次运行时会自动创建 config/local_credentials.py 配置文件
    - 密码会自动加密存储，明文仅存在于内存中
    - 修改凭证后自动调用 save_to_file() 持久化
    
    属性：
    - _cache: 内部缓存字典，用于存储已解密的凭证值，提高访问效率
    - KEY: AES加密密钥（二进制格式），用于加解密敏感数据
    - task_folder: 任务文件夹路径，从TaskScheduler获取
    - CREDENTIALS_file_path: 凭证配置文件的完整路径
    """

    def __init__(self):
        """
        初始化凭证管理器
        1. 检查配置文件是否存在
        2. 若不存在则创建默认配置文件
        3. 加载加密密钥并验证有效性
        """
        self._cache = {}  # 凭证缓存字典，存储解密后的凭证值
        self.KEY = None  # AES加密密钥
        self.task_folder = TaskScheduler().task_folder  # 任务文件夹路径
        self.CREDENTIALS_file_path = self._get_config_path()  # 配置文件路径
        self._load_credentials()  # 加载凭证配置
        self._check_config()  # 检查TEST_URL配置类型
        self._load_key()  # 加载加密密钥

    def _load_credentials(self):
        """
        从配置文件中加载CREDENTIALS配置
        通过importlib模块动态导入配置文件，避免硬编码路径依赖
        若配置文件不存在或格式错误，会记录日志并抛出异常
        """
        global CREDENTIALS

        # 检查配置文件是否存在
        if not os.path.exists(self.CREDENTIALS_file_path):
            logger.info("未找到配置文件，正在创建默认配置...")
            self.create_local_credentials_file()

        # 使用importlib动态导入模块
        try:
            spec = importlib.util.spec_from_file_location("local_credentials", self.CREDENTIALS_file_path)
            local_credentials = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(local_credentials)
            # 更新全局CREDENTIALS变量
            if hasattr(local_credentials, 'CREDENTIALS'):
                CREDENTIALS = local_credentials.CREDENTIALS
            else:
                logger.error("配置文件中未找到CREDENTIALS变量")
                # 如果没有找到，创建空的CREDENTIALS
                raise ValueError("配置文件中未找到CREDENTIALS变量")
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            raise ValueError(f"加载配置文件失败: {str(e)}")

    def _load_key(self):
        """
        加载或生成AES加密密钥
        如果配置中没有ENCRYPTED_KEY，则自动生成新密钥并保存
        否则从配置中解码并加载已有的密钥
        """
        encrypted_key = CREDENTIALS.get('ENCRYPTED_KEY')
        if not encrypted_key:
            logger.error("未设置ENCRYPTED_KEY，正在初始化密钥")
            key = get_random_bytes(32)  # 生成32字节（256位）的随机密钥
            key_b64 = base64.b64encode(key).decode('utf-8')
            CREDENTIALS['ENCRYPTED_KEY'] = key_b64
            self.save_to_file()
            logger.info("✅ 密钥已生成并写入配置文件")
            self.KEY = base64.b64decode(key_b64)
        else:
            self.KEY = base64.b64decode(encrypted_key)

    def _get_config_path(self):
        """
        获取配置文件路径，兼容不同操作系统和打包环境

        返回:
            str: 配置文件的完整路径
        """

        return os.path.join(self.task_folder, 'config', 'local_credentials.py')

    def _encrypt(self, data):
        """
        使用AES ECB模式加密数据（PKCS#7填充）

        参数:
            data (str): 待加密的原始字符串数据

        返回:
            str: Base64编码的加密结果
        """
        cipher = AES.new(self.KEY, AES.MODE_ECB)
        # ✅ 确保加密时使用 pad
        encrypted_raw = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        encrypted_data = base64.b64encode(encrypted_raw).decode()
        return encrypted_data

    def _decrypt(self, encrypted_data):
        """
        使用AES ECB模式解密数据

        参数:
            encrypted_data (str): Base64编码的加密数据

        返回:
            str: 解密后的原始字符串数据
        """
        try:
            cipher = AES.new(self.KEY, AES.MODE_ECB)
            decrypted_padded = cipher.decrypt(base64.b64decode(encrypted_data))
            decrypted_data = unpad(decrypted_padded, AES.block_size)
            return decrypted_data.decode('utf-8')
        except ValueError as e:
            # 🛠️ 明确处理填充错误
            raise ValueError("Invalid data padding") from e

    def get(self, key: str, default=None):
        """
        获取指定凭证项的值（自动处理解密）

        参数:
            key (str): 凭证键名（大小写不敏感）
            default (Any, optional): 未找到键时的默认返回值，默认为None

        返回:
            Any: 对应的凭证值（密码会自动解密），未找到时返回default
        """

        key_upper = key.upper()
        # 优先返回缓存值
        if key_upper in self._cache:
            return self._cache[key_upper]
        try:
            if key_upper == 'PASSWORD':
                # 处理密码的特殊解密逻辑
                encrypted_value = CREDENTIALS.get('ENCRYPTED_PASSWORD', '')
                value = self._decrypt(encrypted_value) if encrypted_value else default
            else:
                # 普通键直接取值
                value = CREDENTIALS.get(key_upper, default)

            # 更新缓存（仅缓存有效非默认值）
            if value is not default:
                self._cache[key_upper] = value

            return value

        except ValueError as e:
            # 解密失败时返回默认值并记录日志
            logger.error(f"获取凭证失败，key={key}: {str(e)}")
            return default

    def set(self, key: str, value: any):
        """
        设置凭证项的值（敏感数据自动处理加密存储）

        参数:
            key (str): 凭证键名（大小写不敏感）
            value (Any): 待存储的凭证值
        """
        try:
            key_upper = key.upper()
            if key_upper == 'PASSWORD':
                CREDENTIALS['ENCRYPTED_PASSWORD'] = self._encrypt(value)
            else:
                CREDENTIALS[key_upper] = value
            self.save_to_file()
            self._cache[key_upper] = value
        except Exception as e:
            logger.error(f"设置凭证失败，key={key}: {str(e)}")
            raise ValueError(f"设置凭证失败，key={key}: {str(e)}")

    def save_to_file(self):
        """
        将当前配置持久化到文件（保持原有文件结构）
        保留文件中的注释和格式，仅更新CREDENTIALS字典中的键值对
        """
        # 确保配置目录存在
        os.makedirs(os.path.dirname(self.CREDENTIALS_file_path), exist_ok=True)
        with open(self.CREDENTIALS_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        keys_to_save = set(CREDENTIALS.keys())
        new_lines = []
        inside_credentials = False

        for line in lines:
            if line.strip().startswith('CREDENTIALS = {'):
                inside_credentials = True
                new_lines.append(line)
                continue
            elif inside_credentials and ':' in line:
                # 更新已有键值对
                match = re.match(r"\s*'([^']+)'\s*:", line)  # 捕获组 ([^']+) 提取单引号内的键名内容
                if match and match.group(1) in CREDENTIALS:
                    key = match.group(1)
                    val = CREDENTIALS[key]
                    new_lines.append(f"    '{key}': '{val}',\n" if isinstance(val, str) else f"    '{key}': {val},\n")
                    keys_to_save.discard(key)
                else:
                    new_lines.append(line)
            elif inside_credentials and line.strip() == '}':
                # 插入剩余的新键值对并闭合字典
                for key in sorted(keys_to_save):
                    val = CREDENTIALS[key]
                    new_lines.append(f"    '{key}': '{val}',\n" if isinstance(val, str) else f"    '{key}': {val},\n")
                new_lines.append(line)
                inside_credentials = False
            else:
                new_lines.append(line)

        with open(self.CREDENTIALS_file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    def _check_config(self):
        """
        检查配置文件是否为最新版本；
        此次更新为检测TEST_URL配置类型是否为list，如果不是则删除并重新创建配置文件
        """
        global CREDENTIALS
        
        if 'TEST_URL' not in CREDENTIALS or not isinstance(CREDENTIALS['TEST_URL'], list):
            logger.warning(f"TEST_URL配置类型错误: {type(CREDENTIALS['TEST_URL']).__name__}，应为list")
            # 删除错误的配置文件
            os.remove(self.CREDENTIALS_file_path)
            # 重新创建配置文件
            self.create_local_credentials_file()
            logger.info("已删除错误配置文件并重新创建默认配置文件")
            # 重新加载配置
            self._load_credentials()
            logger.info("已重新加载配置")

    def create_local_credentials_file(self):
        """
        创建默认配置文件（不论文件是否存在）
        包含初始密钥、空凭证和默认配置参数
        创建的文件包含详细注释，说明各配置项的用途
        """
        # 确保配置目录存在
        os.makedirs(os.path.dirname(self.CREDENTIALS_file_path), exist_ok=True)

        default_content = '''
"""
系统配置说明：
1. ENCRYPTED_KEY: 加密后的AES密钥(Base64编码)，用于密码加密
2. ENCRYPTED_PASSWORD: 加密后的用户密码
3. USERNAME: 登录用户名(明文)
4. BASE_URL: 校园网基础URL
5. AUTH_DOMAIN: 认证服务器域名
6. MAX_RETRY: 网络请求最大重试次数
7. RETRY_INTERVAL: 重试间隔时间(秒)
8. TEST_URL: 网络连通性测试URL
9. MAIN_LOCK: 主界面是否锁定
10.UPDATE_ON_START：启动时是否检查更新
"""
CREDENTIALS = {
    # 加密后的密钥（Base64 编码）
    'ENCRYPTED_KEY': '',
    'ENCRYPTED_PASSWORD': '',
    'USERNAME': '',

    # 其他非敏感配置
    'BASE_URL': 'http://1.1.1.1',
    'AUTH_DOMAIN': 'auth.gxstnu.edu.cn',
    'MAX_RETRY': 4,
    'RETRY_INTERVAL': 1.5,
    'TEST_URL': ['http://www.bilibili.com', 'http://www.baidu.com', 'http://www.gitee.com', 'http://www.taobao.com', 'http://www.douyin.com'],
    'MAIN_LOCK': True,
    'UPDATE_ON_START': True,
}

        '''
        if not os.path.exists(self.CREDENTIALS_file_path):
            with open(self.CREDENTIALS_file_path, 'w', encoding='utf-8') as f:
                f.write(default_content)
            logger.info(f"已创建 {self.CREDENTIALS_file_path} 并写入默认配置")
        else:
            # 直接覆盖现有文件
            with open(self.CREDENTIALS_file_path, 'w', encoding='utf-8') as f:
                f.write(default_content)
            logger.info(f"已覆盖 {self.CREDENTIALS_file_path} 并写入默认配置")


# 全局单例实例，供系统其他模块直接调用
# 使用方式：from src.core.Credentials import credentials
credentials = CredentialManager()
