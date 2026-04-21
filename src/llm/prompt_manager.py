# 提示词加载与管理
import os
import yaml
from typing import Dict, Any, Optional

class PromptManager:
    def __init__(self, prompts_dir: str):
        self.prompts_dir = prompts_dir
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, Any]:
        """加载提示词配置"""
        prompts = {}
        
        if not os.path.exists(self.prompts_dir):
            return prompts
        
        for filename in os.listdir(self.prompts_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                file_path = os.path.join(self.prompts_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data:
                            prompts.update(data)
                except Exception as e:
                    print(f"加载提示词文件失败: {filename}, 错误: {str(e)}")
        
        return prompts
    
    def get_prompt(self, category: str, prompt_type: str) -> Optional[str]:
        """获取提示词"""
        if category in self.prompts:
            category_data = self.prompts[category]
            if prompt_type in category_data:
                return category_data[prompt_type]
        return None
    
    def get_system_prompt(self, task: str) -> Optional[str]:
        """获取系统提示词"""
        return self.get_prompt('document_analysis', 'system')
    
    def reload_prompts(self):
        """重新加载提示词"""
        self.prompts = self._load_prompts()
