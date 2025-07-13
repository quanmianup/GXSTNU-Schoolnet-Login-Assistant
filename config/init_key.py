import base64
from Crypto.Random import get_random_bytes

from config.credentials import credentials
from config.local_credentials import CREDENTIALS
from app.utils.logger import logger

# 生成新密钥
key = get_random_bytes(32)
key_b64 = base64.b64encode(key).decode('utf-8')

# 写入配置
CREDENTIALS['ENCRYPTED_KEY'] = key_b64

# 保存到文件
credentials.save_to_file()

logger.info("✅ 密钥已生成并写入配置文件")
