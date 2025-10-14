# 广西科师校园网自动登录助手

<img alt="Python" src="https://img.shields.io/badge/Python-3.11-blue"/>
<img alt="PySide6" src="https://img.shields.io/badge/PySide6-GUI-orange"/>
<img alt="Windows" src="https://img.shields.io/badge/Windows-10/11-green"/>
<img alt="uv" src="https://img.shields.io/badge/uv-0.8.15-purple"/>

这是一个专为广西科技师范学院校园网设计的自动登录/注销工具，提供图形用户界面，支持账号密码加密存储、详细的日志记录功能以及独立的自动登录EXE生成。通过简单直观的操作，帮助学生和教职工快速连接校园网络，提高网络使用效率。

## 下载

最新下载地址：[点击我](https://gitee.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant/releases/latest)

## 界面展示

### 首页

![首页](/assets/ReadmeFile/首页.png)

### 定时任务管理

![定时任务管理](/assets/ReadmeFile/定时任务管理.png)

## 使用说明

### 使用环境

必须Windows10及以上版本，Python底层不支持win7及以下，所以无解。

### 使用方法

#### 1. 首页操作

- **1.1 登录/下线功能**  
  单击首页标签，在输入框输入账号密码，点击“登录”/“下线”按钮连接/下线校园网；勾选“记住密码”可在下次打开程序时，自动输入账号信息。
- **1.2 生成一键登录文件**  
  点击“生成一键登录文件”按钮可以在 `C:\ScheduledTasks` 文件夹下生成 `AutoLoginScript.exe`
  文件，双击这个文件可以自动登录校园网（要求至少在首页登录过一次并勾选“**记住密码**”选项，确保在打开程序时能**自动填写账号密码
  **）。
- **1.3 保持网络在线**  
  程序会每 5 秒自动检测网络连接状态，点击“保持网络在线”按钮可开启保持网络在线功能，在 **7:00 - 24:00**
  时间段若检测到网络未连接，会尝试自动登录校园网。
- **1.4 日志查看**  
  右侧日志区域显示操作记录，右键点击可打开“清空输出”菜单。

#### 2. 定时任务管理

切换到“定时任务管理”标签页，可创建、删除和查询定时任务。

- **2.1 定时任务使用说明**
- 将 `AutoLoginScript.exe` 文件加入定时任务可实现定时登录校园网功能。
- 首先设置需要定时启动的时间，随后点击“选择文件”按钮选择需要定时执行的文件，比如 `C:\ScheduledTasks\AutoLoginScript.exe`
  ，点击“创建任务”按钮即可。
- 删除任务需要先选中任务，再单击“删除任务”按钮即可。

### 常见问题

- **登录失败**：检查账号密码和网络连接，确定网关 IP 为 `172.16.x.x`，查看日志获取错误原因。
- **任务不执行**：确认 EXE 文件路径正确，检查 Windows 任务计划程序设置。

### 注意事项

- 账号密码使用 AES 加密存储。
- 生成的 EXE 文件包含账号信息，请妥善保管。
- 日志保存在 `c:\ScheduledTasks\logs` 目录。

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
- **uv** - Python包管理工具
- **PySide6** - 图形用户界面框架
- **Requests** - 网络请求处理
- **PyCryptodome** - 密码加密功能
- **Loguru** - 日志管理
- **PyInstaller** - EXE打包工具

## 开发指南

如果您想参与项目开发或修改UI界面，请参考`src/tool/README_PYSIDE_TOOLS.md`文件中的说明，使用提供的工具脚本进行开发工作。

### 前置要求

- Windows 10/11 64位系统
- Python 3.11.5 或更高版本
- 使用uv管理Python虚拟环境（推荐）

### 准备工作

1. 安装uv（可选，uv为高性能项目管理工具）：
   ```powershell
   pip install uv
   ```

2. 克隆项目到本地（可选择任一仓库）：
   ```powershell
   # 从Gitee克隆（国内速度较快）
   git clone https://gitee.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant.git
   # 或从GitHub克隆
   # git clone https://github.com/quanmianup/GXSTNU-Schoolnet-Login-Assistant.git
   cd GXSTNU-Schoolnet-Login-Assistant

   # 创建并激活虚拟环境
   python -m venv .venv
   .venv\Scripts\activate

   # 安装开发依赖
   uv pip install -r requirements.txt

   #  如果没有安装uv，也可以使用pip：
   # pip install -r requirements.txt
   ```

3. **UI修改流程**
   ```powershell
   # 启动Qt Designer
   cd src/tool
   .\run_designer.ps1

   # 使用Qt Designer修改UI文件
   # 完成后，保存UI文件（默认在assets/qtfile/目录下）
   
   # 修改完成后，转换UI文件
   python .\run_ui_rcc_converter.py
   ```
4. **代码开发**
    - 遵循项目现有的代码风格和命名规范
    - 为新功能添加适当的文档注释
    - 确保代码能够正常运行并通过基本测试

### 项目启动

直接运行主程序：

```powershell
python run.py
```

### 打包命令

发行版默认采用 Pyinstaller 进行打包

运行打包脚本：
```powershell
python .\src\tool\build_main_ui.py
```

这将在项目根目录下的`dist`文件夹中生成两个独立的可执行文件`GXSTNU-Schoolnet-Login-Assistant.exe`
和`AutoLoginScript.exe`。

### 提交流程

1. 创建新的分支进行开发
2. 提交代码前确保通过基本功能测试
3. 提交时编写清晰的提交信息
4. 推送到远程仓库并创建Pull Request

## 项目结构

项目采用模块化设计，将核心功能、界面展示和开发工具分离，便于维护和扩展。主要模块包括：

```
schoolnet/
├── assets/
│   ├── ReadmeFile/
│   │   ├── 定时任务管理.png
│   │   └── 首页.png
│   ├── images/
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
│   ├── qtfile/
│       ├── PswdInput.ui
│       ├── main.ui
│       └── window.qrc
├── src/
│   ├── core/
│   │   ├── AsyncTaskExecutor.py  # 异步任务执行器，处理网络请求等耗时操作
│   │   ├── AutoLoginScript.py    # 自动登录脚本，实现无界面登录功能
│   │   ├── Credentials.py        # 凭证管理，负责账号密码加密存储
│   │   ├── NetworkManager.py     # 网络连接和认证管理，处理网络请求和登录逻辑
│   │   ├── TaskScheduler.py      # 任务调度器，管理Windows计划任务
│   │   └── __init__.py
│   ├── gui/
│   │   ├── PswdInput_ui.py       # 密码输入UI组件
│   │   ├── __init__.py
│   │   ├── main_gui_program.py   # 主界面程序，整合各UI组件和业务逻辑
│   │   ├── main_ui.py            # UI界面定义，由Qt Designer生成
│   │   └── window_rc.py          # 窗口资源文件，包含图标、图片等
│   ├── tool/
│   │   ├── README_PYSIDE_TOOLS.md   # PySide工具使用说明
│   │   ├── build_auto_login.ps1     # PowerShell构建自动登录EXE脚本
│   │   ├── build_auto_login.py      # Python构建自动登录EXE脚本
│   │   ├── build_main_ui.ps1        # PowerShell构建主界面EXE脚本
│   │   ├── build_main_ui.py         # Python构建主界面EXE脚本
│   │   ├── run_designer.ps1         # 启动Qt Designer设计器脚本
│   │   ├── run_ui_rcc_converter.py  # UI和RCC文件转换工具
│   │   └── schtasks_params_guide.md
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py    # 日志配置，实现统一的日志记录功能
│   └── __init__.py
├── LICENSE              # 开源许可证文件
├── README.md            # 项目说明文档
├── pyproject.toml       # 项目元数据配置文件
├── requirements.txt     # 项目依赖包列表
└── run.py               # 主程序入口脚本
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

## 许可证

本项目采用 [MIT License](LICENSE) 开源协议

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=quanmianup/GXSTNU-Schoolnet-Login-Assistant&type=date&legend=top-left)](https://www.star-history.com/#quanmianup/GXSTNU-Schoolnet-Login-Assistant&type=date&legend=top-left)