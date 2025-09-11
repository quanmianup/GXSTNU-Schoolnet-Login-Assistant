from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QObject, Signal
import logging

logger = logging.getLogger(__name__)


class AsyncTaskExecutor(QObject):
    # 修改信号，增加操作类型参数
    finished: Signal = Signal(bool, str, str)  # 类型注解明确化

    def __init__(self):
        super().__init__()
        self.thread_pool = ThreadPoolExecutor(max_workers=5)

    def execute_task(self, task, op_type="unknown", *args):
        future = self.thread_pool.submit(self._run_task, task, op_type, *args)
        # 使用默认参数避免闭包问题
        future.add_done_callback(lambda f=future: self._handle_future_result(f))

    @staticmethod
    def _run_task(task, op_type, *args):
        try:
            result = task(*args)
            logger.info("任务执行成功，结果: %s", result)
            return True, str(result), op_type
        except Exception as e:
            logger.error("任务执行失败，错误信息: %s", str(e))
            return False, str(e), op_type

    def _handle_future_result(self, future):
        try:
            success, message, op_type = future.result()
            self.finished.emit(success, message, op_type)  # 发射信号时带上操作类型
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logger.error("任务执行结果回调发生异常", exc_info=True)
            self.finished.emit(False, f"发生未知错误: {str(e)}", "unknown")

    def __del__(self):
        # 关闭线程池，避免资源泄漏
        self.thread_pool.shutdown(wait=True)
