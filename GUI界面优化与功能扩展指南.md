# GUI界面优化与功能扩展指南

## 概述

本指南提供了对广西科师校园网登录助手进行GUI界面优化与功能扩展的详细操作步骤，包括添加日志显示部件、优化控件尺寸、新增网络状态显示和断线重连功能。

## 环境准备

1. 确保已安装Python 3.11.9
2. 确保已安装PyQt5或PySide6
3. 确保项目已在虚拟环境中运行
4. 安装项目依赖：
   ```powershell
   cd f:\code\py\schoolnet
   uv pip install -r requirements.txt
   ```

## 第一部分：使用Qt Designer修改main.ui界面

### 步骤1：打开Qt Designer

运行项目中的Qt Designer工具：

```powershell
cd f:\code\py\schoolnet\src\tool
./run_designer.ps1
```

在Qt Designer中打开`f:\code\py\schoolnet\assets\qtfile\main.ui`文件。

### 步骤2：添加日志显示部件

1. 在`frame_main`框架内，找到`page_main`页面
2. 在现有控件下方添加一个`QTabWidget`，命名为`tabWidget_main`
3. 在`tabWidget_main`中保留原有的登录相关内容作为第一个标签页
4. 添加第二个标签页，命名为`tab_log`，标题为"日志显示"
5. 在`tab_log`中添加一个`QTextBrowser`控件，命名为`textBrowser_log`
6. 设置`textBrowser_log`的属性：
   - 设置`readOnly`为`True`
   - 设置字体为等宽字体（如Consolas或Courier New）
   - 设置背景色为浅灰色

### 步骤3：优化控件尺寸

1. 选择所有输入框控件（`lineEdit_username`, `lineEdit_password`）
2. 在属性编辑器中：
   - 设置`minimumSize`为`300, 30`
   - 设置`maximumSize`为`16777215, 30`
   - 设置`sizePolicy`的`Horizontal Policy`为`Expanding`
3. 选择所有按钮控件（`pushButton_login`, `pushButton_dislogin`, `pushButton_generate`）
4. 在属性编辑器中：
   - 设置`minimumSize`为`120, 35`
   - 设置`sizePolicy`的`Horizontal Policy`为`Fixed`
5. 调整整体布局，确保各控件间距合适

### 步骤4：新增网络状态显示

1. 在主窗口底部添加一个水平布局
2. 在水平布局中添加以下组件：
   - 一个`QLabel`，命名为`label_network_status`，文本为"网络状态："
   - 一个`QLabel`，命名为`label_status_icon`，用于显示状态图标
   - 一个`QLabel`，命名为`label_status_text`，用于显示状态文本
3. 添加网络状态图标资源：
   - 使用项目中已有的`assets/images/network.png`和`assets/images/internet.png`
   - 在Qt Designer中设置`label_status_icon`的图标
4. 设置状态栏的样式表，使其更醒目

### 步骤5：添加断线重连按钮

1. 在网络状态显示区域旁边添加一个`QPushButton`，命名为`pushButton_reconnect`
2. 设置按钮文本为"断线重连"
3. 设置按钮图标（可使用现有的连接相关图标）
4. 设置按钮的`minimumSize`为`100, 30`

### 步骤6：保存修改并生成Python代码

1. 在Qt Designer中保存修改后的`main.ui`文件
2. 运行项目中的uic工具生成Python代码：
   ```powershell
   cd f:\code\py\schoolnet\src\tool
   ./run_uic.ps1
   ```
   这将更新`src/gui/main_ui.py`文件

## 第二部分：实现后端逻辑

### 步骤1：修改主程序逻辑 (main_gui_program.py)

打开`f:\code\py\schoolnet\src\gui\main_gui_program.py`文件，进行以下修改：

1. 导入必要的模块：
   ```python
   import logging
   from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
   from PyQt5.QtGui import QFont, QIcon
   from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
   ```

2. 在`MainWindow`类的初始化方法中添加日志显示和网络状态相关代码：
   ```python
   def __init__(self):
       super().__init__()
       # ... 现有代码 ...
       
       # 初始化日志显示
       self.init_log_display()
       
       # 初始化网络状态检测
       self.init_network_monitor()
       
       # 连接信号和槽
       self.pushButton_reconnect.clicked.connect(self.handle_reconnect)
   ```

3. 添加初始化日志显示的方法：
   ```python
   def init_log_display(self):
       # 设置日志显示控件的字体
       font = QFont()
       font.setFamily("Consolas")
       font.setPointSize(10)
       self.textBrowser_log.setFont(font)
       
       # 创建一个自定义的日志处理器，将日志输出到textBrowser
       class QTextBrowserLogger(logging.Handler):
           def __init__(self, text_browser):
               super().__init__()
               self.text_browser = text_browser
               self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
                
           def emit(self, record):
               msg = self.format(record)
               self.text_browser.append(msg)
               self.text_browser.moveCursor(self.text_browser.textCursor().End)
       
       # 获取logger并添加处理器
       logger = logging.getLogger()
       logger.addHandler(QTextBrowserLogger(self.textBrowser_log))
   ```

4. 添加初始化网络状态监控的方法：
   ```python
   def init_network_monitor(self):
       # 设置网络状态图标
       self.icons = {
           'connected': QIcon('assets/images/internet.png'),
           'disconnected': QIcon('assets/images/network.png')
       }
       
       # 初始状态设为未知
       self.update_network_status(False)
       
       # 创建定时器定期检查网络状态
       self.network_timer = QTimer(self)
       self.network_timer.timeout.connect(self.check_network_status)
       self.network_timer.start(5000)  # 每5秒检查一次
   ```

