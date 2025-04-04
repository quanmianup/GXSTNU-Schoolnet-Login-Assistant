# 广西科师校园网自动登录工具

<img alt="Python" src="https://img.shields.io/badge/Python-3.11-blue"/>

这是一个用于广西科技师范学院校园网自动登录/注销的Python脚本工具。

## 功能特性

- 自动检测网络连接状态
- 自动登录校园网
- 自动注销当前账号
- 生成可执行文件(EXE)方便使用
- 详细的日志记录

## 使用说明

### 前置要求
- Python 3.11

### 准备工作

1. 克隆本项目到本地：
   ```bash
   git clone https://gitee.com/quanmian/GKS-schoolnet-login.git
   ```
2. 安装所需的Python库：
   ```bash
   pip install -r requirements.txt
   ```
3. 复制配置文件模板并填写你的账号信息：
   ```bash
   cp config_secret_example.py config_secret.py
   ```

4. 然后编辑config_secret.py文件，填写你的校园网账号和密码。

### 运行方式

直接运行Python脚本：

   ```bash
   python login.py
   ```

生成的可执行文件会在dist目录中。

## 配置文件说明

- config_secret_example.py - 配置文件模板
- config_secret.py - 存储你的账号密码(此文件已被.gitignore忽略)

## 注意事项

1. 请勿将config_secret.py文件上传到任何代码仓库
2. 生成的日志文件login账号.log包含敏感信息，请妥善保管
3. 本项目仅适用于广西科技师范学院校园网

## 贡献指南
欢迎通过 Merge Request 提交改进：
1. Fork 本项目
2. 创建特性分支 (git checkout -b feature/新功能)
3. 提交修改 (git commit -am '添加新功能')
4. 推送分支 (git push origin feature/新功能)
5. 创建 Merge Request

## 许可证

[MIT License](https://gitee.com/quanmian/GKS-schoolnet-login/blob/master/LICENSE)

