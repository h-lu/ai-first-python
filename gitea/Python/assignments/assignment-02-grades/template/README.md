# 作业 2：成绩统计分析器

## 任务
- 在 `src/grade_analyzer.py` 中完成 `GradeAnalyzer` 类：实现从 CSV 读取、统计分析、生成报告的功能。
- 处理真实数据中的边界情况，如缺失值、无效分数、重复学号、文件编码问题等。
- 通过公开测试与隐藏测试；提交 `REPORT.md` 反思报告。

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
