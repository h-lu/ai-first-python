#!/usr/bin/env python3
"""
期末项目 LLM 评估脚本
根据 run_results.json 和 rubric 进行评分
"""

import json
import argparse
import requests
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# ============== Prompt 模板 ==============

DOCUMENTATION_PROMPT = """你是严格且一致的助教，正在评估学生期末项目的文档质量。

## 评分核心原则

你的任务是判断文档是否体现了学生的**真实思考和实际工作**。评分依据是**内容的实质性**，而非格式的完整性。

### 各评分项的详细判断标准

#### 1. 项目定位 (report_positioning) - 1分
| 有意义（1分） | 无意义（0分） |
|--------------|--------------|
| 描述了具体要解决的问题、目标用户、选择理由 | 占位符"[在此填写]"、泛泛的"完成作业"、空白 |

#### 2. 技术决策 (report_decisions) - 2分

**评估内容包括两部分**：
1. **技术选型**：关键技术选型表格（数据存储、用户界面、LLM提供商等）、最难的技术决策
2. **与 AI 协作**：最有效的 Prompt 示例、为什么有效、AI 帮不了的地方

| 分数 | 标准 |
|------|------|
| 0分 | 无技术决策说明，或只说"AI建议的"；与 AI 协作部分空白或只有"[你的Prompt]"占位符 |
| 1分 | 有决策说明但缺乏替代方案对比；或与 AI 协作部分只是敷衍填写（如"Prompt有效因为好用"） |
| 2分 | 有替代方案对比且理由充分；与 AI 协作部分有真实的 Prompt 示例和具体分析 |

#### 3. 迭代记录 (report_iteration) - 1分
| 有意义（1分） | 无意义（0分） |
|--------------|--------------|
| 描述了真实遇到的挑战、尝试的解决方案、学到的经验 | 空洞的"挑战"、"解决方案"占位符 |

#### 4. 自我反思 (report_reflection) - 1分
| 有意义（1分） | 无意义（0分） |
|--------------|--------------|
| 有具体的优点、缺点、遗憾点分析 | 套话"收获很大"、"学到很多"、空白 |

#### 5. 版本记录数量 (changelog_versions) - 2分
| 分数 | 标准 |
|------|------|
| 0分 | 无版本记录，或只有1个版本且内容简略；日期是"YYYY-MM-DD"模板格式 |
| 1分 | 有2个版本，能看出一定的迭代过程 |
| 2分 | 有3个及以上版本，每版有实质性变化，日期是真实日期 |

#### 6. 版本记录详细程度 (changelog_detail) - 1分
| 有意义（1分） | 无意义（0分） |
|--------------|--------------|
| 记录详细，说明了改动原因、具体修改内容 | 只有"修复XXX问题"、"完成XXX功能"等占位符 |

### 关键判断点

1. **REPORT.md 是否真正填写？**
   - 看项目名称是否是具体的（如"智能日记助手"），而非"[在此填写项目名称]"
   - 看问题回答是否有具体内容，而非"[在此处回答]"或空白
   - 看技术决策表格是否填写了真实选择，而非"[例：JSON]"
   - **看"与 AI 协作"部分是否有真实的 Prompt 示例**，而非"[你的Prompt]"

2. **CHANGELOG.md 是否记录了真实迭代？**
   - 看日期是否是真实日期（如2024-12-06），而非"YYYY-MM-DD"
   - 看变更内容是否具体（如"修复月度总结在没有日记时崩溃的问题"），而非"修复 XXX 问题"
   - 看是否能从记录中看出项目的演进过程

3. **README.md 是否描述了真实项目？**
   - 看标题是否是具体项目名，而非"项目名称"
   - 看功能列表是否具体，而非"功能 1：描述"

## 学生提交的文档

### README.md
<<<README_CONTENT>>>

### REPORT.md (反思报告)
<<<REPORT_CONTENT>>>

### CHANGELOG.md (版本记录)
<<<CHANGELOG_CONTENT>>>

## 实际代码和运行情况（用于交叉验证）

### 源代码文件列表
<<<SOURCE_FILES>>>

### 命令运行结果摘要
<<<RUN_SUMMARY>>>

## 一致性检查（重要！）

**文档内容必须与实际代码/运行结果一致**。请对比验证：

1. **技术决策验证**：
   - REPORT.md 中声称使用的技术（如 LLM、数据存储方式），代码文件中是否有对应实现？
   - 如果文档说"使用了 DeepSeek API 进行情绪分析"，但源代码中没有 LLM 相关文件 → 技术决策应扣分

2. **功能描述验证**：
   - REPORT.md 中描述的功能，运行结果中是否有体现？
   - 如果文档说"实现了完善的错误处理"，但运行结果显示有多个命令失败 → 自我反思应扣分

3. **不一致的处罚**：
   - 文档夸大描述、与实际不符 → 对应评分项 **0 分**
   - 文档描述的功能在代码中完全不存在 → 视为虚假描述，技术决策 **0 分**

## 评分量表
<<<RUBRIC>>>

## 评分规则
- **严格根据内容的实质性评分**，不要被格式完整性欺骗
- **文档内容必须与实际代码一致**，夸大或虚假描述应扣分
- 模板占位符、空白、套话 = 没有内容 = 0 分
- 只有真正体现学生思考的具体内容才能得分
- 每项只能给出 scoring_guide 中定义的整数分值
- 只输出 JSON，不输出任何解释

## 输出格式（严格JSON）
{
  "total": number,
  "criteria": [
    {"id": "评分项id", "score": 整数, "reason": "简短评语，说明为什么给这个分数"},
    ...
  ],
  "flags": [],
  "confidence": number(0-1)
}
"""

