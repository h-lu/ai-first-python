#!/usr/bin/env python3
"""
期末项目自动运行器
根据 manifest.yaml 运行学生项目，捕获所有输出供 LLM 评估
"""

import yaml
import subprocess
import os
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

# 预先加载 .env 并兼容旧变量名
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

if not os.getenv("DEEPSEEK_API_KEY"):
    llm_key = os.getenv("LLM_API_KEY")
    if llm_key:
        os.environ["DEEPSEEK_API_KEY"] = llm_key


class ProjectRunner:
    """项目运行器"""
    
    def __init__(self, project_dir: str, timeout: int = 60):
        """
        初始化运行器
        
        Args:
            project_dir: 项目目录
            timeout: 命令超时时间（秒）
        """
        self.project_dir = Path(project_dir).resolve()
        self.timeout = timeout
        self.results = {
            "project_dir": str(self.project_dir),
            "timestamp": datetime.now().isoformat(),
            "manifest": None,
            "structure_check": {},
            "command_results": [],
            "generated_files": [],
            "security_issues": [],
            "source_code": {},
            "errors": []
        }
    
    def load_manifest(self) -> dict:
        """加载 manifest.yaml"""
        manifest_path = self.project_dir / "manifest.yaml"
        if not manifest_path.exists():
            self.results["errors"].append("缺少 manifest.yaml 文件")
            return {}
        
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = yaml.safe_load(f)
            self.results["manifest"] = manifest
            return manifest
        except Exception as e:
            self.results["errors"].append(f"manifest.yaml 解析失败: {e}")
            return {}
    
    def check_structure(self) -> dict:
        """检查项目结构"""
        required_files = [
            "README.md",
            "REPORT.md",
            "CHANGELOG.md",
            "requirements.txt",
            "manifest.yaml",
        ]
        
        optional_files = [
            "src/main.py",
            "app.py",
            ".env.example",
        ]
        
        structure = {}
        
        # 检查必需文件
        for f in required_files:
            path = self.project_dir / f
            structure[f] = {
                "exists": path.exists(),
                "required": True,
                "size": path.stat().st_size if path.exists() else 0
            }
            # 读取文档内容
            if path.exists() and f.endswith(".md"):
                try:
                    content = path.read_text(encoding="utf-8")
                    structure[f]["content"] = content[:15000]  # 限制长度
                except Exception as e:
                    structure[f]["content"] = f"读取失败: {e}"
        
        # 检查可选文件
        for f in optional_files:
            path = self.project_dir / f
            structure[f] = {
                "exists": path.exists(),
                "required": False,
                "size": path.stat().st_size if path.exists() else 0
            }
        
        self.results["structure_check"] = structure
        return structure
    
    def setup_environment(self, manifest: dict):
        """设置运行环境"""
        req_path = self.project_dir / "requirements.txt"
        if req_path.exists():
            print("📦 安装项目依赖...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(req_path), "-q"],
                    cwd=self.project_dir,
                    timeout=120,
                    capture_output=True
                )
            except Exception as e:
                self.results["errors"].append(f"依赖安装失败: {e}")
        
        # 检查环境变量
        env_vars = manifest.get("env_vars", [])
        missing_vars = []
        for var in env_vars:
            if var not in os.environ:
                missing_vars.append(var)
        
        if missing_vars:
            self.results["errors"].append(f"缺少环境变量: {', '.join(missing_vars)}")
    
    def run_command(self, cmd: str, description: str, category: str) -> dict:
        """
        运行单个命令
        
        Args:
            cmd: 命令字符串
            description: 命令描述
            category: 命令类别（demo/error_handling）
        
        Returns:
            运行结果
        """
        result = {
            "command": cmd,
            "description": description,
            "category": category,
            "stdout": "",
            "stderr": "",
            "exit_code": None,
            "timeout": False,
            "duration": 0
        }
        
        print(f"  ▶ {description}: {cmd}")
        
        start_time = datetime.now()
        try:
            proc = subprocess.run(
                cmd,
                shell=True,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONPATH": str(self.project_dir)}
            )
            result["stdout"] = proc.stdout[:10000]  # 限制长度
            result["stderr"] = proc.stderr[:5000]
            result["exit_code"] = proc.returncode
        except subprocess.TimeoutExpired:
            result["timeout"] = True
            result["stderr"] = f"命令超时 ({self.timeout}s)"
            print(f"    ⏱️ 超时")
        except Exception as e:
            result["stderr"] = str(e)
            result["exit_code"] = -1
            print(f"    ❌ 错误: {e}")
        
        result["duration"] = (datetime.now() - start_time).total_seconds()
        
        if result["exit_code"] == 0:
            print(f"    ✅ 成功 ({result['duration']:.1f}s)")
        elif not result["timeout"]:
            print(f"    ⚠️ 退出码: {result['exit_code']}")
        
        return result
    
    def run_all_commands(self, manifest: dict):
        """运行所有 manifest 中定义的命令"""
        commands = manifest.get("commands", {})
        
        # 运行 demo 命令
        demo_commands = commands.get("demo", [])
        if demo_commands:
            print("\n📺 运行功能演示命令...")
            for cmd_info in demo_commands:
                result = self.run_command(
                    cmd_info.get("command", ""),
                    cmd_info.get("description", ""),
                    "demo"
                )
                self.results["command_results"].append(result)
        
        # 运行 error_handling 命令
        error_commands = commands.get("error_handling", [])
        if error_commands:
            print("\n🛡️ 运行错误处理测试...")
            for cmd_info in error_commands:
                result = self.run_command(
                    cmd_info.get("command", ""),
                    cmd_info.get("description", ""),
                    "error_handling"
                )
                self.results["command_results"].append(result)
    
    def collect_generated_files(self):
        """收集生成的文件"""
        output_dirs = ["output", "data", "reports", "results"]
        
        for dir_name in output_dirs:
            dir_path = self.project_dir / dir_name
            if dir_path.exists():
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        file_info = {
                            "path": str(file_path.relative_to(self.project_dir)),
                            "size": file_path.stat().st_size,
                        }
                        # 文本文件读取内容
                        if file_path.suffix in [".txt", ".md", ".json", ".csv", ".log"]:
                            try:
                                file_info["content"] = file_path.read_text(encoding="utf-8")[:5000]
                            except Exception:
                                pass
                        self.results["generated_files"].append(file_info)
    
    def check_security(self):
        """安全检查：API Key 不硬编码"""
        issues = []
        
        # 检查所有 Python 文件
        for py_file in self.project_dir.rglob("*.py"):
            # 跳过虚拟环境
            if "venv" in str(py_file) or ".venv" in str(py_file):
                continue
            
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                
                # 检查硬编码的 API Key
                if "sk-" in content and "sk-your" not in content.lower():
                    issues.append(f"疑似硬编码 API Key: {py_file.name}")
                
                # 检查直接赋值的 api_key
                if 'api_key = "' in content.lower() or "api_key = '" in content.lower():
                    if "os.getenv" not in content and "os.environ" not in content:
                        issues.append(f"API Key 可能未使用环境变量: {py_file.name}")
                        
            except Exception:
                pass
        
        # 检查 .env.example 是否存在
        env_example = self.project_dir / ".env.example"
        if not env_example.exists():
            issues.append("缺少 .env.example 文件")
        
        self.results["security_issues"] = issues
    
    def read_source_code(self):
        """读取源代码"""
        code_files = {}
        
        # 读取 src 目录
        src_dir = self.project_dir / "src"
        if src_dir.exists():
            for py_file in src_dir.rglob("*.py"):
                if "venv" in str(py_file) or "__pycache__" in str(py_file):
                    continue
                rel_path = str(py_file.relative_to(self.project_dir))
                try:
                    code_files[rel_path] = py_file.read_text(encoding="utf-8")[:15000]
                except Exception:
                    pass
        
        # 读取根目录的关键文件
        for name in ["app.py", "main.py"]:
            f = self.project_dir / name
            if f.exists():
                try:
                    code_files[name] = f.read_text(encoding="utf-8")[:15000]
                except Exception:
                    pass
        
        self.results["source_code"] = code_files
    
    def run(self) -> dict:
        """执行完整的运行流程"""
        print(f"🚀 开始运行项目: {self.project_dir}")
        print("=" * 50)
        
        # 1. 加载 manifest
        print("\n📋 加载 manifest.yaml...")
        manifest = self.load_manifest()
        if not manifest:
            print("❌ manifest.yaml 加载失败")
            return self.results
        
        project_info = manifest.get("project", {})
        print(f"   项目名称: {project_info.get('name', '未知')}")
        print(f"   项目描述: {project_info.get('description', '无')}")
        
        # 2. 检查结构
        print("\n📁 检查项目结构...")
        self.check_structure()
        
        # 3. 设置环境
        self.setup_environment(manifest)
        
        # 4. 运行命令
        self.run_all_commands(manifest)
        
        # 5. 收集生成文件
        print("\n📦 收集生成文件...")
        self.collect_generated_files()
        
        # 6. 安全检查
        print("\n🔒 安全检查...")
        self.check_security()
        if self.results["security_issues"]:
            for issue in self.results["security_issues"]:
                print(f"   ⚠️ {issue}")
        else:
            print("   ✅ 未发现安全问题")
        
        # 7. 读取源代码
        print("\n📝 读取源代码...")
        self.read_source_code()
        print(f"   读取了 {len(self.results['source_code'])} 个文件")
        
        print("\n" + "=" * 50)
        print("✅ 项目运行完成")
        
        return self.results


def main():
    parser = argparse.ArgumentParser(description="期末项目自动运行器")
    parser.add_argument("project_dir", help="学生项目目录")
    parser.add_argument("--out", default="run_results.json", help="输出 JSON 文件")
    parser.add_argument("--timeout", type=int, default=60, help="命令超时时间（秒）")
    args = parser.parse_args()
    
    runner = ProjectRunner(args.project_dir, args.timeout)
    results = runner.run()
    
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 结果保存至: {args.out}")
    
    # 返回状态码
    if results["errors"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

