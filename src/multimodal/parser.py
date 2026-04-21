# 多模态文件解析器
import os
from typing import Dict, Any, Optional
from PIL import Image
import pytesseract
from pypdf import PdfReader
from docx import Document
from src.utils.logger_handler import get_logger

logger = get_logger(__name__)


class FileParser:
    """多模态文件解析器"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """初始化文件解析器"""
        self.config = config
        tesseract_path = config.get('ocr', {}).get('tesseract_path')
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        logger.info("文件解析器初始化完成")
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """解析文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        logger.info(f"开始解析文件: {file_path}")
        
        file_info = {
            'path': file_path,
            'type': self._get_file_type(file_path),
            'size': os.path.getsize(file_path) / (1024 * 1024),
            'content': '',
            'summary': '',
            'metadata': {}
        }
        
        try:
            if file_info['type'] == 'pdf':
                file_info['content'] = self._parse_pdf(file_path)
                logger.debug(f"PDF 文件解析完成，长度: {len(file_info['content'])} 字符")
            elif file_info['type'] == 'docx':
                file_info['content'] = self._parse_docx(file_path)
                logger.debug(f"Word 文件解析完成，长度: {len(file_info['content'])} 字符")
            elif file_info['type'] == 'txt':
                file_info['content'] = self._parse_txt(file_path)
                logger.debug(f"文本文件解析完成，长度: {len(file_info['content'])} 字符")
            elif file_info['type'] in ['png', 'jpg', 'jpeg']:
                file_info['content'] = self._parse_image(file_path)
                logger.debug(f"图片 OCR 解析完成，长度: {len(file_info['content'])} 字符")
            
            file_info['summary'] = self._generate_summary(file_info['content'])
            logger.info(f"文件解析完成: {file_path}, 类型: {file_info['type']}")
        except Exception as e:
            logger.error(f"文件解析失败: {file_path}, 错误: {str(e)}")
            file_info['error'] = str(e)
        
        return file_info
    
    def _get_file_type(self, file_path: str) -> str:
        """获取文件类型"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return 'pdf'
        elif ext == '.docx':
            return 'docx'
        elif ext == '.txt':
            return 'txt'
        elif ext in ['.png', '.jpg', '.jpeg']:
            return ext[1:]
        else:
            return 'unknown'
    
    def _parse_pdf(self, file_path: str) -> str:
        """解析PDF文件"""
        content = []
        reader = PdfReader(file_path)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                content.append(f"第{page_num + 1}页:\n{text}")
        return '\n'.join(content)
    
    def _parse_docx(self, file_path: str) -> str:
        """解析Word文件"""
        content = []
        doc = Document(file_path)
        for para in doc.paragraphs:
            if para.text:
                content.append(para.text)
        return '\n'.join(content)
    
    def _parse_txt(self, file_path: str) -> str:
        """解析文本文件"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def _parse_image(self, file_path: str) -> str:
        """解析图片文件（OCR）"""
        try:
            img = Image.open(file_path)
            lang = self.config.get('ocr', {}).get('lang', 'chi_sim+eng')
            text = pytesseract.image_to_string(img, lang=lang)
            logger.debug(f"OCR 识别完成，识别文字长度: {len(text)} 字符")
            return f"[图片OCR结果]\n{text}"
        except Exception as e:
            logger.warning(f"图片 OCR 解析失败: {str(e)}")
            return "[无法解析图片]"
    
    def _generate_summary(self, content: str) -> str:
        """生成内容摘要"""
        if not content:
            return ""
        return content[:500] + ('...' if len(content) > 500 else '')
