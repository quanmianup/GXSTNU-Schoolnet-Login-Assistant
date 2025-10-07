# Windows 计划任务参数指南

本文档详细介绍Windows系统中计划任务（Task Scheduler）的参数使用方法，帮助用户理解和配置校园网登录助手的计划任务功能。

## 计划任务概述

Windows计划任务是Windows操作系统的一项功能，允许用户安排程序或脚本在特定时间或事件发生时运行。校园网登录助手利用这一功能，帮助用户设置定时自动登录校园网的任务。

## 计划任务基础

### 任务组成部分

一个完整的计划任务通常包含以下几个部分：
- **任务名称**：任务的唯一标识
- **触发器**：任务启动的条件（时间、事件等）
- **操作**：任务执行的操作（运行程序、脚本等）
- **条件**：任务执行的附加条件
- **设置**：任务的其他配置选项

## schtasks命令详解

Windows提供了`schtasks`命令行工具，用于创建、查询、修改和删除计划任务。校园网登录助手的任务管理功能正是基于这个命令实现的。

### 基本语法

```powershell
schtasks /命令 [/参数1] [/参数2] ...
```

### 常用命令

| 命令 | 描述 |
|------|------|
| `/Create` | 创建新的计划任务 |
| `/Query` | 显示计划任务列表 |
| `/Delete` | 删除计划任务 |
| `/Run` | 立即运行计划任务 |
| `/End` | 停止正在运行的计划任务 |
| `/Change` | 修改计划任务的属性 |

## 主要参数说明

以下是校园网登录助手创建计划任务时常用的参数：

### 创建任务参数 (`/Create`)

| 参数 | 描述 | 示例 |
|------|------|------|
| `/TN` | 指定任务名称 | `/TN "GXSTNU_Schoolnet_Login"` |
| `/TR` | 指定要运行的程序或命令 | `/TR "C:\ScheduledTasks\AutoLogin.exe"` |
| `/SC` | 指定任务的计划频率 | `/SC ONLOGON` (登录时)、`/SC DAILY` (每天) |
| `/ST` | 指定任务开始时间 (24小时制) | `/ST 08:00` |
| `/SD` | 指定任务开始日期 | `/SD 2023/10/01` |
| `/RU` | 指定运行任务的用户账户 | `/RU SYSTEM` (系统账户) |
| `/RL` | 指定任务的运行级别 | `/RL HIGHEST` (最高权限) |
| `/F` | 强制创建任务，覆盖同名任务 | `/F` |
| `/DELAY` | 指定触发后延迟执行的时间 | `/DELAY 0005:00` (5分钟) |

### 查询任务参数 (`/Query`)

| 参数 | 描述 | 示例 |
|------|------|------|
| `/TN` | 指定要查询的任务名称 | `/TN "GXSTNU_Schoolnet_Login"` |
| `/V` | 显示详细任务信息 | `/V` |
| `/FO` | 指定输出格式 | `/FO TABLE` (表格)、`/FO LIST` (列表) |

### 删除任务参数 (`/Delete`)

| 参数 | 描述 | 示例 |
|------|------|------|
| `/TN` | 指定要删除的任务名称 | `/TN "GXSTNU_Schoolnet_Login"` |
| `/F` | 强制删除任务，不提示确认 | `/F` |

## 计划任务类型详解

校园网登录助手支持多种类型的计划任务，以下是常见的几种：

### 1. 登录时执行

**功能**：用户登录Windows系统时自动执行校园网登录

**参数配置**：
```powershell
schtasks /Create /TN "GXSTNU_Schoolnet_Login_OnLogon" /TR "C:\ScheduledTasks\AutoLogin.exe" /SC ONLOGON /RU SYSTEM /RL HIGHEST /F /DELAY 0001:00
```

**适用场景**：每次开机或登录系统后需要自动连接校园网的用户

### 2. 每天定时执行

**功能**：每天在指定时间自动执行校园网登录

**参数配置**：
```powershell
schtasks /Create /TN "GXSTNU_Schoolnet_Login_Daily" /TR "C:\ScheduledTasks\AutoLogin.exe" /SC DAILY /ST 08:00 /RU SYSTEM /RL HIGHEST /F
```

**适用场景**：需要在每天固定时间（如早上8点）自动连接校园网的用户

### 3. 系统启动时执行

**功能**：Windows系统启动时自动执行校园网登录

**参数配置**：
```powershell
schtasks /Create /TN "GXSTNU_Schoolnet_Login_OnStartup" /TR "C:\ScheduledTasks\AutoLogin.exe" /SC ONSTART /RU SYSTEM /RL HIGHEST /F
```

**适用场景**：需要电脑开机后立即连接校园网的用户，无需等待用户登录

### 4. 每隔一段时间执行

**功能**：每隔指定时间重复执行校园网登录

**参数配置**：
```powershell
schtasks /Create /TN "GXSTNU_Schoolnet_Login_Hourly" /TR "C:\ScheduledTasks\AutoLogin.exe" /SC HOURLY /MO 3 /RU SYSTEM /RL HIGHEST /F
```

