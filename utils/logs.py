import os
import sys
import logging
# import inspect
from logging.handlers import TimedRotatingFileHandler

from config.settings import log_defulat_dir


def init_logger_obj(log_name: str = None, Level: int = logging.INFO):
    Logger = logging.getLogger("LARK_SYNC")
    if log_name is None:
        script_name = os.path.basename(sys.argv[0])
        filename = os.path.join(log_defulat_dir, f"{script_name.replace('.py', '')}.log")
    else:
        filename = os.path.join(log_defulat_dir, f"{log_name}.log")
    # 创建一个日志处理器，指向 access.log
    if not Logger.hasHandlers():
        log_handler = TimedRotatingFileHandler(
            filename=filename,
            when="midnight",  # midnight日志文件会在每天的午夜自动滚动 创建新的日志文件
            interval=1,  # 滚动的频率 将interval设置为7 那么日志文件将在每周的同一时间滚动一次
            backupCount=90,
            encoding="utf-8"
        )
        # 配置日志格式
        formatter = logging.Formatter('%(levelname)s:  | %(asctime)s | %(filename)s | %(lineno)d | %(funcName)s() | %(message)s')
        log_handler.setFormatter(formatter)
        # 获取应用的根日志记录器
        Logger.setLevel(Level)
        # 将日志处理器添加到日志记录器中
        Logger.addHandler(log_handler)
        # log = FastLogger(logger=app_logger)
    return Logger



def demo():
    app_logger = init_logger_obj()
    
    # INFO | 2024-07-17 12:10:17,685 | __init__.py | f1 | This is an info message from the test endpoint.
    # app_logger.info("This is an info message from the test endpoint.")
    
    # ERROR | 2024-07-17 12:10:17,686 | __init__.py | f1 | This is an error message from the test endpoint.
    # app_logger.error("This is an error message from the test endpoint.")
    
    # INFO | 2024-07-17 15:19:57,960 | __init__.py | demo | {'a': 1, 'b': 2}
    app_logger.info({"a": 1, "b": 2}, {"c": 3})
    
    app_logger.info("Dict", {"a": 1, "b": 2})
    # app_logger.info(200, "200")


def demo2():
    app_logger = init_logger_obj()
    print(type(app_logger))
    print(app_logger)

    
# 现在你可以使用 app_logger 来记录日志
if __name__ == "__main__":
    demo()
    