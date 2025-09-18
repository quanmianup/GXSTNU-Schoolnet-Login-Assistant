# 广西科师校园网自动登录助手

<img alt="Python" src="https://img.shields.io/badge/Python-3.11-blue"/>
<img alt="PySide6" src="https://img.shields.io/badge/PySide6-GUI-orange"/>
<img alt="Windows" src="https://img.shields.io/badge/Windows-10/11-green"/>


这是一个专为广西科技师范学院校园网设计的自动登录/注销工具，提供图形用户界面，支持账号密码加密存储、详细的日志记录功能以及独立的自动登录EXE生成。

## 功能特性

- 📶 **自动检测**：实时监测网络连接状态
- 🔄 **自动登录**：一键登录校园网，支持自定义账号密码
- 🚪 **自动注销**：安全退出当前账号
- 🔒 **密码加密**：使用AES加密算法保护账号密码安全存储
- 📊 **详细日志**：记录所有操作和网络状态变化，支持右键菜单清空日志
- 🖥️ **友好界面**：基于PySide6的现代化图形界面
- 📱 **独立EXE生成**：一键生成独立的自动登录可执行文件，无需安装Python环境
- ⚡ **异步处理**：所有网络操作均使用异步任务执行器，保证界面流畅
- 🔄 **重试机制**：内置智能重试机制，提高登录成功率
- 🎯 **任务管理**：支持计划任务的创建、查询和删除

## 技术栈

- **Python 3.11** - 主要开发语言
- **PySide6** - 图形用户界面框架
- **Requests** - 网络请求处理
- **PyCryptodome** - 密码加密功能
- **Loguru** - 日志管理
- **uv** - Python包管理工具
- **PyInstaller** - EXE打包工具

## 快速开始

### 前置要求
- Windows 10/11 64位系统
- Python 3.11.5 或更高版本
- 使用uv管理Python虚拟环境

### 准备工作

1. 确保所有Python项目保存在`F:\code\py`目录下

2. 克隆项目到本地：
   ```powershell
   cd F:\code\py
   git clone [项目仓库地址]
   cd schoolnet
   ```

3. 创建并激活虚拟环境：
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. 使用uv安装项目依赖：
   ```powershell
   uv pip install -r requirements.txt
   ```

5. 运行初始化脚本生成配置文件：
   ```powershell
   python -m config.init_key
   ```

6. 首次运行时，程序会提示您输入校园网账号和密码，这些信息将被加密存储

### 运行方式

直接运行主程序：

```powershell
python run.py
```

## 使用指南

### 基本操作

1. **登录**：输入账号密码，点击"登录"按钮
2. **注销**：点击"注销"按钮退出当前账号
3. **清空日志**：右键点击日志区域，选择"清空日志"选项

### 生成独立EXE

1. 输入账号密码
2. 点击"生成自动登录EXE"按钮
3. 等待程序完成打包过程
4. 生成的EXE文件将保存在`task_folder`目录下

### 计划任务管理

1. 点击"创建计划任务"可以设置定时自动登录
2. 点击"查询任务"查看已创建的计划任务列表
3. 在任务列表中选择任务后点击"删除任务"可以移除不需要的任务

## 项目结构

```
schoolnet/
├── src/                 # 源代码目录
│   ├── core/            # 核心功能模块
│   │   ├── network.py   # 网络连接和认证管理
│   │   └── AsyncTaskExecutor.py  # 异步任务执行器
│   ├── gui/             # 图形界面模块
│   │   ├── main_gui_program.py  # 主界面程序
│   │   └── main_ui.py   # UI界面定义
│   ├── utils/           # 工具函数
│   │   ├── logger.py    # 日志配置
│   │   └── task_manager.py  # 任务管理
│   └── tool/            # 开发工具脚本
├── config/              # 配置文件
│   ├── credentials.py   # 凭证管理
│   └── init_key.py      # 密钥初始化
├── assets/              # 资源文件
│   ├── images/          # 界面图片
│   └── qtfile/          # Qt设计文件
├── run.py               # 主程序入口
└── requirements.txt     # 项目依赖列表
```

## 安全注意事项

1. 🔐 账号密码使用AES加密算法存储在本地
2. 📝 日志文件默认保存在`logs`目录下，文件名包含用户名信息
3. ⚠️ 请勿将包含敏感信息的文件上传到代码仓库
4. 🔒 项目已配置`.gitignore`文件忽略敏感配置和日志文件
5. 🛡️ 生成的EXE文件包含加密的账号信息，请妥善保管，不要分享给他人

## 错误处理

程序包含完善的错误处理机制，遇到问题时会：

1. 在日志区域显示详细的错误信息
2. 弹出错误提示对话框
3. 自动恢复界面状态，确保程序可以继续使用

## 开发说明

如果您想参与项目开发或修改UI界面，请参考`src/tool/README_PYSIDE_TOOLS.md`文件中的说明，使用提供的工具脚本进行开发工作。

## 许可证

本项目采用 [MIT License](LICENSE) 开源协议

