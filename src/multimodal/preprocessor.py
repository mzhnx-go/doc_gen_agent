# 图像预处理模块
import cv2
import numpy as np
from PIL import Image
from typing import Optional

class ImagePreprocessor:
    def __init__(self, config: dict = None):
        self.config = config or {}
    
    def preprocess(self, image_path: str) -> Optional[Image.Image]:
        """预处理图像"""
        try:
            # 读取图像
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # 灰度化
            img = self._grayscale(img)
            
            # 去噪
            img = self._denoise(img)
            
            # 二值化
            img = self._binarize(img)
            
            # 调整大小
            img = self._resize(img)
            
            # 转换为PIL图像
            return Image.fromarray(img)
        except Exception:
            return None
    
    def _grayscale(self, img: np.ndarray) -> np.ndarray:
        """灰度化"""
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    def _denoise(self, img: np.ndarray) -> np.ndarray:
        """去噪"""
        return cv2.GaussianBlur(img, (5, 5), 0)
    
    def _binarize(self, img: np.ndarray) -> np.ndarray:
        """二值化"""
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return img
    
    def _resize(self, img: np.ndarray, max_size: int = 1024) -> np.ndarray:
        """调整大小"""
        height, width = img.shape
        if max(height, width) > max_size:
            scale = max_size / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height))
        return img
