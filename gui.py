import logging
import threading  # 新增导入
import tkinter as tk
from tkinter import messagebox, ttk  # 新增导入，用于美化控件

from auth import do_login, do_dislogin
from config_secret import USERNAME, PASSWORD, update_credentials
from logger import logger


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("广西科师校园网登录工具")
        self.root.geometry("600x500")

        # 设置程序图标 (需要准备一个icon.ico文件放在同级目录)
        try:
            self.root.iconbitmap('./images/main_image.ico')
        except:
            pass  # 如果图标文件不存在则忽略

        # 设置现代主题样式
        style = ttk.Style()
        style.theme_use('vista')  # 使用更现代的vista主题

        # 配置控件样式
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('微软雅黑', 10))
        style.configure('TButton', font=('微软雅黑', 10), padding=5)
        style.configure('TCheckbutton', background='#f0f0f0', font=('微软雅黑', 10))
        style.map('TCheckbutton',
                  indicatorcolor=[('selected', '#4CAF50'), ('!selected', '#f0f0f0')],
                  foreground=[('selected', '#4CAF50')])

        # 主框架
        main_frame = ttk.Frame(root, padding="20", style='TFrame')
        main_frame.pack(fill='both', expand=True)

        # 账号密码输入框
        ttk.Label(main_frame, text="校园网账号:").pack(pady=5)
        self.username_entry = ttk.Entry(main_frame, font=('微软雅黑', 10))
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, USERNAME)

        ttk.Label(main_frame, text="校园网密码:").pack(pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*", font=('微软雅黑', 10))
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, PASSWORD)

        # 保存账号密码复选框 (使用√号)
        self.save_var = tk.IntVar(value=1)
        check = ttk.Checkbutton(
            main_frame,
            text="记住账号密码",
            variable=self.save_var,
            style='TCheckbutton'
        )
        check.pack(pady=10)

        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        self.login_button = ttk.Button(button_frame, text="一键登录", command=self.do_login, width=15)
        self.login_button.grid(row=0, column=0, padx=10)

        self.dislogin_button = ttk.Button(button_frame, text="一键下线", command=self.do_dislogin, width=15)
        self.dislogin_button.grid(row=0, column=1, padx=10)

        # 替换状态标签为进度条
        self.progress_var = tk.IntVar(value=0)
        self.progress = ttk.Progressbar(
            main_frame,
            orient='horizontal',
            length=300,
            mode='determinate',
            variable=self.progress_var,
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress.pack(pady=10)

        # 配置进度条样式
        style.configure('Custom.Horizontal.TProgressbar',
                        thickness=12,
                        troughcolor='#e0e0e0',
                        background='#4CAF50',
                        troughrelief='flat')

        # 日志显示区域
        ttk.Label(main_frame, text="操作日志:").pack(pady=5)
        self.log_text = tk.Text(main_frame, height=15, state='disabled', bg='white', fg='black')
        self.log_text.pack(fill='both', expand=True)

        # 重定向日志输出到GUI
        self.log_handler = TextHandler(self.log_text)
        logger.addHandler(self.log_handler)

        # 状态标签
        self.status_label = ttk.Label(main_frame, text="就绪", foreground="gray")
        self.status_label.pack(pady=5)

    def _update_progress_state(self, state):
        """更新进度条状态"""
        self.login_button.config(state=state)
        self.dislogin_button.config(state=state)

        if state == 'disabled':
            self._animate_progress(50)  # 操作中显示50%进度
        else:
            self._animate_progress(100)  # 操作完成显示100%进度
            self.root.after(1000, lambda: self.progress_var.set(0))  # 1秒后归零

    def _animate_progress(self, target):
        """平滑动画效果"""
        current = self.progress_var.get()
        if current < target:
            self.progress_var.set(current + 1)
            self.root.after(20, lambda: self._animate_progress(target))
        elif current > target:
            self.progress_var.set(current - 1)
            self.root.after(20, lambda: self._animate_progress(target))

    def do_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("错误", "请输入账号和密码")
            return False

        if self.save_var.get():
            update_credentials(username, password)

        self._update_progress_state('disabled')  # 禁用按钮并更新进度条
        threading.Thread(target=self._login_thread, args=(username, password)).start()

    def _login_thread(self, username, password):
        """登录线程函数"""
        try:
            if do_login():
                self.root.after(0, lambda: messagebox.showinfo("成功", "登录成功"))
            else:
                self.root.after(0, lambda: messagebox.showerror("错误", "登录失败，请检查账号密码"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"发生异常: {str(e)}"))
        finally:
            self.root.after(0, self._toggle_buttons, 'normal')

    def do_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("错误", "请输入账号和密码")
            return False

        if self.save_var.get():
            update_credentials(username, password)

        self._toggle_buttons('disabled')  # 禁用按钮
        # 启动线程执行登录操作
        threading.Thread(target=self._login_thread, args=(username, password)).start()

    def _dislogin_thread(self, username, password):
        """修复后的下线线程函数"""
        try:
            result = do_dislogin()
            self.root.after(0, lambda: messagebox.showinfo("成功", "下线成功") if result else
            messagebox.showerror("错误", "下线失败"))
        except Exception as e:
            logger.error(f"下线异常: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"下线异常: {str(e)}"))
        finally:
            self.root.after(0, lambda: self._toggle_buttons('normal'))

    def do_dislogin(self):
        """修复后的下线方法"""
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("错误", "请输入账号")
            return

        if self.save_var.get():
            update_credentials(username, self.password_entry.get())

        self._toggle_buttons('disabled')
        thread = threading.Thread(
            target=self._dislogin_thread,
            args=(username, self.password_entry.get()),
            daemon=True
        )
        thread.start()

    def _toggle_buttons(self, state):
        """切换按钮状态"""
        self.login_button.config(state=state)
        self.dislogin_button.config(state=state)

        if state == 'disabled':
            self.progress_var.set(50)  # 操作中显示50%进度
        else:
            self.progress_var.set(100)  # 操作完成显示100%进度
            self.root.after(1000, lambda: self.progress_var.set(0))  # 1秒后归零
        self.status_label.config(
            text="操作中..." if state == 'disabled' else "就绪",
            foreground="blue" if state == 'disabled' else "gray"
        )


class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        # 设置完整日志格式
        self.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state='normal')
        self.text_widget.insert('end', msg + '\n')
        self.text_widget.configure(state='disabled')
        self.text_widget.see('end')


def run_gui():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
