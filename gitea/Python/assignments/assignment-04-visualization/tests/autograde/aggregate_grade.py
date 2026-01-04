#!/usr/bin/env python3
"""
汇总编程测试分数 + REPORT.md 分数
编程测试满分 15（core 10 + edge 5），报告满分 5，总分 20
"""

import argparse
import json
import os
import sys


def load_json(filepath, default=None):
    if not os.path.exists(filepath):
        return default or {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return default or {}


def main():
    parser = argparse.ArgumentParser(description="Aggregate grades for assignment-02-grades")
    parser.add_argument("--programming", required=True, help="Programming test grade JSON")
    parser.add_argument("--report", required=True, help="REPORT.md LLM grade JSON")
    parser.add_argument("--out", default="final_grade.json", help="Output JSON file")
    parser.add_argument("--summary", default="final_summary.md", help="Output summary markdown")
    args = parser.parse_args()

    prog_grade = load_json(args.programming, {"total_score": 0, "max_score": 15})
    report_grade = load_json(args.report, {"total": 0})

    prog_score = prog_grade.get("total_score", 0)
    prog_max = prog_grade.get("max_score", 15)
    report_score = report_grade.get("total", 0)
    report_max = 5

    total_score = prog_score + report_score
    total_max = prog_max + report_max

    final_grade = {
        "total_score": round(total_score, 2),
        "max_score": total_max,
        "breakdown": {
            "programming": {
                "score": round(prog_score, 2),
                "max_score": prog_max,
                "groups": prog_grade.get("groups", {}),
            },
            "report": {
                "score": round(report_score, 2),
                "max_score": report_max,
                "flags": report_grade.get("flags", []),
                "confidence": report_grade.get("confidence"),
                "criteria": report_grade.get("criteria", []),
            },
        },
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(final_grade, f, ensure_ascii=False, indent=2)

    with open(args.summary, "w", encoding="utf-8") as f:
        f.write("# 作业 2 成绩报告\n\n")
        f.write(f"## 总分：{total_score:.2f} / {total_max}\n\n")
        f.write("## 分项成绩\n\n")
        f.write("| 项目 | 得分 | 满分 | 备注 |\n")
        f.write("|------|------|------|------|\n")
        f.write(f"| 编程测试 | {prog_score:.2f} | {prog_max} | core + edge |\n")
        f.write(f"| REPORT.md | {report_score:.2f} | {report_max} | 反思报告 |\n")

        if prog_grade.get("groups"):
            f.write("\n### 编程测试详情\n\n")
            f.write("| 分组 | 通过 | 总数 | 得分 | 满分 |\n")
            f.write("|------|------|------|------|------|\n")
            for group_name, group_info in prog_grade["groups"].items():
                f.write(
                    f"| {group_name} | {group_info.get('passed', 0)} | "
                    f"{group_info.get('total', 0)} | {group_info.get('score', 0):.2f} | "
                    f"{group_info.get('max_score', 0)} |\n"
                )

        all_flags = report_grade.get("flags", [])
        if all_flags:
            f.write("\n### 标记\n\n")
            for flag in set(all_flags):
                f.write(f"- {flag}\n")

    print(f"Final grade: {total_score:.2f}/{total_max}")


if __name__ == "__main__":
    main()

