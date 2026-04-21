# Pydantic 数据模型
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class OutlineNode(BaseModel):
    """大纲节点模型"""
    title: str
    level: int
    content: Optional[str] = ""
    children: Optional[List['OutlineNode']] = None


class SectionContent(BaseModel):
    """章节内容模型"""
    title: str
    level: int
    content: str
    subsections: Optional[List['SectionContent']] = []


class GeneratedDocument(BaseModel):
    """生成的文档模型"""
    title: str
    doc_type: str
    sections: List[SectionContent]
    metadata: Dict[str, Any]


class DocumentTask(BaseModel):
    """文档任务模型"""
    task_id: int
    title: str
    doc_type: str
    status: str
    created_at: Optional[datetime] = None
    outline: Optional[List[OutlineNode]] = None


class FileInfo(BaseModel):
    """文件信息模型"""
    path: str
    type: str
    size: float
    content: Optional[str] = ""
    summary: Optional[str] = ""
    metadata: Optional[Dict[str, Any]] = {}


class ParsedContent(BaseModel):
    """解析后的内容模型"""
    user_prompt: str
    files: List[FileInfo]


class PlanningResult(BaseModel):
    """规划结果模型"""
    doc_type: str
    outline: List[OutlineNode]
    objectives: List[str]
    template: Optional[str] = "default_template.docx"
