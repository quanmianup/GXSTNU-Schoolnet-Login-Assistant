# PySide6工具脚本说明

# PySide6 工具使用指南

本文档详细介绍广西科师校园网登录助手项目中用于Qt界面设计和资源文件转换的工具脚本，帮助开发人员快速掌握UI开发流程。

## 工具概述

项目提供两类脚本工具，用于简化Qt界面开发和构建过程：

### PowerShell脚本（Windows专用）
- **run_designer.ps1** - 自动查找并启动Qt Designer设计器
- **build_auto_login.ps1** - 构建自动登录可执行文件
- **build_main_ui.ps1** - 构建主界面可执行文件

### Python脚本（跨平台兼容）
- **run_ui_rcc_converter.py** - 整合工具，一次性转换所有.ui和.qrc文件
- **build_auto_login.py** - 构建自动登录可执行文件的Python实现
- **build_main_ui.py** - 构建主界面可执行文件的Python实现

## 核心功能

所有脚本均支持：
- 自动通过pyproject.toml查找项目根目录
- 自动定位虚拟环境中的PySide6工具
- 转换后的文件保存在src/gui目录

Python脚本特有优势：
- 跨平台兼容（支持Windows、macOS、Linux）
- 统一的转换结果统计和错误处理
- 更详细的日志输出和进度反馈

## 工具详解

### 1. Qt Designer启动工具

**脚本文件**：run_designer.ps1（Windows）

**功能**：自动查找虚拟环境中的Qt Designer并启动，用于设计UI界面

**工作原理**：
- 自动检测虚拟环境位置
- 查找PySide6设计器可执行文件
- 定位项目的Qt设计文件目录
- 启动Qt Designer并加载相关资源

### 2. UI和RCC文件转换工具

**脚本文件**：run_ui_rcc_converter.py（跨平台）

**功能**：将Qt设计的.ui文件转换为Python代码，将.qrc资源文件转换为Python资源模块

**支持的文件**：
- .ui文件：Qt界面设计文件，转换为Python UI模块
- .qrc文件：Qt资源集合文件，转换为Python资源模块

**工作原理**：
- 使用`pyside6-uic`工具将.ui文件转换为Python代码
- 使用`pyside6-rcc`工具将.qrc文件转换为Python代码
- 自动处理文件路径和输出目录

### 3. 可执行文件构建工具

**脚本文件**：
- build_auto_login.py（自动登录EXE构建）
- build_main_ui.py（主界面EXE构建）

**功能**：使用PyInstaller将Python脚本打包为独立的可执行文件

**构建特性**：
- 单文件打包（所有依赖项整合到一个EXE中）
- 包含应用图标
- 无控制台窗口（静默运行）
- 自动处理资源文件

## 使用方法

### 前置条件
- 已创建虚拟环境.venv
- 已安装PySide6：`uv pip install PySide6`
- Python脚本需要Python 3.11或更高版本
- PowerShell脚本需要Windows PowerShell 5.0或更高版本

### 启动Qt Designer

在Windows系统中，使用PowerShell脚本启动Qt Designer：

```powershell
cd src/tool
.
un_designer.ps1
```

### 转换UI和资源文件（推荐）

使用Python脚本一次性转换所有UI和资源文件（跨平台兼容）：

```powershell
cd src/tool
python run_ui_rcc_converter.py
```

**脚本输出示例**：
```
开始转换UI和资源文件...
正在查找项目根目录...
项目根目录: F:\code\py\schoolnet
正在查找虚拟环境...
虚拟环境: F:\code\py\schoolnet\.venv
正在转换 F:\code\py\schoolnet\assets\qtfile\main.ui -> F:\code\py\schoolnet\src\gui\main_ui.py
转换成功: main.ui -> main_ui.py
正在转换 F:\code\py\schoolnet\assets\qtfile\PswdInput.ui -> F:\code\py\schoolnet\src\gui\PswdInput_ui.py
转换成功: PswdInput.ui -> PswdInput_ui.py
正在转换 F:\code\py\schoolnet\assets\qtfile\window.qrc -> F:\code\py\schoolnet\src\gui\window_rc.py
转换成功: window.qrc -> window_rc.py
转换完成! 成功: 3, 失败: 0
```

### 构建可执行文件

构建主界面可执行文件：

```powershell
cd src/tool
python build_main_ui.py
```

构建自动登录可执行文件：

```powershell
cd src/tool
python build_auto_login.py
```

