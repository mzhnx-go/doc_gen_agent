# 内容生成器
from typing import Dict, List, Any, Optional
from src.utils.logger_handler import get_logger

logger = get_logger(__name__)


class ContentGenerator:
    """内容生成器"""
    
    def __init__(self, llm_client, rag_config: Optional[Dict[str, Any]] = None) -> None:
        """初始化内容生成器"""
        self.llm_client = llm_client
        self.rag_config = rag_config or {}
        logger.info("内容生成器初始化完成")
    
    def generate_content(self, plan: Dict[str, Any], parsed_content: Dict[str, Any]) -> Dict[str, Any]:
        """生成文档内容
        
        Args:
            plan: 文档规划
            parsed_content: 解析后的内容
            
        Returns:
            生成的文档内容
        """
        logger.info("开始生成文档内容")
        
        generated_content = {
            'title': self._generate_title(plan),
            'sections': [],
            'metadata': {
                'doc_type': plan.get('doc_type', 'document'),
                'objectives': plan.get('objectives', [])
            }
        }
        logger.info(f"文档标题生成完成: {generated_content['title']}")
        
        for idx, section in enumerate(plan.get('outline', [])):
            logger.info(f"生成章节 {idx + 1}/{len(plan.get('outline', []))}: {section.get('title', '')}")
            section_content = self._generate_section(section, parsed_content, generated_content)
            generated_content['sections'].append(section_content)
        
        logger.info("文档内容生成完成")
        return generated_content
    
    def _generate_title(self, plan: Dict[str, Any]) -> str:
        """生成文档标题"""
        prompt = f"基于以下文档规划，生成一个简洁专业的文档标题：\n\n文档类型：{plan.get('doc_type', '文档')}\n大纲：\n{plan.get('outline', [])}\n\n请只返回标题，不要有其他内容。"
        
        logger.debug(f"生成标题的提示词长度: {len(prompt)} 字符")
        response = self.llm_client.generate(prompt)
        title = response.strip()
        logger.debug(f"生成的标题: {title}")
        return title
    
    def _generate_section(self, section: Dict[str, Any], parsed_content: Dict[str, Any], global_context: Dict[str, Any]) -> Dict[str, Any]:
        """生成章节内容"""
        section_content = {
            'title': section.get('title', ''),
            'level': section.get('level', 1),
            'content': '',
            'subsections': []
        }
        
        prompt = self._build_section_prompt(section, parsed_content, global_context)
        logger.debug(f"生成章节 '{section.get('title', '')}' 的提示词长度: {len(prompt)} 字符")
        
        content = self.llm_client.generate(prompt)
        section_content['content'] = content
        
        for subsection in section.get('subsections', []):
            logger.debug(f"生成子章节: {subsection.get('title', '')}")
            subsection_content = self._generate_section(subsection, parsed_content, global_context)
            section_content['subsections'].append(subsection_content)
        
        return section_content
    
    def _build_section_prompt(self, section: Dict[str, Any], parsed_content: Dict[str, Any], global_context: Dict[str, Any]) -> str:
        """构建章节提示词"""
        relevant_content = []
        for file_info in parsed_content.get('files', []):
            if file_info.get('content'):
                relevant_content.append(file_info['content'])
        
        context = "\n".join(relevant_content[:3])
        
        prompt = f"""
请为以下章节生成详细内容：

章节标题：{section.get('title', '')}
章节说明：{section.get('content', '')}

文档标题：{global_context.get('title', '')}
文档类型：{global_context['metadata']['doc_type']}

参考资料：
{context}

要求：
1. 内容专业、准确、连贯
2. 符合章节主题
3. 适当引用参考资料中的信息
4. 保持与其他章节的一致性

请生成完整的章节内容。
"""
        
        return prompt
