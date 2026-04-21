# 日志配置模块
import logging
import os
from typing import Optional


class LoggerHandler:
    """日志处理器"""
    
    _instance: Optional['LoggerHandler'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self) -> None:
        """设置日志记录器"""
        # 创建日志目录
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # 创建日志记录器
        self._logger = logging.getLogger('doc_gen_agent')
        self._logger.setLevel(logging.INFO)
        
        # 避免重复添加处理器
        if not self._logger.handlers:
            # 文件处理器
            file_handler = logging.FileHandler(
                os.path.join(log_dir, 'doc_gen_agent.log'),
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加处理器
            self._logger.addHandler(file_handler)
            self._logger.addHandler(console_handler)
    
    @property
    def logger(self) -> logging.Logger:
        """获取日志记录器"""
        if self._logger is None:
            self._setup_logger()
        return self._logger


def get_logger(name: str = 'doc_gen_agent') -> logging.Logger:
    """获取日志记录器的便捷函数"""
    return LoggerHandler().logger
