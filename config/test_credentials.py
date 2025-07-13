import unittest
from unittest.mock import patch, MagicMock
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from config.credentials import CredentialManager

class TestCredentialManager(unittest.TestCase):
    def setUp(self):
        """初始化测试环境"""
        self.cm = CredentialManager()
        # 使用固定密钥避免随机性干扰测试
        self.cm.KEY = b'0123456789abcdef'  # 16字节密钥

    @patch('config.credentials.pad')
    @patch('Crypto.Cipher.AES.new')
    @patch('base64.b64encode')
    def test_encrypt_normal_flow(self, mock_b64encode, mock_aes_new, mock_pad):
        """测试_encrypt正常流程"""
        # 模拟依赖返回值
        mock_pad.return_value = b'padded_data'
        mock_cipher = MagicMock()
        mock_aes_new.return_value = mock_cipher
        mock_cipher.encrypt.return_value = b'encrypted_raw'
        mock_b64encode.return_value = b'base64_str'

        # 调用被测函数
        result = self.cm._encrypt('test')

        # 验证调用顺序和参数
        mock_pad.assert_called_once_with(b'test', AES.block_size)
        mock_aes_new.assert_called_once_with(self.cm.KEY, AES.MODE_ECB)
        mock_cipher.encrypt.assert_called_once_with(b'padded_data')
        mock_b64encode.assert_called_once_with(b'encrypted_raw')
        self.assertEqual(result, 'base64_str')

    @patch('base64.b64decode')
    @patch('Crypto.Cipher.AES.new')
    @patch('config.credentials.unpad')
    def test_decrypt_normal_flow(self, mock_unpad, mock_aes_new, mock_b64decode):
        """测试_decrypt正常流程"""
        # 模拟依赖返回值
        mock_b64decode.return_value = b'encrypted_data'
        mock_cipher = MagicMock()
        mock_aes_new.return_value = mock_cipher
        mock_cipher.decrypt.return_value = b'decrypted_padded'
        mock_unpad.return_value = b'unpadded_data'

        # 调用被测函数
        result = self.cm._decrypt('base64_str')

        # 验证调用顺序和参数
        mock_b64decode.assert_called_once_with('base64_str')
        mock_aes_new.assert_called_once_with(self.cm.KEY, AES.MODE_ECB)
        mock_cipher.decrypt.assert_called_once_with(b'encrypted_data')
        mock_unpad.assert_called_once_with(b'decrypted_padded', AES.block_size)
        self.assertEqual(result, 'unpadded_data')

    def test_encrypt_decrypt_integration(self):
        """测试_encrypt和_decrypt互操作性"""
        data = "sensitive_data"
        encrypted = self.cm._encrypt(data)
        decrypted = self.cm._decrypt(encrypted)
        self.assertEqual(decrypted, data)

    @patch('base64.b64decode', side_effect=Exception("Invalid base64"))
    def test_decrypt_invalid_base64(self, _):
        """测试_decrypt处理无效Base64输入"""
        with self.assertRaises(Exception) as context:
            self.cm._decrypt('invalid_base64')
        self.assertEqual(str(context.exception), "Invalid base64")

    @patch('config.credentials.unpad', side_effect=ValueError("Padding is incorrect"))
    def test_decrypt_invalid_padding(self, _):
        """测试_decrypt处理无效填充数据"""
        # 模拟解密后的数据为16字节（块对齐）
        mock_cipher = MagicMock()
        mock_cipher.decrypt.return_value = b'invalid_data_123'  # 长度为16字节
        with patch('Crypto.Cipher.AES.new', return_value=mock_cipher):
            with self.assertRaises(ValueError) as context:
                self.cm._decrypt('valid_base64')
        self.assertEqual(str(context.exception), "Padding is incorrect")
if __name__ == '__main__':
    unittest.main()
