# 文档规划器
import json
from typing import Dict, List, Any
from src.utils.logger_handler import get_logger

logger = get_logger(__name__)


class DocumentPlanner:
    """文档规划器"""
    
    def __init__(self, llm_client) -> None:
        """初始化文档规划器"""
        self.llm_client = llm_client
        logger.info("文档规划器初始化完成")
    
    def plan_document(self, parsed_content: Dict[str, Any], user_prompt: str) -> Dict[str, Any]:
        """规划文档结构
        
        Args:
            parsed_content: 解析后的内容
            user_prompt: 用户提示词
            
        Returns:
            规划结果字典
        """
        logger.info("开始规划文档结构")
        
        prompt = self._build_planning_prompt(parsed_content, user_prompt)
        logger.debug(f"规划提示词长度: {len(prompt)} 字符")
        
        response = self.llm_client.generate(prompt)
        logger.debug(f"LLM 响应长度: {len(response)} 字符")
        
        plan = self._parse_planning_response(response)
        logger.info(f"文档规划完成，类型: {plan.get('doc_type', 'unknown')}")
        
        plan['template'] = self._select_template(plan.get('doc_type', 'document'))
        
        return plan
    
    def _build_planning_prompt(self, parsed_content: Dict[str, Any], user_prompt: str) -> str:
        """构建规划提示词"""
        files_summary = []
        for file_info in parsed_content.get('files', []):
            files_summary.append(f"文件类型: {file_info.get('type')}, 内容摘要: {file_info.get('summary', '')}")
        
        files_text = "\n".join(files_summary)
        
        prompt = f"""
请根据用户需求和输入文件，规划文档结构：

用户需求：{user_prompt}

输入文件：
{files_text}

请输出以下信息：
1. 文档类型（如报告、总结、分析等）
2. 详细大纲（包含标题层级和简要内容说明）
3. 文档的主要目标和范围

请以JSON格式输出，结构如下：
{{
  "doc_type": "文档类型",
  "outline": [
    {{"level": 1, "title": "标题1", "content": "内容说明"}},
    {{"level": 1, "title": "标题2", "content": "内容说明", "subsections": [
      {{"level": 2, "title": "子标题2.1", "content": "内容说明"}}
    ]}}
  ],
  "objectives": ["目标1", "目标2"]
}}
"""
        
        return prompt
    
    def _parse_planning_response(self, response: str) -> Dict[str, Any]:
        """解析规划响应"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"JSON 解析失败: {str(e)}，使用默认规划")
        
        return {
            "doc_type": "报告",
            "outline": [
                {"level": 1, "title": "引言", "content": "介绍文档背景和目的"},
                {"level": 1, "title": "主体内容", "content": "详细内容"},
                {"level": 1, "title": "结论", "content": "总结和建议"}
            ],
            "objectives": ["满足用户需求"]
        }
    
    def _select_template(self, doc_type: str) -> str:
        """选择模板"""
        template_map = {
            '报告': 'report_template.docx',
            '总结': 'summary_template.docx',
            '分析': 'analysis_template.docx',
            '计划': 'plan_template.docx'
        }
        template = template_map.get(doc_type, 'default_template.docx')
        logger.debug(f"为文档类型 '{doc_type}' 选择模板: {template}")
        return template
