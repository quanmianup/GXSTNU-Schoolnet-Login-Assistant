# PySide6 工具脚本使用说明

本文档介绍了广西科师校园网登录助手项目中使用的PySide6工具脚本，用于简化Qt界面设计和资源文件转换工作流程。

## 工具脚本概述

项目提供了三个PowerShell脚本，用于管理Qt UI设计和资源文件：

- **run_designer.ps1** - 启动Qt Designer设计器，用于可视化创建和编辑UI界面
- **run_uic.ps1** - 将Qt Designer生成的.ui文件转换为Python代码文件
- **run_rcc.ps1** - 将Qt资源文件(.qrc)转换为Python代码文件

所有脚本均使用英文注释和输出，确保在不同编码环境下正常运行。

## 脚本功能说明

### 1. 自动查找项目根目录

所有脚本都包含一个`Find-ProjectRoot`函数，能够自动通过查找`pyproject.toml`文件来确定项目的根目录，无需硬编码路径。

这种设计使得脚本可以在项目内的任何位置运行，提高了开发便利性。

### 2. 工具路径自动配置

脚本会根据找到的项目根目录，自动构建PySide6工具的完整路径：

```powershell
$toolPath = Join-Path -Path $projectRoot -ChildPath ".venv\Scripts\pyside6-[tool].exe"
```

### 3. 错误处理机制

脚本包含完整的错误处理机制，包括：
- 检查工具是否存在
- 检查文件路径有效性
- 提供清晰的错误信息输出

## 使用方法

### 前置条件

- 已在项目中创建虚拟环境 `.venv`
- 已安装 PySide6 包：`uv pip install PySide6`
- 当前系统为 Windows 操作系统

### 启动Qt Designer

运行脚本启动Qt Designer界面设计器：
  
 ```powershell
 .\run_designer.ps1
 ```

此脚本会：
- 在后台启动Qt Designer（不显示控制台窗口）
- 自动查找并使用虚拟环境中的PySide6 Designer工具

### 转换UI文件

运行脚本将.ui文件转换为Python代码文件：
 
 ```powershell
 .\run_uic.ps1
 ```

此脚本会：
- 自动查找`assets/qtfile`目录下的所有.ui文件
- 将它们转换为Python文件并保存到`src/gui`目录
- 显示转换成功/失败的统计信息

也可以指定特定的.ui文件：

```powershell
 .\run_uic.ps1 "path/to/specific.ui"
 ```

### 转换资源文件

运行脚本将.qrc资源文件转换为Python代码文件：
 
 ```powershell
 .\run_rcc.ps1
 ```

此脚本会：
- 自动查找`assets/qtfile`目录下的所有.qrc文件
- 将它们转换为Python资源文件并保存到`src/gui`目录
- 显示转换成功/失败的统计信息

也可以指定特定的.qrc文件：

```powershell
 .\run_rcc.ps1 "path/to/specific.qrc"
 ```

## 项目文件结构关系

```
schoolnet/
├── src/
│   ├── gui/             # 转换后的Python UI文件存放位置
│   └── tool/            # 本脚本所在目录
├── assets/
│   └── qtfile/          # Qt设计文件(.ui, .qrc)存放位置
└── .venv/               # 虚拟环境，包含PySide6工具
```

## 注意事项

1. 所有脚本需要在Windows PowerShell环境中运行
2. 确保已在虚拟环境中安装了PySide6包
3. 转换后的文件将按照原始文件名命名，后缀分别为`_ui.py`(UI文件)和`_rc.py`(资源文件)
4. 为了获得最佳性能，建议在转换大量文件时单独指定文件而非转换全部文件

## 开发提示

### 脚本扩展建议

1. **添加批量转换功能**：可以考虑增加转换特定目录下所有文件的选项
2. **自定义输出目录**：允许用户指定转换后的文件保存位置
3. **增加日志记录**：添加日志文件记录转换过程，便于排查问题

### 其他脚本功能

- **自动查找文件**：默认处理`assets/qtfile`目录下的所有.ui和.qrc文件
- **自定义文件路径**：支持通过命令行参数指定具体的文件路径
- **输出目录创建**：自动创建`src/gui`输出目录（如果不存在）
- **转换结果统计**：提供转换成功和失败的文件数量统计

### 附加注意事项

1. 所有工具脚本应在项目根目录下运行以确保正常工作
2. 转换后的Python文件将自动保存到`src/gui`目录
3. 如果需要重新生成UI文件，直接运行相应脚本即可覆盖旧文件

## 常见问题解决

- **找不到工具错误**：确保已在虚拟环境中安装PySide6，可通过`pip install pyside6`命令安装
- **文件转换失败**：检查源文件格式是否正确，路径中是否包含特殊字符
- **中文显示问题**：如果需要中文显示，可能需要额外配置PowerShell的编码设置
- **权限问题**：如果遇到执行权限问题，可以使用`powershell -ExecutionPolicy Bypass -File 脚本名.ps1`命令运行脚本