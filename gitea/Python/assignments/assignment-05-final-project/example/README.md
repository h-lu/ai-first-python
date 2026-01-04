# 📔 智能日记助手

一句话描述：**记录日记，AI 分析情绪，生成月度总结**

这是一个结合了大语言模型（LLM）的智能日记管理工具，帮助你记录生活、追踪情绪变化、回顾成长历程。

## 功能特性

- ✅ **日记管理**：添加、查看、搜索、删除日记
- ✅ **标签系统**：为日记添加标签，方便分类
- ✅ **情绪分析**：🤖 AI 自动分析日记情绪（LLM 功能）
- ✅ **月度总结**：🤖 AI 生成月度回顾报告（LLM 功能）
- ✅ **写作建议**：🤖 AI 提供写作改进建议（LLM 功能）
- ✅ **双界面**：CLI 命令行 + Streamlit Web 界面

## 快速开始

### 环境要求

- Python 3.10+
- DeepSeek API Key（[获取地址](https://platform.deepseek.com/)）

### 安装

```bash
# 安装依赖
pip install -r requirements.txt
```

### 配置

1. 复制环境变量示例文件：

```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 DeepSeek API Key：

```
DEEPSEEK_API_KEY=sk-your-api-key-here
```

### 运行

#### CLI 模式

```bash
# 查看帮助
python src/main.py --help

# 添加日记
python src/main.py add --content "今天天气很好，心情不错"

# 添加带标签的日记
python src/main.py add --content "学习了 Python" --tags "学习,编程"

# 添加并自动分析情绪
python src/main.py add --content "..." --analyze

# 列出日记
python src/main.py list
python src/main.py list --month 2024-12 --limit 20

# 查看日记详情
python src/main.py show --id 1
python src/main.py show --date 2024-12-06

# 搜索日记
python src/main.py search "心情"

# 分析情绪（LLM）
python src/main.py analyze --id 1

# 生成月度总结（LLM）
python src/main.py summary --month 2024-12

# 获取写作建议（LLM）
python src/main.py suggest --id 1

# 导出日记
python src/main.py export --month 2024-12
```

#### Web 模式（Streamlit）

```bash
streamlit run app.py
```

然后在浏览器中打开 http://localhost:8501

## 使用示例

### CLI 示例输出

```bash
$ python src/main.py add --content "今天学习了装饰器，终于理解了闭包的概念！" --analyze

✅ 日记添加成功！
   ID: 1
   日期: 2024-12-06

🔍 正在分析情绪...
   情绪: 开心
```

```bash
$ python src/main.py summary --month 2024-12

📊 正在生成 2024-12 月度总结...
   共 15 篇日记

==================================================
📅 2024-12 月度总结
==================================================
📊 本月概况
这个月你记录了 15 篇日记，情绪以开心和平静为主...

✨ 本月亮点
- 学习了 Python 装饰器和闭包
- 完成了期末项目
...
```

## 项目结构

```
example/
├── src/
│   ├── __init__.py
│   ├── main.py          # CLI 入口
│   ├── diary.py         # 日记管理核心逻辑
│   ├── storage.py       # 存储管理
│   └── llm_features.py  # LLM 功能
├── app.py               # Streamlit Web 入口
├── data/                # 数据存储目录
├── output/              # 导出文件目录
├── manifest.yaml        # 项目运行声明
├── requirements.txt     # 依赖
├── .env.example         # 环境变量示例
├── README.md            # 本文件
├── REPORT.md            # 反思报告
└── CHANGELOG.md         # 版本记录
```

## 技术栈

- **数据存储**：JSON 文件
- **CLI**：argparse
- **Web**：Streamlit
- **LLM**：DeepSeek API (OpenAI 兼容接口)

## 作者

示例项目 - 供学生参考