**适用场景**：校园网连接不稳定，需要定期检查并重新连接的用户

## 高级配置选项

### 1. 设置重复执行

对于某些计划任务，您可能希望在触发后重复执行多次：

```powershell
schtasks /Create /TN "任务名称" /TR "程序路径" /SC DAILY /ST 08:00 /RI 30 /DU 04:00 /RU SYSTEM /RL HIGHEST /F
```

参数说明：
- `/RI 30`：每30分钟重复一次
- `/DU 04:00`：持续4小时

### 2. 设置唤醒计算机

如果需要任务在计算机休眠时唤醒系统执行：

```powershell
schtasks /Create /TN "任务名称" /TR "程序路径" /SC DAILY /ST 08:00 /RU SYSTEM /RL HIGHEST /F /WAKE
```

参数说明：
- `/WAKE`：唤醒计算机执行任务

### 3. 设置运行条件

可以为任务设置附加条件，例如仅在计算机使用交流电源时运行：

```powershell
# 创建任务后修改条件
schtasks /Change /TN "任务名称" /ACPower
```

## 任务计划管理技巧

### 1. 查看任务状态

```powershell
schtasks /Query /TN "GXSTNU_Schoolnet_Login" /V /FO LIST
```

### 2. 立即运行任务

```powershell
schtasks /Run /TN "GXSTNU_Schoolnet_Login"
```

### 3. 导出和导入任务

**导出任务**：
```powershell
schtasks /Query /TN "GXSTNU_Schoolnet_Login" /XML > "D:\task_backup.xml"
```

**导入任务**：
```powershell
schtasks /Create /TN "GXSTNU_Schoolnet_Login_Restored" /XML "D:\task_backup.xml"
```

## 常见问题与解决方案

### 1. 任务创建成功但不执行

**问题现象**：使用校园网登录助手创建计划任务成功，但任务没有在指定时间执行

**解决方案**：
- 检查任务的运行用户权限是否正确，建议使用系统账户（SYSTEM）
- 确认任务的运行级别设置为"最高权限"
- 检查Windows Task Scheduler服务是否正在运行
- 查看任务历史记录，了解失败原因

### 2. 任务执行但登录失败

**问题现象**：计划任务正常执行，但校园网登录失败

**解决方案**：
- 确认生成的AutoLogin.exe文件包含正确的账号信息
- 检查网络连接是否正常
- 手动运行AutoLogin.exe，验证登录功能是否正常
- 查看日志文件了解详细错误信息

### 3. 任务创建失败

**问题现象**：使用校园网登录助手创建计划任务时提示失败

**解决方案**：
- 确保以管理员身份运行校园网登录助手
- 检查任务名称是否已存在，尝试使用不同的任务名称
- 确认`C:\ScheduledTasks`目录存在且可写入
- 查看错误提示信息，针对性解决问题

### 4. 无法删除任务

**问题现象**：尝试删除计划任务时失败

**解决方案**：
- 确保以管理员身份运行校园网登录助手
- 确认任务名称输入正确
- 检查任务是否正在运行，先结束任务再删除
- 使用命令行强制删除：`schtasks /Delete /TN "任务名称" /F`

## 安全注意事项

1. **权限管理**：计划任务可能需要较高权限才能正常运行，但应避免过度授权
2. **任务名称唯一性**：确保任务名称唯一，避免与系统或其他程序的任务冲突
3. **文件安全**：保护好生成的AutoLogin.exe文件，其中包含加密的账号信息
4. **定期检查**：定期检查计划任务的运行状态和日志，确保功能正常
5. **及时更新**：当账号密码变更时，及时更新计划任务

## 附录：常用schtasks命令示例

### 创建登录时自动执行的任务
```powershell
schtasks /Create /TN "GXSTNU_Schoolnet_Login_OnLogon" /TR "C:\ScheduledTasks\AutoLogin.exe" /SC ONLOGON /RU SYSTEM /RL HIGHEST /F
```

### 创建每天8点执行的任务
```powershell
schtasks /Create /TN "GXSTNU_Schoolnet_Login_Daily" /TR "C:\ScheduledTasks\AutoLogin.exe" /SC DAILY /ST 08:00 /RU SYSTEM /RL HIGHEST /F
```

### 查询所有校园网登录相关任务
```powershell
schtasks /Query /TN "GXSTNU_Schoolnet_*" /FO TABLE
```

### 删除指定任务
```powershell
schtasks /Delete /TN "GXSTNU_Schoolnet_Login_Daily" /F
```

### 立即运行任务
```powershell
schtasks /Run /TN "GXSTNU_Schoolnet_Login_OnLogon"
```

## 更新日志

### v1.0.0
- 初始版本，包含基本的计划任务参数说明

### v1.1.0
- 增加了高级配置选项和常见问题解决方案
- 完善了示例命令和参数说明

### v1.2.0
- 添加了任务类型详解和使用场景说明
- 优化了文档结构和格式