# 数据访问对象
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional, Dict, Any
from src.db.models import Base, DocumentTask, DocumentOutline, GeneratedContent

class DocumentRepository:
    def __init__(self, config: Dict[str, Any]):
        db_config = config['database']
        self.engine = create_engine(
            f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        )
        # 创建表
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_task(self, title: str, doc_type: str) -> DocumentTask:
        """创建任务"""
        session = self.Session()
        try:
            task = DocumentTask(title=title, doc_type=doc_type)
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        finally:
            session.close()
    
    def get_task(self, task_id: int) -> Optional[DocumentTask]:
        """获取任务"""
        session = self.Session()
        try:
            return session.query(DocumentTask).filter_by(id=task_id).first()
        finally:
            session.close()
    
    def update_task_status(self, task_id: int, status: str):
        """更新任务状态"""
        session = self.Session()
        try:
            task = session.query(DocumentTask).filter_by(id=task_id).first()
            if task:
                task.status = status
                session.commit()
        finally:
            session.close()
    
    def create_outline(self, task_id: int, tree_structure: Dict[str, Any]) -> DocumentOutline:
        """创建大纲"""
        session = self.Session()
        try:
            outline = DocumentOutline(
                task_id=task_id,
                tree_structure=tree_structure
            )
            session.add(outline)
            session.commit()
            session.refresh(outline)
            return outline
        finally:
            session.close()
    
    def create_content(self, outline_id: int, text_content: str, image_paths: List[str] = None, table_data: Dict[str, Any] = None) -> GeneratedContent:
        """创建内容"""
        session = self.Session()
        try:
            content = GeneratedContent(
                outline_id=outline_id,
                text_content=text_content,
                image_paths=image_paths,
                table_data=table_data
            )
            session.add(content)
            session.commit()
            session.refresh(content)
            return content
        finally:
            session.close()
    
    def get_tasks(self, status: Optional[str] = None) -> List[DocumentTask]:
        """获取任务列表"""
        session = self.Session()
        try:
            query = session.query(DocumentTask)
            if status:
                query = query.filter_by(status=status)
            return query.all()
        finally:
            session.close()
