# PDF 转换/生成引擎
import os
import subprocess
from typing import Optional

class PdfEngine:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
    
    def convert_word_to_pdf(self, word_path: str) -> Optional[str]:
        """将 Word 转换为 PDF"""
        try:
            # 检查 LibreOffice 是否可用
            if not self._check_libreoffice():
                return self._convert_with_comtypes(word_path)
            
            # 使用 LibreOffice 转换
            pdf_path = os.path.join(self.output_dir, os.path.basename(word_path).replace('.docx', '.pdf'))
            
            # 构建命令
            cmd = [
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', self.output_dir,
                word_path
            ]
            
            # 执行命令
            subprocess.run(cmd, check=True, capture_output=True)
            
            if os.path.exists(pdf_path):
                return pdf_path
            else:
                return None
        except Exception as e:
            print(f"PDF 转换错误: {str(e)}")
            return None
    
    def _check_libreoffice(self) -> bool:
        """检查 LibreOffice 是否可用"""
        try:
            subprocess.run(['soffice', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _convert_with_comtypes(self, word_path: str) -> Optional[str]:
        """使用 comtypes 转换（Windows 专用）"""
        try:
            import comtypes.client
            
            pdf_path = os.path.join(self.output_dir, os.path.basename(word_path).replace('.docx', '.pdf'))
            
            # 启动 Word
            word = comtypes.client.CreateObject('Word.Application')
            word.Visible = False
            
            # 打开文档
            doc = word.Documents.Open(word_path)
            
            # 保存为 PDF
            doc.SaveAs(pdf_path, FileFormat=17)  # 17 是 PDF 格式
            doc.Close()
            word.Quit()
            
            if os.path.exists(pdf_path):
                return pdf_path
            else:
                return None
        except Exception:
            return None
