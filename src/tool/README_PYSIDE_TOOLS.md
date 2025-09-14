# PySide6工具脚本说明

本文档介绍广西科师校园网登录助手项目中用于Qt界面设计和资源文件转换的工具脚本。

## 工具概述

项目提供两类脚本工具：

### PowerShell脚本
- **run_designer.ps1** - 启动Qt Designer设计器
- **run_uic.ps1** - 将.ui文件转换为Python代码
- **run_rcc.ps1** - 将.qrc资源文件转换为Python代码

### Python脚本
- **run_ui_rcc_converter.py** - 整合工具，一次性转换所有.ui和.qrc文件

## 核心功能

所有脚本均支持：
- 自动通过pyproject.toml查找项目根目录
- 自动定位虚拟环境中的PySide6工具
- 转换后的文件保存在src/gui目录

Python脚本特有优势：
- 跨平台兼容（支持Windows、macOS、Linux）
- 一个命令完成两种文件类型的转换
- 统一的转换结果统计和错误处理

## 使用方法

### 前置条件
- 已创建虚拟环境.venv
- 已安装PySide6：`uv pip install PySide6`
- Python脚本需要Python 3.11或更高版本

### 启动Qt Designer
```powershell
.
un_designer.ps1
```

### 转换单个文件类型
```powershell
# 转换UI文件
.
un_uic.ps1
# 或指定文件
.
un_uic.ps1 "path/to/specific.ui"

# 转换资源文件
.
un_rcc.ps1
# 或指定文件
.
un_rcc.ps1 "path/to/specific.qrc"
```

### 一次性转换所有文件（推荐）
```powershell
python .\run_ui_rcc_converter.py
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