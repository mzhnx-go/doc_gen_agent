# 测试工作流
import os
import sys
import yaml
import re

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.core.workflow import WorkflowController


def test_workflow():
    """测试工作流"""
    # 加载配置
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'settings.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 初始化工作流控制器
    workflow = WorkflowController(config)
    print("工作流控制器初始化成功")
    
    # 测试文件路径
    test_files = []
    test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', 'test_data')
    os.makedirs(test_data_dir, exist_ok=True)
    
    # 创建测试文件
    test_file = os.path.join(test_data_dir, 'test.txt')
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write('这是一份关于中国旅游业发展现状与未来趋势的研究材料，用于生成专业行业分析报告。\n\n主要内容包括：\n1. 中国旅游业市场规模与复苏情况\n2. 国内旅游消费行为新变化与新趋势\n3. 智慧旅游与数字化技术在旅游业的应用\n4. 文旅融合发展现状与典型案例\n5. 乡村旅游与休闲度假产业发展情况\n6. 未来旅游业可持续发展面临的挑战与对策建议')
    test_files.append(test_file)
    
    # 测试用户提示
    user_prompt = "基于测试文件，生成一份中国旅游业发展现状与未来趋势的专业分析报告"
    
    # 运行工作流
    print("开始测试工作流...")
    result = workflow.process_document(test_files, user_prompt)
    
    print(f"测试结果: {result}")
    
    if result['status'] == 'success':
        print(f"生成成功！输出路径: {result['output_path']}")
        
        # 从结果中提取文档标题（如果有）
        document_title = "测试报告"
        if 'outline' in result:
            # 简单处理：使用大纲的第一个标题作为文档标题
            outline = result['outline']
            if outline and isinstance(outline, list) and len(outline) > 0:
                if isinstance(outline[0], dict) and 'title' in outline[0]:
                    document_title = outline[0]['title']
        
        # 生成新的文件名
        # 清理文件名中的非法字符
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', document_title)
        # 限制文件名长度
        safe_title = safe_title[:50]
        
        # 构建新的文件路径
        output_dir = os.path.dirname(result['output_path'])
        new_filename = f"{safe_title}.docx"
        new_output_path = os.path.join(output_dir, new_filename)
        
        # 重命名文件
        if os.path.exists(result['output_path']):
            os.rename(result['output_path'], new_output_path)
            print(f"文件已重命名为: {new_output_path}")
        
        return True
    else:
        print(f"生成失败: {result.get('message', '未知错误')}")
        return False


if __name__ == "__main__":
    test_workflow()
