#!/usr/bin/env python3
"""
创建期末项目成绩元数据文件

从 final_grade.json 和 run_results.json 生成 metadata.json
包含三维度评分：文档、功能、代码质量
以及运行统计信息
"""

import json
import os
import sys
import re
from datetime import datetime


def extract_student_id():
    """从环境变量或仓库名中提取学生 ID"""
    student_id = os.getenv("STUDENT_ID")
    if student_id:
        return student_id
    
    repo = os.getenv("REPO", "")
    if repo:
        match = re.search(r'-stu[_-]([a-zA-Z0-9_]+)$', repo)
        if match:
            return match.group(1)
        match = re.search(r'stu[_-]([a-zA-Z0-9_]+)', repo)
        if match:
            return match.group(1)
    
    return None


def extract_assignment_id():
    """从环境变量或仓库名中提取作业 ID"""
    assignment_id = os.getenv("ASSIGNMENT_ID")
    if assignment_id:
        return assignment_id
    
    repo = os.getenv("REPO", "")
    if repo:
        repo_name = repo.split("/")[-1] if "/" in repo else repo
        assignment = re.sub(r'-stu[_-][a-zA-Z0-9_]+$', '', repo_name)
        assignment = re.sub(r'-template$', '', assignment)
        if assignment:
            return assignment
    
    return "assignment-05-final-project"


