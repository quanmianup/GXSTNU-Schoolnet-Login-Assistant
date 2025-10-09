# 广西科师校园网自动登录助手

<img alt="Python" src="https://img.shields.io/badge/Python-3.11-blue"/>
<img alt="PySide6" src="https://img.shields.io/badge/PySide6-GUI-orange"/>
<img alt="Windows" src="https://img.shields.io/badge/Windows-10/11-green"/>


这是一个专为广西科技师范学院校园网设计的自动登录/注销工具，提供图形用户界面，支持账号密码加密存储、详细的日志记录功能以及独立的自动登录EXE生成。通过简单直观的操作，帮助学生和教职工快速连接校园网络，提高网络使用效率。

## 功能特性

- 📶 **自动检测**：实时监测网络连接状态，及时发现网络中断情况
- 🔄 **自动登录**：一键登录校园网，支持自定义账号密码，可保存常用账号
- 🚪 **自动注销**：安全退出当前账号，防止账号被他人误用
- 🔒 **密码加密**：使用AES加密算法保护账号密码安全存储，防止信息泄露
- 📊 **详细日志**：记录所有操作和网络状态变化，支持右键菜单清空日志，便于问题排查
- 🖥️ **友好界面**：基于PySide6的现代化图形界面，简洁易用，符合用户操作习惯
- 📱 **独立EXE生成**：一键生成独立的自动登录可执行文件，无需安装Python环境，方便在多台设备使用
- ⚡ **异步处理**：所有网络操作均使用异步任务执行器，保证界面流畅，避免卡顿
- 🔄 **重试机制**：内置智能重试机制，在网络不稳定时提高登录成功率
- 🎯 **任务管理**：支持计划任务的创建、查询和删除，实现定时自动登录

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
- 使用uv管理Python虚拟环境（推荐）

### 准备工作

1. 确保所有Python项目保存在`F:\code\py`目录下

2. 克隆项目到本地（可选择任一仓库）：
   ```powershell
   cd F:\code\py
   # 从Gitee克隆（国内速度较快）
   git clone https://gitee.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant.git
   # 或从GitHub克隆
   # git clone https://github.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant.git
   cd schoolnet
   ```

3. 创建并激活虚拟环境：
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. 使用uv安装项目依赖（推荐）：
   ```powershell
   uv pip install -r requirements.txt
   ```
   
   如果没有安装uv，也可以使用pip：
   ```powershell
   pip install -r requirements.txt
   ```

5. 首次运行时，程序会提示您输入校园网账号和密码，这些信息将被加密存储在本地配置文件中

### 运行方式

直接运行主程序：

```powershell
python run.py
```

## 使用指南

### 基本操作

1. **启动程序**：运行可执行文件
2. **登录**：在界面中输入校园网账号和密码，点击"登录"按钮
3. **注销**：如需退出网络，点击"注销"按钮退出当前账号
4. **清空日志**：右键点击日志区域，选择"清空日志"选项可清除所有日志信息
5. **最小化**：点击最小化按钮，程序会缩小到系统托盘区域继续运行

### 生成独立EXE

1. 在主界面中输入校园网账号和密码
2. 点击"生成自动登录EXE"按钮
3. 等待程序完成打包过程（可能需要数分钟）
4. 生成成功后，会弹出提示窗口显示生成的文件路径
5. 生成的EXE文件默认保存在`C:\ScheduledTasks`目录下，可直接运行无需Python环境

### 计划任务管理

1. **创建计划任务**：点击"创建计划任务"按钮，在弹出的对话框中设置任务名称、触发条件（如开机启动、定时执行）等参数，完成后点击"确定"按钮
2. **查询任务**：点击"查询任务"按钮，系统会显示所有已创建的与本程序相关的计划任务列表
3. **删除任务**：在任务列表中选择要删除的任务，点击"删除任务"按钮即可移除不需要的任务

### 系统托盘功能

程序最小化到系统托盘后，右键点击托盘图标可执行以下操作：
- **显示主窗口**：恢复程序主界面
- **立即登录**：无需打开主界面，直接执行登录操作
- **立即注销**：无需打开主界面，直接执行注销操作
- **退出程序**：完全退出程序

