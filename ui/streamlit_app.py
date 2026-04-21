# Streamlit 前端应用
import os
import sys
import streamlit as st
from pathlib import Path
import yaml

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.core.workflow import WorkflowController
# 加载配置
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 初始化工作流控制器
workflow = WorkflowController(config)

# 页面标题
st.title("文档生成智能体")

# 侧边栏
with st.sidebar:
    st.header("配置")
    
    # 文件上传
    uploaded_files = st.file_uploader(
        "上传文件", 
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg']
    )
    
    # 模板选择
    template_options = ['默认模板', '报告模板', '总结模板', '分析模板']
    selected_template = st.selectbox("选择模板", template_options)
    
    # 生成按钮
    generate_button = st.button("生成文档")

# 主区域
st.header("需求描述")

# 创建一个容器来包含输入框和上传功能
input_container = st.container()

with input_container:
    # 输入框
    user_prompt = st.text_area(
        "请描述您的文档需求",
        height=120,
        placeholder="例如：生成一份关于2024年市场分析的报告，基于上传的销售数据..."
    )
    
    # 输入框下方的工具栏
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    with col1:
        # 文件上传按钮
        if st.button("上传文件", use_container_width=True):
            # 触发文件上传对话框
            uploaded_files = st.file_uploader(
                "选择文件",
                accept_multiple_files=True,
                type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'],
                key="file_uploader"
            )
            if uploaded_files:
                st.success(f"已上传 {len(uploaded_files)} 个文件")
    
    with col2:
        # 模板选择下拉菜单
        template_options = ['默认模板', '报告模板', '总结模板', '分析模板']
        selected_template = st.selectbox("选择模板", template_options, key="template_select", label_visibility="collapsed")
    
    with col3:
        # 生成按钮
        generate_button = st.button("生成文档", use_container_width=True)

# 处理生成请求
if generate_button and user_prompt:
    # 保存上传的文件
    uploads_dir = os.path.join('uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    input_files = []
    # 检查是否有上传的文件
    if 'file_uploader' in st.session_state:
        uploaded_files = st.session_state.file_uploader
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = os.path.join(uploads_dir, uploaded_file.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                input_files.append(file_path)
    
    # 显示处理状态
    with st.spinner("正在处理..."):
        # 调用工作流
        result = workflow.process_document(input_files, user_prompt)
        
        if result['status'] == 'success':
            st.success("文档生成成功！")
            st.info(f"文档类型：{result['document_type']}")
            
            # 显示大纲
            st.subheader("生成的大纲")
            for section in result.get('outline', []):
                st.markdown(f"**{section['title']}**")
                if 'subsections' in section:
                    for subsection in section['subsections']:
                        st.markdown(f"  - {subsection['title']}")
            
            # 提供下载链接
            if 'output_path' in result and result['output_path']:
                output_path = result['output_path']
                if os.path.exists(output_path):
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label="下载文档",
                            data=f,
                            file_name=os.path.basename(output_path),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
        else:
            st.error(f"生成失败：{result.get('message', '未知错误')}")

# 历史记录
st.sidebar.header("历史记录")
st.sidebar.info("生成的文档将显示在这里")
