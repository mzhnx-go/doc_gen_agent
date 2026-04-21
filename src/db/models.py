# SQLAlchemy 模型定义
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DocumentTask(Base):
    """任务表"""
    __tablename__ = 'document_tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    doc_type = Column(String(50), nullable=False)  # 'word', 'ppt', 'pdf'
    status = Column(String(20), default='pending')  # 'pending', 'processing', 'completed'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    outlines = relationship('DocumentOutline', back_populates='task', cascade='all, delete-orphan')

class DocumentOutline(Base):
    """大纲表"""
    __tablename__ = 'document_outlines'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('document_tasks.id'), nullable=False)
    tree_structure = Column(JSON, nullable=False)  # 存储大纲树结构
    sort_order = Column(Integer, default=0)
    
    # 关系
    task = relationship('DocumentTask', back_populates='outlines')
    contents = relationship('GeneratedContent', back_populates='outline', cascade='all, delete-orphan')

class GeneratedContent(Base):
    """内容表"""
    __tablename__ = 'generated_contents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    outline_id = Column(Integer, ForeignKey('document_outlines.id'), nullable=False)
    text_content = Column(Text)
    image_paths = Column(JSON)  # 存储生成的图片路径列表
    table_data = Column(JSON)  # 存储表格数据
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    outline = relationship('DocumentOutline', back_populates='contents')
