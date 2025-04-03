import requests
from config_secret import USERNAME, PASSWORD

# 以下自动获取无需编辑--------------------------------
text_xc = requests.get('https://www.bilibili.com', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36 Core/1.116.489.400 QQBrowser/13.7.6351.400'})  # 发送请求获取数据
print(text_xc)
url_check = "https://auth.gxstnu.edu.cn/getAuthResult.do"  # 检查登录状态网址
data_check = {  # 检查登录状态请求体
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip,deflate,br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie: remeberMeCookie': '075773cd692390a0bd107a0e3bc42cee168a3252b234379e8adb3ad6cf133cfddb3259229578186454cb3bf93c11100c82e3e9514e198ba2; JSESSIONID-BOSS-0=A14C581922C7D5BFE90D8A6B1E228D23; portal_token=075773cd692390a0d4dde1bfce4e278c054e93e374e49e9488b372e44348dec282e3e9514e198ba2',
    'Content-Length': '26',
    'Host': 'auth.gxstnu.edu.cn',
    'pageId': '5',
    'userId': USERNAME,
}
result = requests.post(url=url_check, data=data_check)
# print(result.text)
