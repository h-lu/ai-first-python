#!/usr/bin/env python3
"""
汇总期末项目三维度评分
文档 (8分) + 功能 (12分) + 代码质量 (5分) = 25分
"""

import argparse
import json
import os
import sys


def load_json(filepath, default=None):
    """加载 JSON 文件"""
    if not os.path.exists(filepath):
        return default or {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return default or {}


def main():
    parser = argparse.ArgumentParser(description="汇总期末项目评分")
    parser.add_argument("--documentation", required=True, help="文档评分 JSON")
    parser.add_argument("--functionality", required=True, help="功能评分 JSON")
    parser.add_argument("--code-quality", required=True, help="代码质量评分 JSON")
    parser.add_argument("--out", default="final_grade.json", help="输出 JSON 文件")
    parser.add_argument("--summary", default="final_summary.md", help="输出摘要 Markdown")
    args = parser.parse_args()
    
    # 加载各维度评分
    doc_grade = load_json(args.documentation, {"total": 0})
    func_grade = load_json(args.functionality, {"total": 0})
    code_grade = load_json(args.code_quality, {"total": 0})
    
    # 计算总分
    doc_score = doc_grade.get("total", 0)
    func_score = func_grade.get("total", 0)
    code_score = code_grade.get("total", 0)
    
    total_score = doc_score + func_score + code_score
    total_max = 25
    
    # 合并标记
    all_flags = set()
    all_flags.update(doc_grade.get("flags", []))
    all_flags.update(func_grade.get("flags", []))
    all_flags.update(code_grade.get("flags", []))
    
    # 置信度取最低
    min_confidence = min(
        doc_grade.get("confidence", 1),
        func_grade.get("confidence", 1),
        code_grade.get("confidence", 1)
    )
    
    if min_confidence < 0.7:
        all_flags.add("need_review")
    
    # 构建最终成绩
    final_grade = {
        "total_score": round(total_score, 2),
        "max_score": total_max,
        "breakdown": {
            "documentation": {
                "score": round(doc_score, 2),
                "max_score": 8,
                "criteria": doc_grade.get("criteria", []),
            },
            "functionality": {
                "score": round(func_score, 2),
                "max_score": 12,
                "criteria": func_grade.get("criteria", []),
            },
            "code_quality": {
                "score": round(code_score, 2),
                "max_score": 5,
                "criteria": code_grade.get("criteria", []),
            },
        },
        "flags": sorted(list(all_flags)),
        "confidence": min_confidence,
    }
    
    # 保存结果
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(final_grade, f, ensure_ascii=False, indent=2)
    
    # 生成摘要报告
    with open(args.summary, "w", encoding="utf-8") as f:
        f.write("# 期末项目成绩报告\n\n")
        f.write(f"## 总分：{total_score:.2f} / {total_max}\n\n")
        
        f.write("## 分项成绩\n\n")
        f.write("| 维度 | 得分 | 满分 | 说明 |\n")
        f.write("|------|------|------|------|\n")
        f.write(f"| 📄 文档质量 | {doc_score:.2f} | 8 | REPORT.md + CHANGELOG.md |\n")
        f.write(f"| ⚡ 功能表现 | {func_score:.2f} | 12 | 核心功能 + LLM 集成 + 错误处理 |\n")
        f.write(f"| 🔧 代码质量 | {code_score:.2f} | 5 | 结构 + 可读性 + 安全性 |\n")
        
        # 详细评分
        f.write("\n## 详细评分\n")
        
        for dimension, name in [("documentation", "📄 文档质量"), 
                                 ("functionality", "⚡ 功能表现"),
                                 ("code_quality", "🔧 代码质量")]:
            f.write(f"\n### {name}\n\n")
            criteria = final_grade["breakdown"][dimension].get("criteria", [])
            for c in criteria:
                f.write(f"- **{c.get('id', '')}**: {c.get('score', 0)} 分\n")
                if c.get("reason"):
                    f.write(f"  - {c.get('reason', '')}\n")
        
        # 标记
        if all_flags:
            f.write("\n## 标记\n\n")
            for flag in sorted(all_flags):
                f.write(f"- {flag}\n")
    
    print(f"✅ 最终成绩: {total_score:.2f}/{total_max}")
    print(f"📄 结果保存至: {args.out}")
    print(f"📝 摘要保存至: {args.summary}")


if __name__ == "__main__":
    main()

