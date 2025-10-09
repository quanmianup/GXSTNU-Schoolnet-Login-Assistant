"""
异步任务执行器模块，提供健壮的异步任务执行框架。

此模块实现了一个在独立线程池中执行耗时操作的框架，通过Qt信号槽机制与主线程安全通信，
确保UI界面在执行耗时操作时保持响应性。

依赖项:
- concurrent.futures: 提供线程池和异步任务支持
- PySide6.QtCore: 提供Qt信号槽机制
- src.utils.logger: 提供日志记录功能

使用示例:
```python
from src.core.AsyncTaskExecutor import AsyncTaskExecutor

# 创建执行器实例
executor = AsyncTaskExecutor()

# 连接信号槽以处理任务完成事件
def on_task_finished(success, message, op_type):
    if success:
        print(f"操作 {op_type} 成功: {message}")
    else:
        print(f"操作 {op_type} 失败: {message}")

executor.finished.connect(on_task_finished)

# 定义任务函数
def login_task(username, password):
    # 执行登录逻辑
    return "登录成功"

# 提交任务并获取任务ID
task_id = executor.execute_task(lambda: login_task("user123", "pass456"), "login")

# （可选）取消任务
if need_to_cancel:
    executor.cancel_task(task_id)

# （可选）取消所有任务
if need_to_cancel_all:
    executor.cancel_all_tasks()
```
"""
from concurrent.futures import ThreadPoolExecutor, Future
from src.utils.logger import logger
from typing import Callable, Dict
from PySide6.QtCore import QObject, Signal


