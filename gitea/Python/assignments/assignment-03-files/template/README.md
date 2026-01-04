# 作业 3：文件批量处理工具

## 任务
- 在 `src/file_tool.py` 中完成 `FileTool` 类：实现文件列出、筛选、批量重命名、按类型整理、统计等功能。
- 处理各种边界情况：隐藏文件、无扩展名文件、重命名冲突、权限错误等。
- 通过公开测试与隐藏测试；提交 `REPORT.md` 反思报告。

⚠️ **安全提示**：本作业涉及文件操作，请始终在测试目录中操作，先用 `dry_run` 模式预览。

## 环境与依赖
- Python 3.11+
- 安装依赖：`pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple`

## 本地运行
```bash
python -m pytest -v
```

## 提交要求
- 提交信息需包含关键字"完成作业"以触发评分。
- 确保 `REPORT.md` 已填写。

## 评分构成（总分 20）
- Core 测试：10 分
- Edge 测试：5 分
- REPORT.md：5 分