FUNCTIONALITY_PROMPT = """你是严格且一致的助教，正在评估学生期末项目的功能表现。

## 必选功能检查（重要！）

本项目有 **5 个必选功能**，这是作业的基本要求：

| 必选功能 | 如何从输出判断 | 缺失后果 |
|---------|---------------|---------|
| LLM 集成 | 输出中有 AI 生成的内容（分析、建议、总结等） | **必选！** llm_integration=0，core_feature_works最高2分 |
| 外部数据交互 | 有文件读写操作，或调用了其他 API | 影响核心功能评分 |
| 数据处理逻辑 | 输出经过了处理/转换，不是简单透传 | 影响核心功能评分 |
| 用户交互 | 有 CLI 参数或 Web 界面 | 影响用户体验评分 |
| 错误处理 | 无效输入不会导致程序崩溃 | 影响错误处理评分 |

**LLM 集成是必选项！** 缺少 LLM 功能意味着项目不符合基本要求。

## 评分核心原则

评分依据是**运行输出的实际价值**，而非"是否执行成功"或"是否有输出"。
- 退出码为 0 但输出无意义 = 未实现功能 = 0 分
- 有输出但是模板提示语 = 未实现功能 = 0 分
- 只有 --help 输出没有实际功能演示 = 未实现功能 = 0 分

## 项目信息
- 项目名称：{project_name}
- 项目描述：{project_description}

**首先判断**：如果项目名称是"你的项目名称"或描述是"一句话描述项目功能"，说明学生未修改模板，所有功能评分应为 0 分。

## 命令运行结果

### 主功能演示
{demo_results}

### 错误处理演示
{error_results}

## 生成的文件
{generated_files}

## 各评分项的判断标准

### 1. 核心功能 (core_feature_works) - 最高 4 分

**重要前提**：如果项目缺少 LLM 集成（必选功能），此项最高只能得 2 分！

**0 分 - 无功能实现：**
- 输出包含"🚧 项目待实现"、"请修改 src/main.py 实现你的功能"等模板提示
- 所有 demo 命令只输出帮助信息（usage/help），没有任何实际功能执行
- 所有命令都报错或超时
- 输出为空或仅有换行

**1 分 - 部分功能但有明显问题：**
- 有少量功能可用，但大部分命令失败
- 输出有明显 bug 或不完整
- 缺少多个必选功能

**2 分 - 主要功能可用但缺少 LLM：**
- 核心功能可以运行，输出基本正确
- 但没有 LLM 集成，或 LLM 功能无效
- **这是缺少 LLM 功能时的最高分**

**3 分 - 功能完整：**
- 多个命令展示了不同功能
- **包含有效的 LLM 集成**
- 输出正确、格式清晰

**4 分 - 表现出色：**
- demo 命令展示了 5 个以上不同功能
- 功能之间有数据流转（如：添加数据 -> 查询 -> LLM分析 -> 导出）
- LLM 功能是核心流程的一部分，不是可有可无的附加功能
- 输出有格式化（如表格、列表、分隔线、状态标识）

### 2. LLM 集成 (llm_integration) - 最高 3 分

**这是必选功能！** 此项为 0 分表示项目不满足基本要求。

**0 分 - 缺失/不合格：**
- 没有任何命令涉及 LLM 调用
- 或 LLM 调用完全失败/超时，没有返回任何结果
- 输出中完全没有 AI 生成内容的痕迹
- **此项为 0 意味着项目不符合必选要求**

**1 分 - LLM 调用但效果差：**
- LLM 返回了内容，但内容与用户输入/数据无关（如通用模板回复）
- 或 LLM 输出过短（少于 20 字）无实际分析价值
- 或 LLM 返回格式错误，无法正常展示

**2 分 - LLM 功能正常：**
- LLM 调用成功，返回了有意义的内容
- 如：情绪分析结果、内容摘要、智能回复等
- LLM 输出与用户数据相关，有一定的分析价值

**3 分 - LLM 与业务深度结合：**
- LLM 输出是基于用户具体数据的个性化分析（如分析用户输入的日记内容、记账数据等）
- 去掉 LLM 功能后，产品核心价值会显著降低
- LLM 输出有实质内容（50字以上），包含具体的分析、建议或总结

### 3. 错误处理 (error_handling) - 最高 3 分

**前提**：如果项目本身未实现（核心功能为 0 分），错误处理也应为 0 分。

**0 分 - 无错误处理：**
- 无效输入导致 Python Traceback（异常未捕获）
- 程序崩溃

**1 分 - 部分错误处理：**
- error_handling 命令中，有 1-2 个仍导致 Python Traceback
- 或有捕获异常但只打印了默认错误信息

**2 分 - 基本错误处理：**
- error_handling 命令中，无 Traceback 崩溃
- 有错误提示，但可能是 argparse 默认提示或简单的 "Error" 信息

**3 分 - 完善的错误处理：**
- error_handling 命令中，全部无 Traceback
- 有自定义的友好错误提示，说明了错误原因和正确用法
- 如："错误：日期格式无效，请使用 YYYY-MM-DD 格式"

### 4. 用户体验 (user_experience) - 最高 2 分

**重要限制**：如果项目缺少 LLM 功能（llm_integration = 0），user_experience 最高只能得 **1 分**。
理由：没有 LLM 集成的产品无法体现完整的产品价值和用户体验。

**0 分 - 体验差：**
- 无帮助信息
- 输出混乱难以理解
- 或项目未实现

**1 分 - 基本可用：**
- 有 --help 帮助信息
- 输出尚可理解
- **这是缺少 LLM 功能时的最高分**

**2 分 - 体验良好：**
- **前提：必须有 LLM 功能（llm_integration > 0）**
- --help 输出包含使用示例（Examples 或示例命令）
- 命令输出使用了格式化元素（如表格、分隔线、缩进、emoji 标识）
- 操作结果有明确的成功/失败状态提示

## 评分量表
<<<RUBRIC>>>

## 评分规则
- **严格根据运行输出的实际价值评分**
- 没有实际功能的项目，所有评分项都应为 0 分
- 每项只能给出 scoring_guide 中定义的整数分值
- 只输出 JSON，不输出任何解释

## 输出格式（严格JSON）
{{
  "total": number,
  "criteria": [
    {{"id": "评分项id", "score": 整数, "reason": "简短评语，引用具体输出内容作为依据"}},
    ...
  ],
  "flags": [],
  "confidence": number(0-1)
}}
"""

