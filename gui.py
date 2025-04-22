import logging
import os
import threading  # 新增导入
import tkinter as tk
from tkinter import messagebox, ttk  # 新增导入，用于美化控件
from tkinter import simpledialog  # 新增导入，用于弹出对话框
import sys  # 新增导入，用于获取Python解释器路径
from datetime import datetime  # 新增导入，用于验证时间格式
from tkcalendar import Calendar  # 新增导入，用于日期选择

from auth import do_login, do_dislogin
from config_secret import USERNAME, PASSWORD, update_credentials
from logger import logger


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("广西科师校园网登录工具")
        self.root.geometry("600x500")

        # 获取脚本所在目录的绝对路径
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, 'images', 'main_icon.ico')

        # 设置图标
        self.root.iconbitmap(icon_path)

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



        # 添加定时任务管理按钮
        self.schedule_manage_button = ttk.Button(button_frame, text="定时任务管理", command=self.manage_schedule, width=15)
        self.schedule_manage_button.grid(row=1, column=0, padx=10, pady=5)

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

        self._toggle_buttons('disabled')  # 禁用按钮
        # 启动线程执行登录操作
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

    def setup_schedule(self):
        """设置定时登录时间"""
        # 创建日期选择窗口
        date_window = tk.Toplevel(self.root)
        date_window.title("选择时间")
        date_window.geometry("300x200")

        # 添加时间选择框
        time_frame = ttk.Frame(date_window)
        time_frame.pack(pady=20)

        # 小时选择
        ttk.Label(time_frame, text="小时:").grid(row=0, column=0, padx=5)
        hour_combobox = ttk.Combobox(time_frame, width=5, values=[f"{i:02d}" for i in range(24)])
        hour_combobox.grid(row=0, column=1, padx=5)
        hour_combobox.current(datetime.now().hour)  # 默认当前小时

        # 分钟选择
        ttk.Label(time_frame, text="分钟:").grid(row=1, column=0, padx=5)
        minute_combobox = ttk.Combobox(time_frame, width=5, values=[f"{i:02d}" for i in range(60)])
        minute_combobox.grid(row=1, column=1, padx=5)
        minute_combobox.current(datetime.now().minute)  # 默认当前分钟

        # 确认按钮
        def on_confirm():
            selected_hour = hour_combobox.get()
            selected_minute = minute_combobox.get()
            try:
                # 验证时间格式
                datetime.strptime(f"{selected_hour}:{selected_minute}", "%H:%M")
                full_time = f"{selected_hour}:{selected_minute}"
                self._setup_schedule_task(full_time)
                date_window.destroy()
            except ValueError:
                messagebox.showerror("错误", "请选择有效的时间")

        confirm_button = ttk.Button(date_window, text="确认", command=on_confirm)
        confirm_button.pack(pady=10)

    def _setup_schedule_task(self, time_str):
        """使用Windows任务计划程序设置定时任务"""
        # 获取Python解释器路径
        python_exe = sys.executable
        # 获取脚本路径
        script_path = os.path.abspath(__file__)
        # 创建任务计划命令
        task_name = "GKS_SchoolNet_Login"
        command = f'schtasks /create /tn "{task_name}" /tr "{python_exe} {script_path}" /sc daily /st {time_str} /f'
        
        # 执行命令
        result = os.system(command)
        if result == 0:
            messagebox.showinfo("成功", f"定时登录任务已设置，每天{time_str}自动登录")
        else:
            messagebox.showerror("错误", "定时任务设置失败，请检查权限")

    def manage_schedule(self):
        """管理定时任务"""
        # 创建管理窗口
        manage_window = tk.Toplevel(self.root)
        manage_window.title("定时任务管理")
        manage_window.geometry("400x400")
        # 添加定时登录按钮
        schedule_button = ttk.Button(manage_window, text="定时登录", command=self.setup_schedule)
        schedule_button.pack(pady=10)
        # 查询任务按钮
        query_button = ttk.Button(manage_window, text="查询任务", command=self.query_schedule_task)
        query_button.pack(pady=10)

        # 删除任务按钮
        delete_button = ttk.Button(manage_window, text="删除任务", command=self.delete_schedule_task)
        delete_button.pack(pady=10)

        # 修改任务按钮
        modify_button = ttk.Button(manage_window, text="修改任务", command=self.modify_schedule_task)
        modify_button.pack(pady=10)

        # 添加关闭按钮
        close_button = ttk.Button(manage_window, text="关闭", command=manage_window.destroy)
        close_button.pack(pady=10)

    def query_schedule_task(self):
        """查询定时任务"""
        task_name = "GKS_SchoolNet_Login"
        command = f'schtasks /query /tn "{task_name}"'
        result = os.system(command)
        if result != 0:
            messagebox.showinfo("提示", "未找到定时登录任务")
        else:
            # 获取任务详细信息
            command = f'schtasks /query /tn "{task_name}" /fo list /v'
            output = os.popen(command).read()
            # 弹出窗口显示任务信息
            info_window = tk.Toplevel(self.root)
            info_window.title("定时任务信息")
            info_window.geometry("500x300")
            # 添加文本框显示任务信息
            info_text = tk.Text(info_window, wrap='word', state='normal', bg='white', fg='black')
            info_text.pack(fill='both', expand=True, padx=10, pady=10)
            info_text.insert('end', output)
            info_text.config(state='disabled')
            # 添加关闭按钮
            close_button = ttk.Button(info_window, text="关闭", command=info_window.destroy)
            close_button.pack(pady=10)

    def delete_schedule_task(self):
        """删除定时任务"""
        task_name = "GKS_SchoolNet_Login"
        command = f'schtasks /delete /tn "{task_name}" /f'
        result = os.system(command)
        if result == 0:
            messagebox.showinfo("成功", "定时登录任务已删除")
        else:
            messagebox.showerror("错误", "删除定时任务失败")

    def modify_schedule_task(self):
        """修改定时任务时间"""
        # 弹出对话框获取新时间
        new_time = simpledialog.askstring("修改定时任务", "请输入新的定时登录时间（格式：HH:MM）", parent=self.root)
        if new_time:
            try:
                # 验证时间格式
                datetime.strptime(new_time, "%H:%M")
                # 调用任务计划程序修改定时任务
                self._modify_schedule_task_time(new_time)
            except ValueError:
                messagebox.showerror("错误", "时间格式不正确，请输入HH:MM格式的时间")

    def _modify_schedule_task_time(self, new_time):
        """使用Windows任务计划程序修改定时任务时间"""
        task_name = "GKS_SchoolNet_Login"
        command = f'schtasks /change /tn "{task_name}" /st {new_time}'
        result = os.system(command)
        if result == 0:
            messagebox.showinfo("成功", f"定时登录任务时间已修改为每天{new_time}")
        else:
            messagebox.showerror("错误", "修改定时任务时间失败")

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