**构建过程说明**：
1. 脚本会自动检测项目根目录和虚拟环境
2. 收集必要的源文件和资源
3. 调用PyInstaller进行打包
4. 生成的可执行文件会保存在指定目录

## 项目文件结构

```
schoolnet/
├── src/
│   ├── gui/         # 转换后的Python文件（自动生成，请勿手动修改）
│   └── tool/        # 脚本所在目录
├── assets/
│   ├── images/      # 图片资源文件
│   └── qtfile/      # .ui和.qrc文件存放位置（设计源文件）
└── .venv/           # 虚拟环境（包含PySide6工具）
```

**重要注意事项**：
- `src/gui`目录下的`*_ui.py`和`*_rc.py`文件是自动生成的，**请勿手动修改**，否则下次转换时会被覆盖
- 所有UI修改应在Qt Designer中进行，然后重新转换
- 资源文件（如图标、图片）应放在`assets/images`目录下，并在`.qrc`文件中引用

## 常见问题与解决方案

### 1. 找不到工具

**问题现象**：运行脚本时提示找不到PySide6相关工具

**解决方案**：
- 确保已在虚拟环境中安装PySide6：`pip install pyside6`
- 确认虚拟环境已正确激活：`.venv\Scripts\Activate.ps1`
- 检查pyproject.toml文件是否存在于项目根目录

### 2. 文件转换失败

**问题现象**：运行转换脚本时提示转换失败

**解决方案**：
- 检查源文件格式是否正确，路径中是否包含特殊字符
- 确认.ui或.qrc文件没有语法错误
- 尝试使用Qt Designer打开文件，检查是否能正常加载

### 3. 权限问题

**问题现象**：运行脚本时出现权限错误

**解决方案**：
- Windows PowerShell：以管理员身份运行PowerShell，或使用以下命令：
  ```powershell
  powershell -ExecutionPolicy Bypass -File 脚本名.ps1
  ```
- Linux/macOS：
  ```bash
  chmod +x run_ui_rcc_converter.py
  python run_ui_rcc_converter.py
  ```

### 4. 构建EXE失败

**问题现象**：打包可执行文件时出现错误

**解决方案**：
- 确保已安装PyInstaller：`pip install pyinstaller`
- 检查磁盘空间是否充足
- 关闭可能阻止打包的安全软件
- 查看详细的错误输出，定位具体问题

### 5. 转换后的文件与预期不符

**问题现象**：转换后的Python文件与.ui文件内容不匹配

**解决方案**：
- 确认使用的是正确版本的PySide6工具
- 尝试删除旧的转换文件，重新运行转换脚本
- 检查.ui文件是否有损坏或格式错误

## 开发最佳实践

1. **UI设计与代码分离**
   - 所有界面设计应在Qt Designer中完成
   - 业务逻辑代码应写在单独的Python文件中，不要直接修改自动生成的UI文件
   - 使用信号和槽机制连接UI事件和业务逻辑

2. **资源管理**
   - 所有图片、图标等资源应放在`assets/images`目录
   - 使用`.qrc`文件集中管理资源引用
   - 每次修改资源后，重新运行转换脚本

3. **版本控制**
   - 将`.ui`和`.qrc`文件纳入版本控制
   - 不要将自动生成的`*_ui.py`和`*_rc.py`文件纳入版本控制
   - 在`.gitignore`中添加相应的忽略规则

4. **团队协作**
   - 团队成员应使用相同版本的PySide6工具
   - 修改UI前，确保已获取最新版本的`.ui`文件
   - 修改后，及时提交更新的`.ui`文件

## 高级功能

### 自定义转换参数

如果需要自定义PySide6转换工具的参数，可以修改`run_ui_rcc_converter.py`文件中的相关配置。例如：

```python
# 自定义uic转换参数
euic_args = ['--from-imports']

# 自定义rcc转换参数
rcc_args = ['--compress', '9']
```

### 批量处理多个项目

可以扩展脚本，使其支持批量处理多个项目的UI和资源文件，适用于大型项目或多个相关项目的管理。

### 集成到开发工作流

将转换脚本集成到项目的构建系统或CI/CD流程中，确保每次构建时都使用最新的UI和资源文件。

## 更新日志

### v1.0.0
- 初始版本，包含基本的UI转换和构建功能

### v1.1.0
- 增加了Python版本的跨平台工具
- 完善了错误处理和日志输出
- 添加了自动查找项目根目录功能

### v1.2.0
- 优化了构建可执行文件的脚本
- 增加了更多的配置选项
- 完善了文档和使用说明