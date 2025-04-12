import tkinter as tk
from tkinter import messagebox
from config_secret import USERNAME, PASSWORD, update_credentials
from auth import do_login, do_dislogin  # 修改导入来源
import logging
from logger import logger


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("广西科师校园网登录工具")
        self.root.geometry("600x500")  # 增大窗口尺寸

        # 账号密码输入框
        tk.Label(root, text="校园网账号:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, USERNAME)

        tk.Label(root, text="校园网密码:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, PASSWORD)

        # 保存账号密码复选框
        self.save_var = tk.IntVar(value=1)
        tk.Checkbutton(root, text="记住账号密码", variable=self.save_var).pack(pady=5)

        # 按钮区域
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="一键登录", command=self.do_login, width=15).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="一键下线", command=self.do_dislogin, width=15).grid(row=0, column=1, padx=10)
        # 日志显示区域
        tk.Label(root, text="操作日志:").pack(pady=5)
        self.log_text = tk.Text(root, height=15, state='disabled')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=5)

        # 重定向日志输出到GUI
        self.log_handler = TextHandler(self.log_text)
        logger.addHandler(self.log_handler)

    def do_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("错误", "请输入账号和密码")
            return False

        if self.save_var.get():
            update_credentials(username, password)

        # 这里调用你的登录函数
        if do_login():
            messagebox.showinfo("成功", "登录成功")
        else:
            messagebox.showerror("错误", "登录失败，请检查账号密码")

    def do_dislogin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username:
            messagebox.showerror("错误", "请输入账号")
            return

        if self.save_var.get():
            update_credentials(username, password)
        # 这里调用你的下线函数
        if do_dislogin():
            messagebox.showinfo("成功", "下线成功")
        else:
            messagebox.showerror("错误", "下线失败")


class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

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