## 项目结构

项目采用模块化设计，将核心功能、界面展示和开发工具分离，便于维护和扩展。主要模块包括：

```
schoolnet/
├── src/                 # 源代码目录
│   ├── core/            # 核心功能模块（业务逻辑实现）
│   │   ├── AsyncTaskExecutor.py  # 异步任务执行器，处理网络请求等耗时操作
│   │   ├── AutoLoginScript.py    # 自动登录脚本，实现无界面登录功能
│   │   ├── Credentials.py        # 凭证管理，负责账号密码加密存储
│   │   ├── NetworkManager.py     # 网络连接和认证管理，处理网络请求和登录逻辑
│   │   ├── TaskScheduler.py      # 任务调度器，管理Windows计划任务
│   │   └── __init__.py
│   ├── gui/             # 图形界面模块（用户交互界面）
│   │   ├── PswdInput_ui.py       # 密码输入UI组件
│   │   ├── __init__.py
│   │   ├── main_gui_program.py   # 主界面程序，整合各UI组件和业务逻辑
│   │   ├── main_ui.py            # UI界面定义，由Qt Designer生成
│   │   └── window_rc.py          # 窗口资源文件，包含图标、图片等
│   ├── tool/            # 开发工具脚本（辅助开发和构建）
│   │   ├── README_PYSIDE_TOOLS.md   # PySide工具使用说明
│   │   ├── build_auto_login.ps1     # PowerShell构建自动登录EXE脚本
│   │   ├── build_auto_login.py      # Python构建自动登录EXE脚本
│   │   ├── build_main_ui.ps1        # PowerShell构建主界面EXE脚本
│   │   ├── build_main_ui.py         # Python构建主界面EXE脚本
│   │   ├── run_designer.ps1         # 启动Qt Designer设计器脚本
│   │   └── run_ui_rcc_converter.py  # UI和RCC文件转换工具
│   └── utils/           # 工具函数（通用功能模块）
│       ├── __init__.py
│       └── logger.py    # 日志配置，实现统一的日志记录功能
├── assets/              # 资源文件
│   ├── images/          # 界面图片资源
│   │   ├── QC.jpg
│   │   ├── close.png
│   │   ├── dislogin.png
│   │   ├── internet.png
│   │   ├── login.png
│   │   ├── main.png
│   │   ├── main_icon.ico
│   │   ├── minizing.png
│   │   ├── network.png
│   │   ├── 关.png
│   │   └── 开关.png
│   └── qtfile/          # Qt设计源文件
│       ├── PswdInput.ui    # 密码输入界面设计文件
│       ├── main.ui         # 主界面设计文件
│       └── window.qrc      # Qt资源集合文件
├── .gitignore           # Git忽略文件配置
├── .python-version      # Python版本指定文件
├── LICENSE              # 开源许可证文件
├── README.md            # 项目说明文档
├── pyproject.toml       # 项目元数据配置文件
├── requirements.txt     # 项目依赖包列表
├── run.py               # 主程序入口脚本
└── uv.lock              # uv依赖锁定文件
```

## 常见问题与解决方案

### 登录失败

**问题现象**：点击登录按钮后，程序提示登录失败或无响应

**解决方案**：
1. 检查账号密码是否正确，注意区分大小写
2. 确认校园网是否正常运行（尝试使用浏览器直接登录）
3. 检查防火墙设置，确保程序可以访问网络
4. 如果网络不稳定，尝试增加重试次数（程序会自动重试）

### 无法生成EXE文件

**问题现象**：点击"生成自动登录EXE"后，程序提示生成失败

**解决方案**：
1. 确保已安装PyInstaller：`pip install pyinstaller`
2. 检查系统磁盘空间是否充足
3. 确认用户具有管理员权限运行程序
4. 关闭安全软件，部分安全软件可能会阻止EXE打包过程

### 计划任务不生效

**问题现象**：创建的计划任务没有按时执行

