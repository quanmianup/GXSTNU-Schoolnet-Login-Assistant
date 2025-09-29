# PySide6工具脚本说明

本文档介绍广西科师校园网登录助手项目中用于Qt界面设计和资源文件转换的工具脚本。

## 工具概述

项目提供两类脚本工具：

### PowerShell脚本
- **run_designer.ps1** - 启动Qt Designer设计器
- **build_auto_login.ps1** - 构建自动登录可执行文件
- **build_main_ui.ps1** - 构建主界面可执行文件

### Python脚本
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

## 使用方法

### 前置条件
- 已创建虚拟环境.venv
- 已安装PySide6：`uv pip install PySide6`
- Python脚本需要Python 3.11或更高版本

### 启动Qt Designer
```powershell
./run_designer.ps1
```

### 转换UI和资源文件（推荐）
```powershell
python .\run_ui_rcc_converter.py
```

### 构建可执行文件
构建主界面可执行文件：
```powershell
python .\build_main_ui.py
```

构建自动登录可执行文件：
```powershell
python .\build_auto_login.py
```

## 项目文件结构
```
schoolnet/
├── src/
│   ├── gui/         # 转换后的Python文件
│   └── tool/        # 脚本所在目录
├── assets/
│   └── qtfile/      # .ui和.qrc文件存放位置
└── .venv/           # 虚拟环境
```

## 注意事项
- PowerShell脚本仅支持Windows，Python脚本支持多平台
- 转换后的文件命名规则：原文件名+_ui.py/_rc.py
- 所有脚本可在项目内任何位置运行

## 常见问题

### 找不到工具
确保已在虚拟环境中安装PySide6：`pip install pyside6`

### 文件转换失败
检查源文件格式是否正确，路径中是否包含特殊字符

### 权限问题
- Windows PowerShell：`powershell -ExecutionPolicy Bypass -File 脚本名.ps1`
- Linux/macOS：`chmod +x run_ui_rcc_converter.py`