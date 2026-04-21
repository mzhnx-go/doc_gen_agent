# 项目启动入口
import os
import yaml
from src.core.workflow import WorkflowController

def main():
    """主函数"""
    # 加载配置
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 确保目录存在
    for dir_path in ['output', 'uploads', 'rag_knowledge']:
        os.makedirs(dir_path, exist_ok=True)
    
    print("文档生成智能体启动中...")
    print(f"LM Studio URL: {config['llm']['base_url']}")
    print(f"模型: {config['llm']['model']}")
    
    # 初始化工作流控制器
    workflow = WorkflowController(config)
    print("工作流控制器初始化完成")
    
    # 启动 Streamlit 应用
    print("启动 Streamlit 应用...")
    print("请在浏览器中打开 http://localhost:8501")
    
    # 注意：实际运行时，应该使用命令行启动 Streamlit
    # 这里只是作为入口文件
    print("\n使用以下命令启动应用：")
    print("cd doc_gen_agent && streamlit run ui/streamlit_app.py")

if __name__ == "__main__":
    main()