5. 添加检查网络状态和更新显示的方法：
   ```python
   def check_network_status(self):
       # 使用NetworkManager检查网络连接状态
       from src.core.network import NetworkManager
       is_connected = NetworkManager().check_network()
       self.update_network_status(is_connected)
       
       # 如果断线，自动触发重连（可选）
       if not is_connected:
           logging.warning("网络连接已断开，正在尝试重连...")
           self.handle_reconnect()
   
   def update_network_status(self, is_connected):
       if is_connected:
           self.label_status_icon.setIcon(self.icons['connected'])
           self.label_status_text.setText("已连接")
           self.label_status_text.setStyleSheet("color: green;")
           self.pushButton_reconnect.setEnabled(False)
       else:
           self.label_status_icon.setIcon(self.icons['disconnected'])
           self.label_status_text.setText("未连接")
           self.label_status_text.setStyleSheet("color: red;")
           self.pushButton_reconnect.setEnabled(True)
   ```

6. 添加断线重连处理方法：
   ```python
   def handle_reconnect(self):
       logging.info("开始执行断线重连...")
       
       # 禁用重连按钮防止重复点击
       self.pushButton_reconnect.setEnabled(False)
       self.pushButton_reconnect.setText("重连中...")
       
       # 检查是否已保存登录凭据
       from src.config.credentials import Credentials
       creds = Credentials()
       username, password = creds.get_credentials()
       
       if username and password:
           # 在单独的线程中执行重连操作
           self.reconnect_thread = ReconnectThread(username, password)
           self.reconnect_thread.reconnect_finished.connect(self.on_reconnect_finished)
           self.reconnect_thread.start()
       else:
           QMessageBox.warning(self, "重连失败", "没有保存的登录凭据，请先手动登录")
           self.pushButton_reconnect.setEnabled(True)
           self.pushButton_reconnect.setText("断线重连")
   
   def on_reconnect_finished(self, success):
       if success:
           logging.info("断线重连成功")
           QMessageBox.information(self, "重连成功", "网络已成功重新连接")
       else:
           logging.error("断线重连失败")
           QMessageBox.critical(self, "重连失败", "无法重新连接到校园网络，请检查网络环境或手动登录")
       
       self.pushButton_reconnect.setEnabled(True)
       self.pushButton_reconnect.setText("断线重连")
   ```

### 步骤2：创建断线重连线程类

在`main_gui_program.py`文件中添加重连线程类：

```python
class ReconnectThread(QThread):
    reconnect_finished = pyqtSignal(bool)
    
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
    
    def run(self):
        try:
            from src.core.network import NetworkManager
            nm = NetworkManager()
            success = nm.login(self.username, self.password)
            self.reconnect_finished.emit(success)
        except Exception as e:
            logging.error(f"重连过程发生错误: {str(e)}")
            self.reconnect_finished.emit(False)
```

### 步骤3：修改NetworkManager类

打开`f:\code\py\schoolnet\src\core\network.py`文件，进行以下修改：

1. 确保`check_network`方法正确实现：
   ```python
   def check_network(self):
       try:
           # 测试连接到一个稳定的外部网站
           import requests
           response = requests.get("http://www.baidu.com", timeout=3)
           return response.status_code == 200
       except:
           return False
   ```

2. 确保`login`方法可以正确处理重连逻辑：
   ```python
   def login(self, username, password):
       # 现有的登录逻辑
       # ...
       # 确保返回布尔值表示登录成功或失败
       return success
   ```

### 步骤4：修改日志配置

打开`f:\code\py\schoolnet\src\utils\logger.py`文件，确保日志配置正确：

```python
import logging
import os
from datetime import datetime

def setup_logger():
    # 创建日志目录
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志文件名（按日期）
    log_file = os.path.join(log_dir, f"schoolnet_{datetime.now().strftime('%Y%m%d')}.log")
    
    # 配置logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 清除已有的处理器
    if logger.handlers:
        logger.handlers.clear()
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger
```

## 第三部分：测试与部署

### 步骤1：运行应用程序进行测试

```powershell
cd f:\code\py\schoolnet
python run.py
```

### 步骤2：测试功能

1. 测试日志显示功能：观察操作过程中日志是否正确显示在日志标签页中
2. 测试网络状态显示：观察网络状态是否正确显示在状态栏
3. 测试断线重连功能：手动断开网络连接，然后点击"断线重连"按钮，检查是否能成功重连

### 步骤3：创建可执行文件（可选）

如果需要创建独立的可执行文件，可以使用PyInstaller：

```powershell
uv pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/images/main_icon.ico run.py
```

## 常见问题与解决方案

1. **问题**：Qt Designer无法打开
   **解决方案**：检查PyQt5或PySide6是否正确安装，确保`run_designer.ps1`脚本路径正确

2. **问题**：生成的Python代码与UI不匹配
   **解决方案**：确保每次修改UI后都重新运行`run_uic.ps1`脚本生成最新的Python代码

3. **问题**：日志不显示或显示异常
   **解决方案**：检查日志级别设置，确保使用了正确的logger名称

4. **问题**：网络状态检测不准确
   **解决方案**：调整`check_network`方法中的测试网站，选择校园网内稳定的服务器

5. **问题**：断线重连功能不工作
   **解决方案**：检查登录凭据是否正确保存，检查NetworkManager的login方法是否正常工作

---

完成以上步骤后，您的广西科师校园网登录助手将具备更友好的界面和更强大的功能，包括实时日志显示、优化的控件尺寸、网络状态监控和自动断线重连功能。