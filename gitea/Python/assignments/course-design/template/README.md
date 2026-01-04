# 课程设计模板（Python 程序设计）

> 基于 DeepSeek API + Streamlit 的 AI 应用课程设计。自动评分覆盖 80 分（功能 25 + 创意体验 20 + 技术实现 20 + 开发心得 15），展示表现与学习态度由教师人工评定。

## 快速开始

1. 创建虚拟环境并安装依赖
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: .\\venv\\Scripts\\activate
   pip install -r requirements.txt
   ```
2. 配置密钥
   ```bash
   cp .env.example .env
   # 在 .env 中填入 DEEPSEEK_API_KEY
   ```
3. 运行项目（示例）
   ```bash
   # CLI 示例（请根据你的实现修改）
   python src/main.py --help

   # 若有 Web 界面
   # streamlit run app.py --server.headless true
   ```

## manifest.yaml（必改）
- `project.name`/`description`：写真实的项目名称与一句话介绍，勿留模板占位。
- `commands.demo`：至少 3 个演示命令，覆盖核心流程与 LLM 功能。
- `commands.error_handling`：至少 2 个异常/无效输入的演示命令，不能崩溃。
- `env_vars`：列出需要的环境变量（如 DEEPSEEK_API_KEY）。

## 评分对照（自动 80 分）

| 维度 | 分值 | 要点 |
| --- | --- | --- |
| 功能完成度 | 25 | 核心功能可跑通；LLM 集成有效；错误处理不崩溃；流程可演示 |
| 创意与体验 | 20 | 界面/交互清晰，有状态提示与示例；解决真实痛点；有亮点/创新 |
| 技术实现 | 20 | 代码分层清晰；命名/注释可读；密钥用环境变量；遵循工程实践 |
| 开发心得 | 15 | >500 字，包含选题思考、AI 协作、真实反思与改进方向 |

> 提示：缺少 LLM 功能会直接拉低功能与技术分；API Key 不得硬编码。

## 提交前自查
- README、REPORT、CHANGELOG 均已填写，无占位符。
- manifest.yaml 已更新，演示/错误处理命令可运行且展示 LLM。
- `.env.example` 存在，代码用 `os.getenv` 读取密钥。
- 错误输入不会输出 Traceback。
- REPORT.md 字数 ≥ 500，内容真实具体。

## 目录结构
```
project/
├── src/               # 业务与 LLM 调用代码
├── app.py             # 如有 Streamlit 界面
├── manifest.yaml      # 运行声明（必填）
├── requirements.txt
├── README.md
├── REPORT.md
└── CHANGELOG.md
```