class AsyncTaskExecutor(QObject):
    """
    异步任务执行器类，提供健壮的异步任务执行框架。
    
    该类在独立线程池中执行耗时操作，同时通过Qt信号槽机制与主线程安全通信，确保UI响应性。
    
    适用场景:
    - 网络请求处理（登录、注销、数据获取等）
    - 文件读写操作
    - 数据处理与计算
    - 任何可能阻塞主线程的耗时操作
    
    信号:
        finished: 任务完成信号，参数为(success: bool, message: object, op_type: str)
                 success: 任务是否执行成功的布尔值
                 message: 任务执行返回结果或错误信息
                 op_type: 操作类型标识
    
    属性:
        thread_pool: 线程池对象
        active_tasks: 活跃任务字典，键为任务ID，值为Future对象
        task_counter: 任务计数器，用于生成唯一任务ID
    """
    # 任务完成信号：参数(success, message, operation_type, extra_data)
    finished = Signal(bool, object, str, dict)  # 正确实例化信号

    def __init__(self):
        """
        初始化异步任务执行器。
        
        创建线程池（最大工作线程数为5），初始化活跃任务字典和任务计数器。
        """
        super().__init__()
        # 创建线程池，最大工作线程数为5
        self.thread_pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="AsyncTask")
        # 用于追踪任务的字典
        self.active_tasks: Dict[str, Future] = {}
        # 记录任务ID，用于区分不同任务
        self.task_counter = 0

    def execute_task(self, func: Callable, op_type: str = "unknown", extra_data: dict = None) -> str:
        """
        执行异步任务，提交到线程池并返回任务ID。
        
        参数:
            func: 要执行的任务函数或已绑定参数的函数
            op_type: 操作类型标识（如"login", "dislogin"等）
            extra_data: 额外数据，会传递到完成信号
        
        返回:
            str: 任务ID，可用于后续取消任务
        
        示例:
            >>> task_id = executor.execute_task(lambda: networkmanager.login(username, password), "login")
        """
        # 生成唯一任务ID
        task_id = f"{op_type}_{self.task_counter}"
        self.task_counter += 1
        
        try:
            # 提交任务到线程池
            future = self.thread_pool.submit(self._run_task, func, op_type)
            # 存储任务引用以便追踪和取消
            self.active_tasks[task_id] = future
            # 添加回调处理结果，传递extra_data
            future.add_done_callback(lambda f, tid=task_id, ed=extra_data: self._handle_future_result(f, tid, ed))
            return task_id
        except Exception as e:
            logger.error(f"[任务 {task_id}] 提交失败: {str(e)}")
            self.finished.emit(False, f"任务提交失败: {str(e)}", op_type, extra_data)
            return task_id

    def cancel_task(self, task_id: str) -> bool:
        """
        取消指定ID的任务。
        
        参数:
            task_id: 要取消的任务ID
        
        返回:
            bool: 取消是否成功
        
        注意:
            任务取消成功仅表示尝试取消的操作成功，不保证任务一定能被取消。
            如果任务已经开始执行，则无法取消。
        """
        if task_id in self.active_tasks:
            # 尝试取消任务
            cancelled = self.active_tasks[task_id].cancel()
            if cancelled:
                logger.info(f"[任务 {task_id}] 已取消")
                del self.active_tasks[task_id]  # 从活动任务列表中移除
            return cancelled
        return False

    def cancel_all_tasks(self) -> None:
        """
        取消所有正在执行的任务。
        
        该方法会尝试取消所有已提交但尚未开始执行的任务，并记录剩余活跃任务数。
        """
        for task_id in list(self.active_tasks.keys()):
            self.cancel_task(task_id)
        logger.info(f"已尝试取消所有任务，剩余活跃任务数: {len(self.active_tasks)}")

    @staticmethod
    def _run_task(func: Callable, op_type: str) -> tuple:
        """
        在线程池中运行任务的内部方法。
        
        参数:
            func: 要执行的任务函数
            op_type: 操作类型标识
        
        返回:
            tuple: (success: bool, message: str, op_type: str)
            success: 任务是否执行成功的布尔值
            message: 任务执行返回结果或错误信息
            op_type: 操作类型标识
        """
        # 获取任务名称，处理lambda函数和其他没有__name__属性的情况
        task_name = getattr(func, "__name__", str(func))
        # 转义可能导致loguru颜色解析错误的字符
        task_name = task_name.replace('<', '\<').replace('>', '\>')
        # logger.info(f"[任务执行] 开始执行: {task_name}, 操作类型: {op_type}")
        
        try:
            # 包装成(success, message, op_type)格式
            return True, func(), op_type
        except ConnectionError as e:
            logger.error(f"[任务执行] 连接错误: {task_name}, 错误: {str(e)}")
            return False, f"网络连接错误: {str(e)}", op_type
        except TimeoutError as e:
            logger.error(f"[任务执行] 超时: {task_name}, 错误: {str(e)}")
            return False, f"操作超时: {str(e)}", op_type
        except Exception as e:
            logger.error(f"[任务执行] 失败: {task_name}, 错误: {str(e)}", exc_info=True)
            return False, f"任务执行失败: {str(e)}", op_type

    def _handle_future_result(self, future: Future, task_id: str, extra_data: dict = None) -> None:
        """
        处理任务执行结果的回调方法。
        
        参数:
            future: 任务的Future对象
            task_id: 任务ID
            extra_data: 额外数据，会传递到完成信号
        
        功能:
            - 从活跃任务列表中移除已完成的任务
            - 获取任务结果并通过信号发送给主线程
            - 处理回调过程中可能发生的异常
        """
        try:
            # 从活动任务列表中移除已完成的任务
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            # 获取任务结果
            success, message, op_type = future.result()
            # 发射完成信号
            self.finished.emit(success, message, op_type, extra_data)
        except (KeyboardInterrupt, SystemExit):
            # 允许这些异常向上传播
            raise
        except Exception as e:
            # 处理回调过程中的异常
            logger.error(f"[任务回调] 发生异常: {task_id}", exc_info=True)
            op_type = task_id.split('_')[0] if '_' in task_id else "unknown"
            self.finished.emit(False, f"处理任务ID（{task_id}）时发生未知错误: {str(e)}", op_type, extra_data)

    def __del__(self):
        """
        析构函数，确保线程池正确关闭。
        
        取消所有任务并关闭线程池，等待所有任务完成。
        """
        # 取消所有任务
        self.cancel_all_tasks()
        # 关闭线程池，等待所有任务完成
        self.thread_pool.shutdown(wait=True)
        logger.info("异步任务执行器已关闭")
