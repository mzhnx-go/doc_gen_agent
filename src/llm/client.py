# LM Studio 客户端封装
import json
import requests
from typing import Dict, Any, Optional
from src.utils.logger_handler import get_logger

logger = get_logger(__name__)


class LLMClient:
    """LLM 客户端"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """初始化 LLM 客户端"""
        self.config = config
        self.base_url = config.get('base_url', 'http://localhost:1234/v1')
        self.model = config.get('model', 'qwen3.5-4b')
        self.timeout = config.get('timeout', 60)
        logger.info(f"LLM 客户端初始化完成，模型: {self.model}, URL: {self.base_url}")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成文本
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            
        Returns:
            生成的文本内容
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.config.get('temperature', 0.7),
            "max_tokens": self.config.get('max_tokens', 4096)
        }
        
        try:
            logger.debug(f"发送请求到 {self.base_url}/chat/completions")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                logger.debug(f"收到响应，长度: {len(content)} 字符")
                return content
            else:
                logger.warning("响应中没有 choices 字段")
                return ""
        except Exception as e:
            logger.error(f"LLM 请求错误: {str(e)}")
            return ""
    
    def generate_stream(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """流式生成文本
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            
        Returns:
            生成的文本内容
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.config.get('temperature', 0.7),
            "max_tokens": self.config.get('max_tokens', 4096),
            "stream": True
        }
        
        try:
            logger.debug(f"发送流式请求到 {self.base_url}/chat/completions")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=self.timeout,
                stream=True
            )
            
            response.raise_for_status()
            
            full_content = ""
            for chunk in response.iter_lines():
                if chunk:
                    chunk_data = chunk.decode('utf-8')
                    if chunk_data.startswith('data: '):
                        chunk_data = chunk_data[6:]
                        if chunk_data == '[DONE]':
                            break
                        try:
                            chunk_json = json.loads(chunk_data)
                            if 'choices' in chunk_json and len(chunk_json['choices']) > 0:
                                delta = chunk_json['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    full_content += content
                        except json.JSONDecodeError:
                            pass
            
            logger.debug(f"流式响应完成，总长度: {len(full_content)} 字符")
            return full_content
        except Exception as e:
            logger.error(f"流式请求错误: {str(e)}")
            return ""
