# 第11周：API 基础与 LLM 入门

## 本周主题
从数据处理进入 AI 应用阶段，学习 API 调用基础和 LLM API 入门。

## 学习目标
1. 理解 API 和 HTTP 基础
2. 使用 requests 库调用公开 API
3. 初步体验 LLM API 调用（DeepSeek）
4. 掌握 API Key 安全管理

## 课堂内容

### 第一节：API 和 HTTP 基础（45分钟）

1. **什么是 API？**（15分钟）
   - API 是程序之间的通信接口
   - HTTP 请求方法：GET 获取数据，POST 发送数据
   - JSON 数据格式

2. **requests 库使用**（20分钟）
   - 安装：`pip install requests`
   - GET 请求：带参数查询
   - POST 请求：发送 JSON 数据
   - 状态码处理

3. **调用公开 API 实战**（10分钟）
   - GitHub API 示例
   - 错误处理最佳实践

### 第二节：LLM API 入门（45分钟）

1. **为什么需要 LLM API？**（10分钟）
   - 应用场景：聊天机器人、内容生成、代码助手
   - 与传统 API 的区别

2. **API Key 安全管理**（15分钟）
   - 环境变量 vs 硬编码
   - 创建 .env 文件
   - python-dotenv 使用

3. **调用 DeepSeek API**（20分钟）
   - 注册获取 API Key
   - 构建请求：URL + Headers + Messages
   - 解析响应，提取回复
   - 演示一次完整对话

## 课堂练习

### 练习 1：调用 GitHub API
用 AI 生成代码，获取指定用户的仓库列表：
- 处理 API 响应
- 提取仓库名、stars、描述
- 错误处理

### 练习 2：第一次 LLM 对话
1. 配置 .env 文件
2. 调用 DeepSeek API
3. 发送一个问题，获取回答

## Prompt 参考

```
帮我写一个 Python 函数调用 DeepSeek API：
- 使用 requests 库
- API Key 从环境变量读取
- 发送用户消息，返回 AI 回复
- 添加超时和错误处理
```

## 课后任务

### 任务：尝试 LLM API
1. 注册 DeepSeek 账号，获取 API Key
2. 配置本地 .env 文件
3. 编写代码完成一次对话
4. 尝试修改 System Prompt，观察效果变化

### REPORT.md 记录
- 你在调用 API 时遇到了什么问题？
- 如何解决的？
- LLM 的回答质量如何？

## 下周预告
第12周：LLM 应用开发
- 多轮对话实现
- Prompt Engineering 进阶
- 构建有特定人设的聊天机器人
