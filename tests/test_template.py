"""
测试默认模板文件读取
"""
import os
import sys
import traceback

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.renderer.word_engine import WordEngine


def test_template_read():
    """测试默认模板文件读取"""
    print("开始测试默认模板文件读取...")
    
    # 初始化 Word 引擎
    templates_dir = "templates"
    word_engine = WordEngine(templates_dir)
    
    print(f"模板目录: {word_engine.templates_dir}")
    
    # 检查默认模板文件是否存在
    default_template_path = os.path.join(word_engine.templates_dir, 'default_template.docx')
    print(f"默认模板路径: {default_template_path}")
    
    if os.path.exists(default_template_path):
        print(f"✓ 默认模板文件存在")
        print(f"  文件大小: {os.path.getsize(default_template_path)} 字节")
    else:
        print(f"✗ 默认模板文件不存在")
        # 尝试创建默认模板
        print("  尝试创建默认模板...")
        try:
            word_engine._create_default_template(default_template_path)
            if os.path.exists(default_template_path):
                print(f"  ✓ 默认模板创建成功")
            else:
                print(f"  ✗ 默认模板创建失败")
        except Exception as e:
            print(f"  ✗ 创建模板时出错: {str(e)}")
    
    # 测试模板渲染
    print("\n测试模板渲染...")
    test_context = {
        'title': '测试文档',
        'sections': [
            {
                'level': 1,
                'title': '测试章节',
                'content': '这是测试章节的内容'
            }
        ],
        'metadata': {
            'doc_type': '测试报告'
        }
    }
    
    try:
        output_path = word_engine.render('default_template.docx', test_context)
        if output_path:
            print(f"✓ 模板渲染成功")
            print(f"  输出路径: {output_path}")
            if os.path.exists(output_path):
                print(f"  输出文件大小: {os.path.getsize(output_path)} 字节")
            else:
                print(f"  ✗ 输出文件不存在")
        else:
            print(f"✗ 模板渲染失败")
    except Exception as e:
        print(f"✗ 渲染时出错: {str(e)}")
        traceback.print_exc()
    
    print("\n测试完成！")


if __name__ == "__main__":
    test_template_read()
