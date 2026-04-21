# 文档生成智能体 (Document Generation Agent)

一个端到端的文档生成智能体，能够接收多模态输入（文本、图片、文档等），通过本地大语言模型进行理解、规划、内容生成，最终自动填充模板并输出格式规范的文档。

## 功能特性

- **多模态输入**：支持 PDF、Word、图片、文本等多种格式
- **本地模型**：使用 LM Studio 运行本地大模型，保护数据隐私
- **智能规划**：自动生成文档大纲和结构
- **内容生成**：基于输入内容和模板生成高质量文档
- **模板系统**：支持自定义 Word 模板
- **Streamlit 界面**：友好的 Web 交互界面

## 技术栈

- **后端**：Python, LangChain
- **大模型**：LM Studio (OpenAI 兼容 API)
- **模型**：Qwen3.5-4b (本地部署)
- **文档处理**：python-docx, python-docxtpl, pypdf
- **图像处理**：OpenCV, Tesseract OCR
- **前端**：Streamlit
- **数据库**：PostgreSQL

## 快速开始

### 1. 环境准备

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 安装 Tesseract OCR (用于图片识别)
- Windows: 下载并安装 https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt install tesseract-ocr`
- macOS: `brew install tesseract`

#### 启动 LM Studio
1. 下载并安装 LM Studio: https://lmstudio.ai/
2. 下载 Qwen3.5-4b 模型
3. 启动本地服务器 (默认端口 1234)

### 2. 配置

编辑 `config/settings.yaml` 文件：

```yaml
# LM Studio 配置
llm:
  base_url: "http://localhost:1234/v1"
  model: "qwen3.5-4b@q4_k_s" (换成使用的模型)

# PostgreSQL 配置 (可选)
database:
  host: "localhost"
  port: 5432
  user: "root"
  password: "root"
  database: "doc_gen_agent"
```

### 3. 运行应用

```bash
cd doc_gen_agent
streamlit run ui/streamlit_app.py
```

然后在浏览器中打开 http://localhost:8501

## 使用方法

1. **上传文件**：在侧边栏上传 PDF、Word、图片等文件
2. **描述需求**：在主区域输入文档生成需求
3. **选择模板**：选择适合的文档模板
4. **生成文档**：点击 "生成文档" 按钮
5. **下载结果**：生成完成后下载文档

## 项目结构

```
doc_gen_agent/
├── config/            # 配置文件
├── src/               # 核心代码
│   ├── core/         # 核心业务逻辑
│   ├── multimodal/   # 多模态处理
│   ├── llm/          # 模型交互
│   ├── db/           # 数据库
│   ├── renderer/     # 文档渲染
│   └── utils/        # 工具函数
├── templates/        # 文档模板
├── ui/               # 前端界面
├── output/           # 生成的文档
├── uploads/          # 上传的文件
└── main.py           # 启动入口
```

## 模板系统

在 `templates/` 目录下可以添加自定义模板，使用 Jinja2 语法：

```docx
{{title}}

{{#sections}}
{{level}}. {{title}}

{{content}}

{{#subsections}}
{{level}}.{{level}} {{title}}

{{content}}
{{/subsections}}
{{/sections}}
```

## 故障排除

1. **LM Studio 连接失败**：确保 LM Studio 已启动，且端口正确
2. **OCR 识别失败**：确保 Tesseract OCR 已正确安装并配置路径
3. **PDF 解析错误**：确保 PDF 文件未加密且可读取
4. **内存不足**：对于大文件，可能需要增加系统内存

## 未来计划

- [ ] 支持 PPT 生成
- [ ] 集成 RAG 知识库
- [ ] 添加更多模板
- [ ] 支持批量处理
- [ ] 优化生成质量