CODE_QUALITY_PROMPT = """你是严格且一致的助教，正在评估学生期末项目的代码质量。

## 必选功能代码检查

本项目要求实现以下必选功能，请检查代码中是否包含相关实现：

| 必选功能 | 代码特征 |
|---------|---------|
| LLM 集成 | 有 API 调用代码（如 openai、requests 调用 LLM API、DEEPSEEK_API_KEY 等） |
| 外部数据交互 | 有文件读写代码（open/read/write）或其他 API 调用 |
| 数据处理逻辑 | 有数据处理函数，不只是简单打印或透传 |

**LLM 集成是必选项！** 如果代码中没有 LLM API 调用相关代码，code_structure 最高只能得 1 分。

## 评分核心原则

评分依据是**代码是否实现了真正的业务逻辑**，而非代码文件是否存在或格式是否规范。
- 只有框架代码（argparse + print）没有业务逻辑 = 未实现 = 0 分
- 模板代码未修改 = 未实现 = 0 分
- 没有 LLM 调用代码 = 不满足必选要求 = 结构最高 1 分

## 源代码文件

{source_code}

## 安全检查结果
{security_issues}

## 各评分项的判断标准

### 1. 代码结构 (code_structure) - 最高 2 分

**首先检查必选功能代码**：
- 是否有 LLM API 调用代码（如 openai.ChatCompletion、requests.post 到 API endpoint、使用 DEEPSEEK_API_KEY 等）
- 是否有文件读写或其他数据交互代码
- 是否有实际的数据处理逻辑

**0 分 - 无代码/模板代码：**
- 没有实际的业务逻辑代码
- 只有命令行框架 + `print("🚧 项目待实现")`
- 代码充满 "TODO: 实现你的项目功能" 注释但没有实现
- 所有逻辑堆在一个函数里

**1 分 - 有代码但不完整：**
- 有业务逻辑代码，但都在一个文件
- 函数过长或职责不清
- **或者缺少 LLM 调用代码（不满足必选要求时的最高分）**

**2 分 - 结构清晰：**
- 有多个模块文件，分工明确（如 storage.py, llm.py, main.py）
- **包含 LLM 调用相关的模块或函数**
- 函数职责单一，长度适中
- 模块划分服务于实际功能

### 2. 代码可读性 (code_readability) - 最高 2 分

**前提**：如果没有实际业务代码，可读性为 0 分（没有代码可评价）。

**0 分 - 不可读/无代码：**
- 无实际代码可评价
- 或变量名无意义（如 a, b, x, tmp）
- 无注释，逻辑混乱

**1 分 - 基本可读：**
- 变量名基本可理解
- 有部分注释

**2 分 - 清晰易读：**
- 变量命名规范有意义（如 diary_content, user_input）
- 关键位置有注释说明
- 代码格式统一

### 3. 安全性 (security) - 最高 1 分

**0 分 - 不安全：**
- API Key 硬编码在代码中（如 `api_key = "sk-xxx"`）
- 没有 .env.example 文件
- 没有使用环境变量

**1 分 - 安全：**
- 使用 `os.getenv()` 或 `os.environ` 获取 API Key
- 有 .env.example 示例文件
- 代码中没有泄露密钥

## 评分量表
<<<RUBRIC>>>

## 评分规则
- **严格根据代码的实际业务逻辑评分**
- 模板代码、框架代码、没有功能实现的代码 = 0 分
- 只有真正实现了功能的代码才能评价其结构和可读性
- 每项只能给出 scoring_guide 中定义的整数分值
- 只输出 JSON，不输出任何解释

## 输出格式（严格JSON）
{{
  "total": number,
  "criteria": [
    {{"id": "评分项id", "score": 整数, "reason": "简短评语，引用具体代码特征作为依据"}},
    ...
  ],
  "flags": [],
  "confidence": number(0-1)
}}
"""