**解决方案**：
1. 检查任务设置是否正确，特别是触发条件和执行时间
2. 确认系统是否已启用"Task Scheduler"服务
3. 尝试以管理员身份运行程序并重新创建任务
4. 检查任务的操作路径是否正确

### 程序启动时报错

**问题现象**：程序启动时显示错误消息，无法正常运行

**解决方案**：
1. 确保已安装所有依赖项：`pip install -r requirements.txt`
2. 检查Python版本是否为3.11或更高版本
3. 如果提示缺少某个模块，尝试单独安装该模块
4. 对于"No module named 'window_rc'"错误，确保已正确转换Qt资源文件

### 日志文件过大

**问题现象**：日志文件占用过多磁盘空间

**解决方案**：
1. 右键点击日志区域，选择"清空日志"选项
2. 手动删除`c:\ScheduledTasks\logs`目录下的日志文件
3. 定期清理日志文件以节省磁盘空间

### 系统托盘图标不显示

**问题现象**：程序最小化后，系统托盘中看不到程序图标

**解决方案**：
1. 检查Windows任务栏设置，确保系统托盘图标已显示
2. 尝试重新启动程序
3. 确认Windows系统版本兼容性（推荐Windows 10/11）

## 安全注意事项

1. 🔐 账号密码使用AES加密算法存储在本地，确保数据安全
2. 📝 日志文件默认保存在`c:\ScheduledTasks\logs`目录下，文件名包含用户名信息，请妥善管理
3. ⚠️ 请勿将包含敏感信息的文件上传到代码仓库，避免信息泄露
4. 🔒 项目已配置`.gitignore`文件忽略敏感配置和日志文件，确保代码安全
5. 🛡️ 生成的EXE文件包含加密的账号信息，请妥善保管，不要分享给他人
6. 🔑 定期更新账号密码，以提高账号安全性
7. 🚫 避免在公共设备上使用此工具，或使用后及时清理敏感数据

## 错误处理

程序包含完善的错误处理机制，遇到问题时会：

1. 在日志区域显示详细的错误信息，帮助用户快速定位问题
2. 弹出错误提示对话框，提供简洁明了的错误描述
3. 自动恢复界面状态，确保程序可以继续使用而不会崩溃
4. 对于网络请求错误，内置重试机制和超时处理
5. 记录完整的错误堆栈信息到日志文件，便于开发人员排查问题

## 开发说明

如果您想参与项目开发或修改UI界面，请参考`src/tool/README_PYSIDE_TOOLS.md`文件中的说明，使用提供的工具脚本进行开发工作。

### 开发流程

1. **环境准备**
   ```powershell
   # 克隆仓库
   git clone https://gitee.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant.git
   cd schoolnet
   
   # 创建虚拟环境
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   
   # 安装开发依赖
   uv pip install -r requirements.txt
   ```

2. **UI修改流程**
   ```powershell
   # 启动Qt Designer
   cd src/tool
   .\run_designer.ps1
   
   # 修改完成后，转换UI文件
   python .\run_ui_rcc_converter.py
   ```

3. **代码开发**
   - 遵循项目现有的代码风格和命名规范
   - 为新功能添加适当的文档注释
   - 确保代码能够正常运行并通过基本测试

### 提交流程

1. 创建新的分支进行开发
2. 提交代码前确保通过基本功能测试
3. 提交时编写清晰的提交信息
4. 推送到远程仓库并创建Pull Request

## 版本历史

### v1.0.0 (初始版本)
- 实现校园网自动登录/注销功能
- 提供图形用户界面
- 支持账号密码加密存储
- 实现详细的日志记录功能
- 支持生成独立的自动登录EXE
- 实现任务计划的创建、查询和删除

### v1.1.0 (功能增强)
- 优化网络连接检测机制，提高网络状态判断准确性
- 增强错误处理和重试机制，提升不稳定网络环境下的使用体验
- 改进UI界面，提升用户体验和界面响应速度
- 添加系统托盘功能，支持最小化到托盘并提供快捷操作
- 完善日志管理功能，增强日志记录的详细程度和可读性

## 许可证

本项目采用 [MIT License](LICENSE) 开源协议
