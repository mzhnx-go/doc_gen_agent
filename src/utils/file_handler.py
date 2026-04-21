# 文件处理器
import os
import shutil
from typing import Optional

class FileHandler:
    def __init__(self):
        pass
    
    def ensure_directory(self, directory: str):
        """确保目录存在"""
        os.makedirs(directory, exist_ok=True)
    
    def copy_file(self, src: str, dst: str) -> bool:
        """复制文件"""
        try:
            shutil.copy2(src, dst)
            return True
        except Exception:
            return False
    
    def move_file(self, src: str, dst: str) -> bool:
        """移动文件"""
        try:
            shutil.move(src, dst)
            return True
        except Exception:
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """删除文件"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception:
            return False
    
    def get_file_size(self, file_path: str) -> float:
        """获取文件大小（MB）"""
        try:
            return os.path.getsize(file_path) / (1024 * 1024)
        except Exception:
            return 0
    
    def get_file_extension(self, file_path: str) -> str:
        """获取文件扩展名"""
        return os.path.splitext(file_path)[1].lower()
    
    def is_valid_file(self, file_path: str, allowed_extensions: list = None) -> bool:
        """检查文件是否有效"""
        if not os.path.exists(file_path):
            return False
        
        if allowed_extensions:
            ext = self.get_file_extension(file_path)
            return ext in allowed_extensions
        
        return True
