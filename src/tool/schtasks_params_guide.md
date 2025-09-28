# schtasks /Create 命令参数指南

本指南基于 Windows 任务计划程序的 `schtasks /Create` 命令，详细解释了所有可用参数及其用法。

## 主要参数

| 参数 | 说明 |
|------|------|
| `/S system` | 指定要连接的远程系统。如果省略，默认为本地系统。 |
| `/U username` | 指定 SchTasks.exe 应执行的用户上下文。 |
| `/P [password]` | 指定给定用户上下文的密码。如果省略，会提示输入。 |
| `/RU username` | 指定任务运行的"运行方式"用户账户。对于系统账户，有效值为""、"NT AUTHORITY\SYSTEM"或"SYSTEM"。 |
| `/RP [password]` | 指定"运行方式"用户的密码。要提示输入密码，值必须是"*"或为空。系统账户忽略此密码。必须与 /RU 或 /XML 开关结合使用。 |

## 计划参数

| 参数 | 说明 |
|------|------|
| `/SC schedule` | 指定计划频率。有效的计划类型：MINUTE（分钟）、HOURLY（小时）、DAILY（每日）、WEEKLY（每周）、MONTHLY（每月）、ONCE（一次性）、ONSTART（启动时）、ONLOGON（登录时）、ONIDLE（空闲时）、ONEVENT（事件时）。 |
| `/MO modifier` | 细化计划类型，允许更精细地控制计划重复。 |
| `/D days` | 指定运行任务的星期几。有效值：MON、TUE、WED、THU、FRI、SAT、SUN，以及每月计划的 1-31（每月的天数）。通配符"*"指定所有天。 |
| `/M months` | 指定一年中的月份。默认为该月的第一天。有效值：JAN、FEB、MAR、APR、MAY、JUN、JUL、AUG、SEP、OCT、NOV、DEC。通配符"*"指定所有月份。 |
| `/I idletime` | 指定运行计划的 ONIDLE 任务之前要等待的空闲时间量。有效范围：1-999 分钟。 |

## 时间参数

| 参数 | 说明 |
|------|------|
| `/ST starttime` | 指定开始运行任务的时间。时间格式为 HH:mm（24 小时制），例如，14:30 表示下午 2:30。如果未指定 /ST，则默认为当前时间。与 /SC ONCE 一起使用时，此选项是必需的。 |
| `/RI interval` | 指定重复间隔（分钟）。不适用于 MINUTE、HOURLY、ONSTART、ONLOGON、ONIDLE、ONEVENT 计划类型。有效范围：1-599940 分钟。如果指定了 /ET 或 /DU，则默认为 10 分钟。 |
| `/ET endtime` | 指定结束运行任务的时间。时间格式为 HH:mm（24 小时制）。不适用于 ONSTART、ONLOGON、ONIDLE、ONEVENT 计划类型。 |
| `/DU duration` | 指定运行任务的持续时间。时间格式为 HH:mm。不适用于 /ET 和 ONSTART、ONLOGON、ONIDLE、ONEVENT 计划类型。对于 /V1 任务，如果指定了 /RI，则持续时间默认为 1 小时。 |
| `/K` | 在结束时间或持续时间终止任务。不适用于 ONSTART、ONLOGON、ONIDLE、ONEVENT 计划类型。必须指定 /ET 或 /DU。 |
| `/SD startdate` | 指定任务首次运行的日期。格式为 yyyy/mm/dd。默认为当前日期。不适用于 ONCE、ONSTART、ONLOGON、ONIDLE、ONEVENT 计划类型。 |
| `/ED enddate` | 指定任务应运行的最后日期。格式为 yyyy/mm/dd。不适用于 ONCE、ONSTART、ONLOGON、ONIDLE、ONEVENT 计划类型。 |

## 任务设置参数

| 参数 | 说明 |
|------|------|
| `/TN taskname` | 指定以 path\name 形式唯一标识此计划任务的字符串。 |
| `/TR taskrun` | 指定在计划时间运行的程序的路径和文件名。例如：C:\windows\system32\calc.exe |
| `/F` | 强制创建任务并在指定任务已存在时抑制警告。 |
| `/IT` | 仅当 /RU 用户在作业运行时当前已登录时，才允许任务交互式运行。此任务仅在用户登录时运行。 |
| `/NP` | 不存储密码。任务以给定用户身份非交互式运行。仅本地资源可用。 |
| `/Z` | 在任务最终运行后将其标记为删除。 |
| `/XML xmlfile` | 从文件中指定的任务 XML 创建任务。可以与 /RU 和 /RP 开关结合使用，或单独与 /RP 结合使用（当任务 XML 已包含主体时）。 |
| `/V1` | 创建对 Vista 之前平台可见的任务。与 /XML 不兼容。 |
| `/RL level` | 设置作业的运行级别。有效值为 LIMITED 和 HIGHEST。默认为 LIMITED。 |
| `/DELAY delaytime` | 指定在触发触发器后延迟运行任务的等待时间。时间格式为 mmmm:ss。此选项仅对 ONSTART、ONLOGON、ONEVENT 计划类型有效。 |
| `/WAKE` | 唤醒计算机以运行任务（这个参数在命令帮助中没有明确列出，但在 Windows 任务计划程序的图形界面和实际使用中是存在的）。 |

## 事件触发参数

| 参数 | 说明 |
|------|------|
| `/EC ChannelName` | 指定 OnEvent 触发器的事件通道。 |
| `/SC ONEVENT` | 创建事件触发的任务。 |
| `/MO XPath` | 指定事件查询的 XPath 字符串。 |

## 修饰符（Modifiers）

每个计划类型的 /MO 开关的有效值：
- MINUTE: 1-1439 分钟。
- HOURLY: 1-23 小时。
- DAILY: 1-365 天。
- WEEKLY: 周 1-52。
- ONCE: 无修饰符。
- ONSTART: 无修饰符。
- ONLOGON: 无修饰符。
- ONIDLE: 无修饰符。
- MONTHLY: 1-12，或 FIRST、SECOND、THIRD、FOURTH、LAST、LASTDAY。
- ONEVENT: XPath 事件查询字符串。

## 使用示例

### 创建每小时运行的任务
```
SCHTASKS /Create /S ABC /U user /P password /RU runasuser /RP runaspassword /SC HOURLY /TN doc /TR notepad
```

### 创建每分钟运行的任务
```
SCHTASKS /Create /S ABC /U domain\user /P password /SC MINUTE /MO 5 /TN accountant /TR calc.exe /ST 12:00 /ET 14:00 /SD 06/06/2006 /ED 06/06/2006 /RU runasuser /RP userpassword
```

### 创建每月运行的任务
```
SCHTASKS /Create /SC MONTHLY /MO first /D SUN /TN gametime /TR c:\windows\system32\freecell
```

### 创建每周运行的任务
```
SCHTASKS /Create /S ABC /U user /P password /RU runasuser /RP runaspassword /SC WEEKLY /TN report /TR notepad.exe
```

### 创建自动终止的任务
```
SCHTASKS /Create /SC DAILY /TN gaming /TR c:\freecell /ST 12:00 /ET 14:00 /K
```

### 创建事件触发的任务
```
SCHTASKS /Create /TN EventLog /TR wevtvwr.msc /SC ONEVENT
```

## 注意事项

1. 某些参数组合可能不兼容，请根据实际需求选择合适的参数。
2. 使用 /RU 和 /RP 参数时，确保您有足够的权限来以指定用户身份运行任务。
3. 对于需要唤醒计算机的任务，确保启用了 /WAKE 参数（虽然命令行帮助中未列出，但实际可用）。