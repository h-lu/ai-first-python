#!/usr/bin/env python3
"""
按分组计算编程题得分（pytest JUnit XML）

- core 组满分 10
- edge 组满分 5
- 总分为各组得分之和（满分 15）
"""

import argparse
import xml.etree.ElementTree as ET
import json
import os
import re
import sys
from glob import glob


def parse_junit_files(junit_dir):
    """解析目录下所有 JUnit XML 报告"""
    results = []
    xml_files = glob(os.path.join(junit_dir, "TEST-*.xml")) or glob(
        os.path.join(junit_dir, "*.xml")
    )

    for xml_file in xml_files:
        try:
            root = ET.parse(xml_file).getroot()
            for testsuite in root.iter("testsuite"):
                for testcase in testsuite.iter("testcase"):
                    classname = testcase.get("classname", "")
                    name = testcase.get("name", "")
                    # 注意：Element 没有子元素时 bool 值为 False，所以用 find() is not None
                    failed = testcase.find("failure") is not None or testcase.find("error") is not None
                    skipped = testcase.find("skipped") is not None
                    results.append(
                        {
                            "classname": classname,
                            "name": name,
                            "passed": not failed and not skipped,
                            "skipped": skipped,
                        }
                    )
        except Exception as e:
            print(f"Error parsing {xml_file}: {e}", file=sys.stderr)
    return results


def load_groups_config(groups_file):
    """加载测试分组配置"""
    if not os.path.exists(groups_file):
        return {
            "groups": {
                "core": {"pattern": "core", "max_score": 10},
                "edge": {"pattern": "edge", "max_score": 5},
            },
            "fallback_group": "core",
        }

    with open(groups_file, "r", encoding="utf-8") as f:
        return json.load(f)


def categorize_test(classname, groups_config):
    """根据 classname 将测试分类到对应的组"""
    for group_name, group_info in groups_config.get("groups", {}).items():
        pattern = group_info.get("pattern", "")
        if re.search(pattern, classname, re.IGNORECASE):
            return group_name
    return groups_config.get("fallback_group", "core")


def calculate_grouped_score(test_results, groups_config):
    """按分组计算得分"""
    groups = groups_config.get("groups", {})
    group_stats = {}

    for group_name, group_info in groups.items():
        group_stats[group_name] = {
            "passed": 0,
            "total": 0,
            "max_score": group_info.get("max_score", 0),
            "tests": [],
        }

    for test in test_results:
        group = categorize_test(test["classname"], groups_config)
        if group not in group_stats:
            group = groups_config.get("fallback_group", "core")

        group_stats[group]["total"] += 1
        if test["passed"]:
            group_stats[group]["passed"] += 1
        else:
            group_stats[group]["tests"].append(f"{test['classname']}.{test['name']}")

    total_score = 0
    total_max = 0
    group_scores = {}

    for group_name, stats in group_stats.items():
        total_max += stats["max_score"]
        if stats["total"] > 0:
            pass_rate = stats["passed"] / stats["total"]
            group_score = pass_rate * stats["max_score"]
        else:
            group_score = 0

        group_scores[group_name] = {
            "passed": stats["passed"],
            "total": stats["total"],
            "max_score": stats["max_score"],
            "score": round(group_score, 2),
            "failed_tests": stats["tests"][:10],
        }
        total_score += group_score

    return {
        "total_score": round(total_score, 2),
        "max_score": total_max,
        "groups": group_scores,
    }


def main():
    parser = argparse.ArgumentParser(description="Grade programming assignments with test groups")
    parser.add_argument("--junit-dir", required=True, help="Directory containing JUnit XML files")
    parser.add_argument("--groups", default="test_groups.json", help="Test groups configuration file")
    parser.add_argument("--out", default="grade.json", help="Output JSON file")
    parser.add_argument("--summary", default="summary.md", help="Output summary markdown file")
    args = parser.parse_args()

    test_results = parse_junit_files(args.junit_dir)

    if not test_results:
        print("Warning: No test results found", file=sys.stderr)
        grade_data = {
            "total_score": 0,
            "max_score": 0,
            "groups": {},
            "error": "No test results found",
        }
    else:
        groups_config = load_groups_config(args.groups)
        
        # Debug: 显示测试分类
        print(f"📝 Found {len(test_results)} tests:")
        for test in test_results:
            group = categorize_test(test["classname"], groups_config)
            status = "✅" if test["passed"] else "❌"
            print(f"  {status} [{group}] {test['classname']}.{test['name']}")
        
        grade_data = calculate_grouped_score(test_results, groups_config)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(grade_data, f, ensure_ascii=False, indent=2)

    with open(args.summary, "w", encoding="utf-8") as f:
        f.write("# 编程测试成绩报告\n\n")
        f.write(f"**总分：{grade_data['total_score']:.2f} / {grade_data['max_score']}**\n\n")
        f.write("## 分组得分\n\n")
        f.write("| 分组 | 通过 | 总数 | 得分 | 满分 |\n")
        f.write("|------|------|------|------|------|\n")
        for group_name, group_info in grade_data.get("groups", {}).items():
            f.write(
                f"| {group_name} | {group_info['passed']} | {group_info['total']} | "
                f"{group_info['score']:.2f} | {group_info['max_score']} |\n"
            )

        all_failed = []
        for group_info in grade_data.get("groups", {}).values():
            all_failed.extend(group_info.get("failed_tests", []))
        if all_failed:
            f.write("\n## 未通过的测试\n\n")
            for test in all_failed[:20]:
                f.write(f"- {test}\n")
            if len(all_failed) > 20:
                f.write(f"\n... 还有 {len(all_failed) - 20} 个未通过的测试\n")

    print(f"Grading complete: {grade_data['total_score']:.2f}/{grade_data['max_score']}")


if __name__ == "__main__":
    main()

