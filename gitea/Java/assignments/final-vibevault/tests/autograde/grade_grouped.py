#!/usr/bin/env python3
"""
分组编程题评分脚本

解析 JUnit XML 报告，按测试分组（Core/Advanced/Challenge）计算加权分数
"""

import argparse
import xml.etree.ElementTree as ET
import json
import os
import re
import sys
from pathlib import Path
from glob import glob


def parse_junit_files(junit_dir):
    """
    解析目录下所有 JUnit XML 报告
    
    Returns
    -------
    results : list of dict
        每个测试的结果，包含 classname, name, passed
    """
    results = []
    
    xml_files = glob(os.path.join(junit_dir, "TEST-*.xml"))
    if not xml_files:
        xml_files = glob(os.path.join(junit_dir, "*.xml"))
    
    for xml_file in xml_files:
        try:
            root = ET.parse(xml_file).getroot()
            
            for testsuite in root.iter("testsuite"):
                for testcase in testsuite.iter("testcase"):
                    classname = testcase.get("classname", "")
                    name = testcase.get("name", "")
                    
                    # 检查是否有 failure、error 或 skipped 子元素
                    failed = any(testcase.iter("failure")) or any(testcase.iter("error"))
                    skipped = any(testcase.iter("skipped"))
                    
                    results.append({
                        "classname": classname,
                        "name": name,
                        "passed": not failed and not skipped,
                        "skipped": skipped
                    })
        except Exception as e:
            print(f"Error parsing {xml_file}: {e}", file=sys.stderr)
    
    return results


def load_groups_config(groups_file):
    """加载测试分组配置"""
    if not os.path.exists(groups_file):
        # 默认配置
        return {
            "groups": {
                "core": {"pattern": ".*core.*", "weight": 0.75, "max_score": 60},
                "advanced": {"pattern": ".*advanced.*", "weight": 0.125, "max_score": 10},
                "challenge": {"pattern": ".*challenge.*", "weight": 0.125, "max_score": 10}
            },
            "fallback_group": "core"
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
    """
    按分组计算加权分数
    
    Returns
    -------
    dict
        包含各组得分和总分的字典
    """
    groups = groups_config.get("groups", {})
    
    # 初始化各组统计
    group_stats = {}
    for group_name, group_info in groups.items():
        group_stats[group_name] = {
            "passed": 0,
            "total": 0,
            "max_score": group_info.get("max_score", 10),
            "weight": group_info.get("weight", 0.1),
            "tests": []
        }
    
    # 分类并统计测试结果
    for test in test_results:
        group = categorize_test(test["classname"], groups_config)
        if group not in group_stats:
            group = groups_config.get("fallback_group", "core")
        
        group_stats[group]["total"] += 1
        if test["passed"]:
            group_stats[group]["passed"] += 1
        else:
            group_stats[group]["tests"].append(f"{test['classname']}.{test['name']}")
    
    # 计算各组得分
    total_score = 0
    group_scores = {}
    
    for group_name, stats in group_stats.items():
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
            "failed_tests": stats["tests"][:10]  # 只保留前 10 个失败测试
        }
        
        total_score += group_score
    
    return {
        "total_score": round(total_score, 2),
        "max_score": 80,  # 编程测试总分 80 分（Core 60 + Advanced 10 + Challenge 10）
        "groups": group_scores
    }


def main():
    parser = argparse.ArgumentParser(description="Grade programming assignments with test groups")
    parser.add_argument("--junit-dir", required=True, help="Directory containing JUnit XML files")
    parser.add_argument("--groups", default="test_groups.json", help="Test groups configuration file")
    parser.add_argument("--out", default="grade.json", help="Output JSON file")
    parser.add_argument("--summary", default="summary.md", help="Output summary markdown file")
    args = parser.parse_args()
    
    # 解析测试结果
    test_results = parse_junit_files(args.junit_dir)
    
    if not test_results:
        print("Warning: No test results found", file=sys.stderr)
        grade_data = {
            "total_score": 0,
            "max_score": 80,
            "groups": {},
            "error": "No test results found"
        }
    else:
        # 加载分组配置
        groups_config = load_groups_config(args.groups)
        
        # 计算分组分数
        grade_data = calculate_grouped_score(test_results, groups_config)
    
    # 保存 grade.json
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(grade_data, f, ensure_ascii=False, indent=2)
    
    # 生成 summary.md
    with open(args.summary, "w", encoding="utf-8") as f:
        f.write("# 编程测试成绩报告\n\n")
        f.write(f"**总分：{grade_data['total_score']:.2f} / {grade_data['max_score']}**\n\n")
        
        f.write("## 分组得分\n\n")
        f.write("| 分组 | 通过 | 总数 | 得分 | 满分 |\n")
        f.write("|------|------|------|------|------|\n")
        
        for group_name, group_info in grade_data.get("groups", {}).items():
            f.write(f"| {group_name} | {group_info['passed']} | {group_info['total']} | "
                    f"{group_info['score']:.2f} | {group_info['max_score']} |\n")
        
        # 列出失败的测试
        all_failed = []
        for group_name, group_info in grade_data.get("groups", {}).items():
            all_failed.extend(group_info.get("failed_tests", []))
        
        if all_failed:
            f.write("\n## 未通过的测试\n\n")
            for test in all_failed[:20]:  # 最多显示 20 个
                f.write(f"- {test}\n")
            if len(all_failed) > 20:
                f.write(f"\n... 还有 {len(all_failed) - 20} 个未通过的测试\n")
    
    print(f"Grading complete: {grade_data['total_score']:.2f}/{grade_data['max_score']}")


if __name__ == "__main__":
    main()