def call_llm(prompt: str, api_url: str, api_key: str, model: str) -> dict:
    """调用 LLM API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data, timeout=(10, 120))
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as e:
        print(f"⚠️ LLM 调用失败: {e}", file=sys.stderr)
        return {
            "total": 0,
            "criteria": [],
            "flags": ["llm_error"],
            "confidence": 0
        }


def format_command_results(results: list, category: str) -> str:
    """格式化命令运行结果"""
    filtered = [r for r in results if r.get("category") == category]
    
    if not filtered:
        return "无"
    
    lines = []
    for r in filtered:
        lines.append(f"命令: {r['command']}")
        lines.append(f"描述: {r['description']}")
        lines.append(f"退出码: {r['exit_code']}")
        if r.get("timeout"):
            lines.append("状态: 超时")
        lines.append(f"标准输出:\n{r['stdout'][:2000] if r['stdout'] else '(空)'}")
        if r['stderr']:
            lines.append(f"标准错误:\n{r['stderr'][:1000]}")
        lines.append("-" * 40)
    
    return "\n".join(lines)


def format_source_code(code_files: dict) -> str:
    """格式化源代码"""
    if not code_files:
        return "无源代码文件"
    
    lines = []
    for path, content in code_files.items():
        lines.append(f"=== {path} ===")
        lines.append(content[:8000])
        lines.append("")
    
    return "\n".join(lines)


def format_source_files_summary(code_files: dict) -> str:
    """格式化源代码文件摘要（用于文档一致性检查）"""
    if not code_files:
        return "无源代码文件"
    
    lines = []
    for path, content in code_files.items():
        lines.append(f"### {path}")
        
        # 检测 LLM 相关代码
        has_llm = any(kw in content.lower() for kw in [
            "openai", "deepseek", "api_key", "llm", "chat", "completion",
            "gpt", "claude", "anthropic"
        ])
        if has_llm:
            lines.append("  - ✅ 包含 LLM/API 相关代码")
        
        # 检测文件操作
        has_file_ops = any(kw in content for kw in [
            "open(", "read(", "write(", "json.load", "json.dump",
            "csv.", "pandas", "with open"
        ])
        if has_file_ops:
            lines.append("  - ✅ 包含文件读写操作")
        
        # 提取函数名
        import re
        functions = re.findall(r'def\s+(\w+)\s*\(', content)
        if functions:
            lines.append(f"  - 函数: {', '.join(functions[:10])}")
        
        # 提取类名
        classes = re.findall(r'class\s+(\w+)\s*[:\(]', content)
        if classes:
            lines.append(f"  - 类: {', '.join(classes[:5])}")
    
    return "\n".join(lines)


def format_run_summary(command_results: list) -> str:
    """格式化运行结果摘要（用于文档一致性检查）"""
    if not command_results:
        return "无命令运行结果"
    
    demo_cmds = [r for r in command_results if r.get("category") == "demo"]
    error_cmds = [r for r in command_results if r.get("category") == "error_handling"]
    
    success_count = sum(1 for r in command_results if r.get("exit_code") == 0)
    fail_count = sum(1 for r in command_results if r.get("exit_code") not in (None, 0) and not r.get("timeout"))
    timeout_count = sum(1 for r in command_results if r.get("timeout"))
    traceback_count = sum(1 for r in command_results 
                         if "Traceback" in r.get("stderr", "") or "Traceback" in r.get("stdout", ""))
    
    lines = [
        f"总命令数: {len(command_results)}",
        f"- Demo 命令: {len(demo_cmds)} 个",
        f"- 错误处理测试: {len(error_cmds)} 个",
        f"- 成功: {success_count}, 失败: {fail_count}, 超时: {timeout_count}",
        f"- 出现 Traceback: {traceback_count} 次",
        "",
        "### 各命令执行情况："
    ]
    
    for r in command_results:
        status = "✅" if r.get("exit_code") == 0 else ("⏱️超时" if r.get("timeout") else "❌")
        has_tb = "⚠️Traceback" if ("Traceback" in r.get("stderr", "") or "Traceback" in r.get("stdout", "")) else ""
        lines.append(f"- [{status}] {r.get('description', r.get('command', ''))} {has_tb}")
    
    return "\n".join(lines)


def evaluate_documentation(run_results: dict, rubric: dict, llm_config: dict) -> dict:
    """评估文档"""
    structure = run_results.get("structure_check", {})
    
    readme = structure.get("README.md", {}).get("content", "未提交")
    report = structure.get("REPORT.md", {}).get("content", "未提交")
    changelog = structure.get("CHANGELOG.md", {}).get("content", "未提交")
    
    # 获取源代码文件摘要和运行结果摘要（用于一致性检查）
    source_files_summary = format_source_files_summary(run_results.get("source_code", {}))
    run_summary = format_run_summary(run_results.get("command_results", []))
    
    prompt = DOCUMENTATION_PROMPT.replace(
        "<<<README_CONTENT>>>", readme
    ).replace(
        "<<<REPORT_CONTENT>>>", report
    ).replace(
        "<<<CHANGELOG_CONTENT>>>", changelog
    ).replace(
        "<<<SOURCE_FILES>>>", source_files_summary
    ).replace(
        "<<<RUN_SUMMARY>>>", run_summary
    ).replace(
        "<<<RUBRIC>>>", json.dumps(rubric, ensure_ascii=False, indent=2)
    )
    
    return call_llm(prompt, **llm_config)


def evaluate_functionality(run_results: dict, rubric: dict, llm_config: dict) -> dict:
    """评估功能"""
    manifest = run_results.get("manifest", {})
    project = manifest.get("project", {})
    
    prompt = FUNCTIONALITY_PROMPT.format(
        project_name=project.get("name", "未知"),
        project_description=project.get("description", ""),
        demo_results=format_command_results(run_results.get("command_results", []), "demo"),
        error_results=format_command_results(run_results.get("command_results", []), "error_handling"),
        generated_files=json.dumps(run_results.get("generated_files", []), ensure_ascii=False, indent=2)
    ).replace(
        "<<<RUBRIC>>>", json.dumps(rubric, ensure_ascii=False, indent=2)
    )
    
    return call_llm(prompt, **llm_config)


def evaluate_code_quality(run_results: dict, rubric: dict, llm_config: dict) -> dict:
    """评估代码质量"""
    prompt = CODE_QUALITY_PROMPT.format(
        source_code=format_source_code(run_results.get("source_code", {})),
        security_issues=json.dumps(run_results.get("security_issues", []), ensure_ascii=False)
    ).replace(
        "<<<RUBRIC>>>", json.dumps(rubric, ensure_ascii=False, indent=2)
    )
    
    return call_llm(prompt, **llm_config)


def check_llm_in_code(source_code: dict) -> bool:
    """检测源代码中是否有 LLM API 调用"""
    if not source_code:
        return False
    
    llm_keywords = [
        # API 调用相关
        "openai", "deepseek", "anthropic", "claude",
        "chatcompletion", "chat.completions",
        # API Key 相关
        "api_key", "apikey", "deepseek_api_key", "openai_api_key",
        # 常见的 LLM 调用模式
        "llm", "gpt", "chat", "completion",
        # requests 调用 LLM API
        "api.deepseek.com", "api.openai.com",
    ]
    
    all_code = "\n".join(source_code.values()).lower()
    
    for keyword in llm_keywords:
        if keyword in all_code:
            return True
    
    return False


def post_process_grade(grade: dict, rubric: dict, dimension: str = None, run_results: dict = None) -> dict:
    """后处理评分结果，确保分数在有效范围内，并应用硬性限制"""
    criteria = grade.get("criteria", [])
    rubric_criteria = {c["id"]: c for c in rubric.get("criteria", [])}
    
    # 构建 criteria 的字典以便快速查找
    criteria_dict = {c.get("id"): c for c in criteria}
    
    # ============ 功能维度的硬性限制 ============
    if dimension == "functionality":
        llm_score = criteria_dict.get("llm_integration", {}).get("score", 0)
        
        if llm_score == 0:
            # 缺少 LLM 功能时的分数上限
            caps = {
                "core_feature_works": 2,  # 最高 2 分
                "user_experience": 1,     # 最高 1 分
            }
            
            for c in criteria:
                cid = c.get("id", "")
                if cid in caps:
                    current_score = int(c.get("score", 0))
                    if current_score > caps[cid]:
                        c["score"] = caps[cid]
                        c["reason"] = c.get("reason", "") + f" [因缺少 LLM 功能，分数被限制为 {caps[cid]}]"
    
    # ============ 代码质量维度的硬性限制 ============
    if dimension == "code_quality" and run_results:
        has_llm_code = check_llm_in_code(run_results.get("source_code", {}))
        
        if not has_llm_code:
            for c in criteria:
                if c.get("id") == "code_structure":
                    current_score = int(c.get("score", 0))
                    if current_score > 1:
                        c["score"] = 1
                        c["reason"] = c.get("reason", "") + " [因缺少 LLM 调用代码，分数被限制为 1]"
    
    # ============ 原有的分数范围检查 ============
    total = 0
    for c in criteria:
        cid = c.get("id", "")
        score = int(c.get("score", 0))
        
        # 确保分数不超过最大值
        if cid in rubric_criteria:
            max_score = rubric_criteria[cid].get("max_score", score)
            score = min(score, max_score)
            score = max(score, 0)
        
        c["score"] = score
        total += score
    
    grade["total"] = total
    grade["criteria"] = criteria
    
    # 检查是否需要人工复核
    lo, hi = rubric.get("borderline_band", [None, None])
    if lo is not None and hi is not None:
        if lo <= total <= hi:
            flags = set(grade.get("flags", []))
            flags.add("need_review")
            grade["flags"] = list(flags)
    
    return grade


def main():
    parser = argparse.ArgumentParser(description="期末项目 LLM 评估")
    parser.add_argument("--run-results", required=True, help="run_project.py 的输出 JSON")
    parser.add_argument("--rubric", required=True, help="Rubric JSON 文件")
    parser.add_argument("--dimension", required=True, 
                       choices=["documentation", "functionality", "code_quality"],
                       help="评估维度")
    parser.add_argument("--out", default="grade.json", help="输出 JSON 文件")
    parser.add_argument("--summary", help="输出摘要 Markdown 文件")
    parser.add_argument("--model", default=os.getenv("LLM_MODEL", "deepseek-chat"))
    parser.add_argument("--api-url", default=os.getenv("LLM_API_URL", "https://api.deepseek.com/chat/completions"))
    parser.add_argument("--api-key", default=os.getenv("LLM_API_KEY", ""))
    args = parser.parse_args()
    
    if not args.api_key:
        print("⚠️ LLM_API_KEY 未设置，评分可能失败", file=sys.stderr)
    
    # 加载数据
    with open(args.run_results, "r", encoding="utf-8") as f:
        run_results = json.load(f)
    
    with open(args.rubric, "r", encoding="utf-8") as f:
        rubric = json.load(f)
    
    llm_config = {
        "api_url": args.api_url,
        "api_key": args.api_key,
        "model": args.model
    }
    
    # 执行评估
    print(f"🔍 评估 {args.dimension}...")
    
    if args.dimension == "documentation":
        grade = evaluate_documentation(run_results, rubric, llm_config)
    elif args.dimension == "functionality":
        grade = evaluate_functionality(run_results, rubric, llm_config)
    else:
        grade = evaluate_code_quality(run_results, rubric, llm_config)
    
    # 后处理（应用硬性分数限制）
    grade = post_process_grade(grade, rubric, dimension=args.dimension, run_results=run_results)
    
    # 保存结果
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(grade, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 评分完成: {grade.get('total', 0)}/{rubric.get('max_score', 0)}")
    
    # 生成摘要
    if args.summary:
        lines = [
            f"# {args.dimension} 评分",
            f"- **总分**: {grade.get('total', 0)} / {rubric.get('max_score', 0)}",
            f"- **置信度**: {grade.get('confidence', 0):.2f}",
            f"- **标记**: {', '.join(grade.get('flags', [])) or '无'}",
            "",
            "## 分项评分",
        ]
        for c in grade.get("criteria", []):
            lines.append(f"- **{c.get('id', '')}**: {c.get('score', 0)} 分")
            if c.get("reason"):
                lines.append(f"  - {c.get('reason', '')}")
        
        with open(args.summary, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


if __name__ == "__main__":
    main()

