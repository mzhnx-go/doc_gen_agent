# JSON 解析器
import json
from typing import Dict, Any, Optional

class JsonParser:
    @staticmethod
    def parse(json_str: str) -> Optional[Dict[str, Any]]:
        """解析 JSON 字符串"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    
    @staticmethod
    def serialize(data: Any) -> str:
        """序列化数据为 JSON 字符串"""
        try:
            return json.dumps(data, ensure_ascii=False, indent=2)
        except Exception:
            return ""
    
    @staticmethod
    def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
        """从文本中提取 JSON"""
        try:
            # 查找 JSON 开始和结束位置
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
            return None
        except Exception:
            return None
