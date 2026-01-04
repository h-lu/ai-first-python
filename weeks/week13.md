# 第13周：Web 应用基础

## 本周主题
学习使用 Streamlit/Gradio 快速构建 Web 界面，将命令行程序转化为可交互的 Web 应用。

## 学习目标
1. 理解 Web 应用基础架构
2. 使用 Streamlit 快速构建 Web 界面
3. 为 AI 应用添加交互界面
4. 了解部署基础

## 课堂内容

### 第一节：Web 应用概述与 Streamlit（45分钟）

1. **Web 应用基础架构**（10分钟）
   - 前端 vs 后端
   - 传统开发 vs 快速原型
   - 为什么选择 Streamlit/Gradio

2. **Streamlit 快速入门**（20分钟）
   - 安装：`pip install streamlit`
   - Hello World：`st.title()`, `st.write()`
   - 运行：`streamlit run app.py`

3. **常用组件**（15分钟）
   - 输入：`st.text_input()`, `st.selectbox()`, `st.slider()`
   - 显示：`st.markdown()`, `st.dataframe()`, `st.pyplot()`
   - 布局：`st.columns()`, `st.sidebar`

### 第二节：实战应用开发（45分钟）

1. **数据可视化应用**（15分钟）
   - 文件上传：`st.file_uploader()`
   - Pandas 数据展示
   - 动态图表生成

2. **AI 聊天界面**（20分钟）
   - `st.chat_input()` 和 `st.chat_message()`
   - 对话历史显示
   - 集成 LLM API

3. **部署基础**（10分钟）
   - Streamlit Cloud 免费部署
   - requirements.txt 配置
   - 环境变量管理

## 课堂练习

### 练习 1：数据分析仪表板
将之前的数据分析代码改造成 Web 应用：
- 支持 CSV 文件上传
- 显示数据预览
- 自动生成基础图表

### 练习 2：AI 聊天界面
为上周的聊天机器人添加 Web 界面：
- 使用 Streamlit chat 组件
- 显示对话历史
- 支持清空对话

## Prompt 参考

```
帮我用 Streamlit 创建一个数据分析应用：
- 支持上传 CSV 文件
- 显示数据基本信息（行数、列名）
- 生成一个柱状图展示某列分布
- 添加筛选功能
```

```
帮我用 Streamlit 创建一个 AI 聊天界面：
- 使用 st.chat_input 和 st.chat_message
- 调用 DeepSeek API
- 在侧边栏显示 System Prompt 设置
- 支持清空对话历史
```

## 课后任务

### 项目进展
1. 完成项目核心功能开发
2. 添加 Web 界面（如适用）
3. 编写 README.md

### Streamlit 练习
选择以下任一练习完成：
- 将作业 4 的数据可视化改造成 Web 应用
- 为期末项目添加 Streamlit 界面

## 下周预告
第14-15周：综合项目开发
- 项目开发与迭代
- 代码审查与优化
- 准备项目展示
