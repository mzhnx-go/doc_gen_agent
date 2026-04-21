# 主工作流控制器
import os
import re
from typing import Dict, List, Any, Optional
from src.multimodal.parser import FileParser
from src.core.planner import DocumentPlanner
from src.core.generator import ContentGenerator
from src.renderer.word_engine import WordEngine
from src.llm.client import LLMClient
from src.utils.file_handler import FileHandler
from src.utils.logger_handler import get_logger

logger = get_logger(__name__)


class WorkflowController:
    """文档生成工作流控制器"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """初始化工作流控制器"""
        self.config = config
        self.llm_client = LLMClient(config['llm'])
        self.file_parser = FileParser(config['multimodal'])
        self.document_planner = DocumentPlanner(self.llm_client)
        self.content_generator = ContentGenerator(self.llm_client, config.get('rag', {}))
        self.word_engine = WordEngine(config['paths']['templates'])
        self.file_handler = FileHandler()
        logger.info("工作流控制器初始化完成")
    
    def process_document(self, input_files: List[str], user_prompt: str) -> Dict[str, Any]:
        """处理文档生成流程
        
        Args:
            input_files: 输入文件路径列表
            user_prompt: 用户提示词
            
        Returns:
            处理结果字典
        """
        logger.info(f"开始处理文档，输入文件数: {len(input_files)}")
        
        try:
            parsed_content = self._parse_inputs(input_files, user_prompt)
            logger.info("步骤1: 多模态输入解析完成")
            
            plan = self._plan_document(parsed_content, user_prompt)
            logger.info(f"步骤2: 文档规划完成，类型: {plan.get('doc_type', 'unknown')}")
            
            generated_content = self._generate_content(plan, parsed_content)
            logger.info("步骤3: 内容生成完成")
            
            output_path = self._render_document(plan, generated_content)
            logger.info(f"步骤4: 文档渲染完成，输出路径: {output_path}")
            
            return {
                'status': 'success',
                'output_path': output_path,
                'document_type': plan.get('doc_type', 'document'),
                'outline': plan.get('outline', [])
            }
        except Exception as e:
            logger.error(f"文档处理失败: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _parse_inputs(self, input_files: List[str], user_prompt: str) -> Dict[str, Any]:
        """解析输入文件"""
        parsed_content = {
            'user_prompt': user_prompt,
            'files': []
        }
        
        for file_path in input_files:
            if os.path.exists(file_path):
                logger.debug(f"解析文件: {file_path}")
                file_info = self.file_parser.parse(file_path)
                parsed_content['files'].append(file_info)
        
        return parsed_content
    
    def _plan_document(self, parsed_content: Dict[str, Any], user_prompt: str) -> Dict[str, Any]:
        """规划文档结构"""
        return self.document_planner.plan_document(parsed_content, user_prompt)
    
    def _generate_content(self, plan: Dict[str, Any], parsed_content: Dict[str, Any]) -> Dict[str, Any]:
        """生成文档内容"""
        return self.content_generator.generate_content(plan, parsed_content)
    
    def _render_document(self, plan: Dict[str, Any], generated_content: Dict[str, Any]) -> str:
        """渲染文档"""
        # 获取文档标题
        document_title = generated_content.get('title', '文档')
        
        # 清理文件名中的非法字符
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', document_title)
        # 限制文件名长度
        safe_title = safe_title[:50]
        
        # 使用文档标题作为模板名的一部分
        template_name = plan.get('template', 'default_template.docx')
        base_template_name = os.path.basename(template_name)
        name_without_ext = os.path.splitext(base_template_name)[0]
        new_template_name = f"{safe_title}_{name_without_ext}.docx"
        
        output_path = self.word_engine.render(new_template_name, generated_content)
        logger.info(f"使用文档标题生成文件名: {new_template_name}")
        return output_path