def load_run_results(run_results_file='run_results.json'):
    """加载运行结果文件"""
    if not os.path.exists(run_results_file):
        return None
    try:
        with open(run_results_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def extract_run_summary(run_results):
    """从运行结果中提取统计摘要"""
    if not run_results:
        return None
    
    command_results = run_results.get("command_results", [])
    
    # 统计命令执行情况
    demo_commands = [c for c in command_results if c.get("category") == "demo"]
    error_commands = [c for c in command_results if c.get("category") == "error_handling"]
    
    success_count = sum(1 for c in command_results if c.get("exit_code") == 0)
    fail_count = sum(1 for c in command_results if c.get("exit_code") not in (None, 0) and not c.get("timeout"))
    timeout_count = sum(1 for c in command_results if c.get("timeout"))
    
    # 检查是否有 Traceback
    traceback_count = sum(1 for c in command_results 
                         if "Traceback" in c.get("stderr", "") or "Traceback" in c.get("stdout", ""))
    
    return {
        "total_commands": len(command_results),
        "demo_commands": len(demo_commands),
        "error_handling_commands": len(error_commands),
        "success_count": success_count,
        "fail_count": fail_count,
        "timeout_count": timeout_count,
        "traceback_count": traceback_count
    }


def extract_command_outputs(run_results, max_preview=500):
    """提取每个命令的输出摘要"""
    if not run_results:
        return []
    
    outputs = []
    for cmd in run_results.get("command_results", []):
        stdout = cmd.get("stdout", "")
        stderr = cmd.get("stderr", "")
        
        output_info = {
            "command": cmd.get("command", ""),
            "description": cmd.get("description", ""),
            "category": cmd.get("category", ""),
            "exit_code": cmd.get("exit_code"),
            "timeout": cmd.get("timeout", False),
            "duration": cmd.get("duration", 0),
            "stdout_preview": stdout[:max_preview] + ("..." if len(stdout) > max_preview else ""),
            "stderr_preview": stderr[:max_preview] + ("..." if len(stderr) > max_preview else "") if stderr else "",
            "has_traceback": "Traceback" in stderr or "Traceback" in stdout,
            "stdout_lines": len(stdout.splitlines()) if stdout else 0
        }
        outputs.append(output_info)
    
    return outputs


def extract_project_info(run_results):
    """提取项目基本信息"""
    if not run_results:
        return None
    
    manifest = run_results.get("manifest", {})
    if not manifest:
        return None
    
    project = manifest.get("project", {})
    return {
        "name": project.get("name", ""),
        "description": project.get("description", ""),
        "interface": project.get("interface", ""),
        "is_template": project.get("name", "").startswith("你的") or "待实现" in project.get("description", "")
    }


def extract_file_stats(run_results):
    """提取文件统计信息"""
    if not run_results:
        return None
    
    source_code = run_results.get("source_code", {})
    generated_files = run_results.get("generated_files", [])
    security_issues = run_results.get("security_issues", [])
    structure = run_results.get("structure_check", {})
    
    # 检查关键文件是否存在
    has_env_example = structure.get(".env.example", {}).get("exists", False)
    
    return {
        "source_file_count": len(source_code),
        "source_files": list(source_code.keys()),
        "generated_file_count": len(generated_files),
        "security_issues": security_issues,
        "has_env_example": has_env_example
    }


def create_final_metadata(final_grade_file='final_grade.json', run_results_file='run_results.json'):
    """从 final_grade.json 和 run_results.json 创建元数据（期末项目专用）"""
    try:
        with open(final_grade_file, 'r', encoding='utf-8') as f:
            final_data = json.load(f)
        
        # 加载运行结果
        run_results = load_run_results(run_results_file)
        
        assignment_id = extract_assignment_id()
        student_id = extract_student_id()
        
        total_score = final_data.get("total_score", 0)
        max_score = final_data.get("max_score", 25)
        breakdown = final_data.get("breakdown", {})
        flags = final_data.get("flags", [])
        confidence = final_data.get("confidence", 1.0)
        
        components = []
        
        # 文档质量部分
        doc = breakdown.get("documentation", {})
        if doc:
            doc_component = {
                "type": "llm_documentation",
                "score": doc.get("score", 0),
                "max_score": doc.get("max_score", 8),
                "details": {
                    "criteria": doc.get("criteria", [])
                }
            }
            components.append(doc_component)
        
        # 功能表现部分
        func = breakdown.get("functionality", {})
        if func:
            func_component = {
                "type": "llm_functionality",
                "score": func.get("score", 0),
                "max_score": func.get("max_score", 12),
                "details": {
                    "criteria": func.get("criteria", [])
                }
            }
            components.append(func_component)
        
        # 代码质量部分
        code = breakdown.get("code_quality", {})
        if code:
            code_component = {
                "type": "llm_code_quality",
                "score": code.get("score", 0),
                "max_score": code.get("max_score", 5),
                "details": {
                    "criteria": code.get("criteria", [])
                }
            }
            components.append(code_component)
        
        metadata = {
            "version": "1.1",
            "assignment": assignment_id,
            "student_id": student_id,
            "components": components,
            "total_score": round(total_score, 2),
            "total_max_score": max_score,
            "flags": flags,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "generator": "gitea-autograde-final-project"
        }
        
        # 添加运行统计信息
        if run_results:
            # 项目基本信息
            project_info = extract_project_info(run_results)
            if project_info:
                metadata["project_info"] = project_info
            
            # 运行摘要统计
            run_summary = extract_run_summary(run_results)
            if run_summary:
                metadata["run_summary"] = run_summary
            
            # 每个命令的输出详情
            command_outputs = extract_command_outputs(run_results)
            if command_outputs:
                metadata["command_outputs"] = command_outputs
            
            # 文件统计
            file_stats = extract_file_stats(run_results)
            if file_stats:
                metadata["file_stats"] = file_stats
            
            # 错误信息
            if run_results.get("errors"):
                metadata["run_errors"] = run_results["errors"]
        
        return metadata
    except Exception as e:
        print(f"Error creating final metadata: {e}", file=sys.stderr)
        return {}


def main():
    """主函数"""
    grade_type = os.getenv("GRADE_TYPE", "final").lower()
    grade_file = os.getenv("GRADE_FILE", "final_grade.json")
    
    if os.path.exists(grade_file):
        metadata = create_final_metadata(grade_file)
    else:
        print(f"Error: {grade_file} not found", file=sys.stderr)
        metadata = {}
    
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

