#!/usr/bin/env python3
"""
生成期末项目 PDF 成绩报告（Python 作业）
包含：封面、文档内容、运行与安全摘要、评分明细、水印
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
import html

try:
    import markdown
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    HAS_PDF_SUPPORT = True
except ImportError:
    HAS_PDF_SUPPORT = False


def load_json(filepath, default=None):
    """安全加载 JSON"""
    if not os.path.exists(filepath):
        return default or {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:  # noqa: broad-except
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return default or {}


def markdown_to_html(md_content):
    """Markdown 转 HTML"""
    if not md_content:
        return ""
    return markdown.markdown(md_content, extensions=["tables", "fenced_code", "nl2br"])


def escape(text, limit=None):
    """HTML 转义并可选截断"""
    if text is None:
        return ""
    safe = html.escape(str(text))
    if limit and len(safe) > limit:
        return safe[: limit - 3] + "..."
    return safe


def load_text_from_results(run_results, filename, fallback_path):
    """优先从 run_results.structure_check 中取文件内容，再退回磁盘"""
    if run_results:
        content = (
            run_results.get("structure_check", {})
            .get(filename, {})
            .get("content")
        )
        if content:
            return content
    if fallback_path and os.path.exists(fallback_path):
        return Path(fallback_path).read_text(encoding="utf-8")
    return ""


def generate_cover_page(student_info, assignment_name="Python 期末项目"):
    """封面页 HTML"""
    current_date = datetime.now().strftime("%Y年%m月%d日")
    name_value = student_info.get("name") or "&emsp;" * 6
    class_value = student_info.get("class_name") or "&emsp;" * 6
    id_value = student_info.get("student_id") or "&emsp;" * 6
    return f"""
    <div class="cover-page">
        <div class="cover-header">
            <div class="university-name">课程大作业报告</div>
        </div>
        <div class="cover-title">
            <h1>《Python 程序设计》</h1>
            <h2>期末项目</h2>
            <h3>{escape(assignment_name)}</h3>
        </div>
        <div class="cover-info">
            <table class="info-table">
                <tr><td class="label">学号：</td><td class="value underline">{id_value}</td></tr>
                <tr><td class="label">姓名：</td><td class="value underline">{name_value}</td></tr>
                <tr><td class="label">班级：</td><td class="value underline">{class_value}</td></tr>
                <tr><td class="label">提交日期：</td><td class="value underline">{current_date}</td></tr>
            </table>
        </div>
        <div class="cover-footer">
            <p>{datetime.now().strftime("%Y年%m月")} | 自动评分报告</p>
        </div>
    </div>
    """


def build_doc_section(title, content, icon="📝"):
    """文档章节"""
    if not content.strip():
        html_content = "<p class='empty-notice'>（未提交或内容为空）</p>"
    else:
        html_content = markdown_to_html(content)
    return f"""
    <div class="report-section">
        <h1 class="section-title">{icon} {escape(title)}</h1>
        <div class="section-content">
            {html_content}
        </div>
    </div>
    """


def build_command_table(run_results):
    """命令运行结果"""
    commands = run_results.get("command_results", []) if run_results else []
    if not commands:
        return "<p class='empty-notice'>（无命令运行数据）</p>"

    rows = []
    for cmd in commands:
        status = "成功" if cmd.get("exit_code") == 0 else ("超时" if cmd.get("timeout") else "失败")
        rows.append(
            f"""
            <tr>
                <td>{escape(cmd.get('category', ''))}</td>
                <td>{escape(cmd.get('description') or cmd.get('command'))}</td>
                <td>{escape(status)}</td>
                <td>{escape(cmd.get('exit_code'))}</td>
                <td><pre>{escape(cmd.get('stdout'), 1200)}</pre></td>
                <td><pre>{escape(cmd.get('stderr'), 800)}</pre></td>
            </tr>
            """
        )
    return f"""
    <table class="detail-table">
        <thead>
            <tr><th>类别</th><th>命令/说明</th><th>状态</th><th>退出码</th><th>标准输出</th><th>标准错误</th></tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
    </table>
    """


def build_generated_files(run_results):
    files = run_results.get("generated_files", []) if run_results else []
    if not files:
        return "<p class='empty-notice'>（无收集到的生成文件）</p>"
    rows = []
    for f in files[:50]:
        rows.append(
            f"<tr><td>{escape(f.get('path',''))}</td><td>{escape(f.get('size',''))}</td><td><pre>{escape(f.get('content',''),400)}</pre></td></tr>"
        )
    return f"""
    <table class="detail-table">
        <thead><tr><th>路径</th><th>大小</th><th>内容片段</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
    </table>
    """


def build_security_section(run_results):
    issues = run_results.get("security_issues", []) if run_results else []
    if not issues:
        return "<p class='ok-text'>未发现安全问题</p>"
    items = "".join(f"<li>{escape(i)}</li>" for i in issues)
    return f"<ul>{items}</ul>"


def build_grade_page(final_grade):
    total = final_grade.get("total_score", 0)
    max_score = final_grade.get("max_score", 25)
    breakdown = final_grade.get("breakdown", {})

    def build_dimension_row(key, title):
        data = breakdown.get(key, {})
        return f"<tr><td>{title}</td><td class='score-cell'>{data.get('score',0):.2f}</td><td>{data.get('max_score',0)}</td></tr>"

    def build_criteria(key):
        data = breakdown.get(key, {})
        criteria = data.get("criteria", []) or []
        if not criteria:
            return "<p class='empty-notice'>无详细评分</p>"
        rows = []
        for c in criteria:
            rows.append(
                f"<tr><td>{escape(c.get('id',''))}</td><td class='score-cell'>{escape(c.get('score',0))}</td><td>{escape(c.get('reason',''))}</td></tr>"
            )
        return f"""
        <table class="detail-table">
            <thead><tr><th>评分项</th><th>得分</th><th>评语</th></tr></thead>
            <tbody>{''.join(rows)}</tbody>
        </table>
        """

    flags = final_grade.get("flags", [])
    flag_html = f"<p class='flags'>标记：{', '.join(flags)}</p>" if flags else ""

    return f"""
    <div class="grade-page">
        <h1 class="page-title">📊 评分详情</h1>
        <div class="total-score">
            <div class="score-circle">
                <span class="score-value">{total:.2f}</span>
                <span class="score-max">/ {max_score}</span>
            </div>
            <div class="score-label">总分</div>
        </div>
        <div class="grade-summary">
            <h2>成绩汇总</h2>
            <table class="summary-table">
                <thead><tr><th>维度</th><th>得分</th><th>满分</th></tr></thead>
                <tbody>
                    {build_dimension_row('documentation','📄 文档')}
                    {build_dimension_row('functionality','⚡ 功能')}
                    {build_dimension_row('code_quality','🔧 代码质量')}
                </tbody>
            </table>
            {flag_html}
        </div>
        <div class="grade-details">
            <h2>📄 文档评分</h2>
            {build_criteria('documentation')}
        </div>
        <div class="grade-details">
            <h2>⚡ 功能评分</h2>
            {build_criteria('functionality')}
        </div>
        <div class="grade-details">
            <h2>🔧 代码质量</h2>
            {build_criteria('code_quality')}
        </div>
        <div class="grade-footer">
            <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>本报告由自动评分系统生成</p>
        </div>
    </div>
    """


def generate_watermark_id(student_id, commit_sha):
    raw = f"{student_id}-{commit_sha}-{datetime.now().isoformat()}"
    return re.sub("[^A-Z0-9]", "", hex(abs(hash(raw)))[2:]).upper()[:16]


def get_css_styles(watermark_text="", commit_sha=""):
    commit_marker = ""
    if commit_sha:
        short = commit_sha[:7]
        commit_marker = f"""
        @top-right {{
            content: "{short}";
            font-size: 8pt;
            color: #999;
            font-family: 'Consolas','Monaco', monospace;
        }}
        """
    watermark_css = ""
    if watermark_text:
        watermark_css = f"""
        body::after {{
            content: "{watermark_text}";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 60pt;
            color: rgba(200,200,200,0.12);
            pointer-events: none;
            z-index: 9999;
            white-space: nowrap;
        }}
        """
    return f"""
    @page {{
        size: A4;
        margin: 2cm 2.2cm;
        {commit_marker}
        @bottom-center {{ content: counter(page); font-size: 10pt; color: #666; }}
    }}
    @page cover {{ margin: 0; @bottom-center {{ content: none; }} }}
    body {{
        font-family: 'Noto Sans CJK SC','Source Han Sans SC','Microsoft YaHei',sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
    }}
    {watermark_css}
    .cover-page {{
        page: cover;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 3cm;
        page-break-after: always;
    }}
    .cover-header {{ margin-bottom: 3cm; }}
    .university-name {{ font-size: 18pt; color: #1a5490; letter-spacing: 0.4em; font-weight: bold; }}
    .cover-title h1 {{ font-size: 24pt; color: #1a5490; margin-bottom: 0.4cm; }}
    .cover-title h2 {{ font-size: 18pt; color: #333; margin-bottom: 0.3cm; }}
    .cover-title h3 {{ font-size: 13pt; color: #666; }}
    .cover-info {{ margin-top: 2.5cm; }}
    .info-table {{ margin: 0 auto; border-collapse: collapse; }}
    .info-table td {{ padding: 0.35cm 0.5cm; font-size: 12pt; }}
    .info-table .label {{ color: #333; text-align: right; }}
    .info-table .value {{ min-width: 6cm; text-align: left; }}
    .underline {{ border-bottom: 1px solid #333; }}
    .cover-footer {{ margin-top: 3cm; color: #666; font-size: 11pt; }}
    .report-section {{ page-break-before: always; position: relative; }}
    .section-title {{ font-size: 17pt; color: #1a5490; border-bottom: 2px solid #1a5490; padding-bottom: 0.3cm; margin-bottom: 0.7cm; }}
    .section-content {{ text-align: justify; }}
    .section-content h1 {{ font-size: 15pt; color: #1a5490; margin: 0.8cm 0 0.4cm; }}
    .section-content h2 {{ font-size: 13pt; color: #333; margin: 0.6cm 0 0.3cm; }}
    .section-content h3 {{ font-size: 12pt; color: #555; margin: 0.4cm 0 0.2cm; }}
    .section-content p {{ margin: 0.35cm 0; text-indent: 2em; }}
    .section-content ul, .section-content ol {{ margin: 0.4cm 0 0.4cm 1.4cm; }}
    .section-content li {{ margin: 0.2cm 0; }}
    .section-content pre {{ background: #f6f6f6; padding: 0.5cm; border-radius: 5px; overflow-x: auto; font-size: 9pt; }}
    .section-content code {{ background: #f2f2f2; padding: 0.1cm 0.2cm; border-radius: 3px; }}
    .section-content table {{ width: 100%; border-collapse: collapse; margin: 0.5cm 0; font-size: 10pt; }}
    .section-content th, .section-content td {{ border: 1px solid #ddd; padding: 0.25cm; text-align: left; }}
    .section-content th {{ background: #1a5490; color: #fff; }}
    .empty-notice {{ color: #999; font-style: italic; text-align: center; padding: 1.2cm; }}
    .ok-text {{ color: #1a5490; }}
    .grade-page {{ page-break-before: always; position: relative; }}
    .page-title {{ font-size: 18pt; color: #1a5490; text-align: center; margin-bottom: 1cm; }}
    .total-score {{ text-align: center; margin: 1cm 0; }}
    .score-circle {{ display: inline-block; width: 4cm; height: 4cm; border: 4px solid #1a5490; border-radius: 50%; line-height: 4cm; text-align: center; }}
    .score-value {{ font-size: 26pt; font-weight: bold; color: #1a5490; }}
    .score-max {{ font-size: 13pt; color: #666; }}
    .score-label {{ font-size: 11pt; color: #666; margin-top: 0.3cm; }}
    .grade-summary, .grade-details {{ margin: 0.8cm 0; }}
    .grade-summary h2, .grade-details h2 {{ font-size: 14pt; color: #333; border-bottom: 1px solid #ddd; padding-bottom: 0.2cm; margin-bottom: 0.4cm; }}
    .summary-table, .detail-table {{ width: 100%; border-collapse: collapse; font-size: 10pt; }}
    .summary-table th, .summary-table td, .detail-table th, .detail-table td {{ border: 1px solid #ddd; padding: 0.25cm 0.35cm; text-align: left; }}
    .summary-table th, .detail-table th {{ background: #1a5490; color: #fff; }}
    .summary-table tr:nth-child(even), .detail-table tr:nth-child(even) {{ background: #f9f9f9; }}
    .score-cell {{ text-align: center; font-weight: bold; color: #1a5490; }}
    .flags {{ color: #c00; margin-top: 0.3cm; }}
    .grade-footer {{ margin-top: 1cm; padding-top: 0.5cm; border-top: 1px solid #ddd; font-size: 9pt; color: #777; text-align: center; }}
    """


def create_full_html(args, run_results, final_grade, student_info):
    readme = load_text_from_results(run_results, "README.md", args.readme)
    report = load_text_from_results(run_results, "REPORT.md", args.report)
    changelog = load_text_from_results(run_results, "CHANGELOG.md", args.changelog)

    student_id = student_info.get("student_id", "")
    commit_sha = student_info.get("commit_sha", "")
    watermark = generate_watermark_id(student_id, commit_sha) if student_id else ""

    html_parts = [
        "<!DOCTYPE html><html lang='zh-CN'><head>",
        "<meta charset='UTF-8'>",
        f"<title>Python 期末项目成绩报告</title>",
        f"<style>{get_css_styles(watermark, commit_sha)}</style>",
        "</head><body>",
        generate_cover_page(student_info),
        build_doc_section("README 概览", readme, "📘"),
        build_doc_section("REPORT 反思报告", report, "📝"),
        build_doc_section("CHANGELOG 版本记录", changelog, "📜"),
        "<div class='report-section'><h1 class='section-title'>🛠️ 命令运行结果</h1>",
        build_command_table(run_results),
        "</div>",
        "<div class='report-section'><h1 class='section-title'>📦 生成的文件</h1>",
        build_generated_files(run_results),
        "</div>",
        "<div class='report-section'><h1 class='section-title'>🔒 安全检查</h1>",
        build_security_section(run_results),
        "</div>",
        build_grade_page(final_grade),
        "</body></html>",
    ]
    return "".join(html_parts)


def convert_to_pdf(html_content, pdf_file, base_dir=None):
    if not HAS_PDF_SUPPORT:
        print("weasyprint not available", file=sys.stderr)
        return False
    try:
        font_config = FontConfiguration()
        base_url = os.path.abspath(base_dir or os.getcwd())
        HTML(string=html_content, base_url=base_url).write_pdf(pdf_file, font_config=font_config)
        return True
    except Exception as e:  # noqa: broad-except
        print(f"PDF generation error: {e}", file=sys.stderr)
        return False


def load_student_info(args):
    info = load_json(".student_info.json", {})
    repo = os.getenv("REPO", "")
    student_id = args.student_id or info.get("student_id") or ""
    if not student_id and repo:
        match = re.search(r"-stu[_-]?st?(\w+)$", repo)
        if match:
            student_id = match.group(1)
    return {
        "student_id": student_id,
        "name": args.student_name or info.get("name", ""),
        "class_name": args.class_name or info.get("class_name", ""),
        "commit_sha": args.commit_sha or os.getenv("COMMIT_SHA", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="生成 PDF 成绩报告（Python 作业）")
    parser.add_argument("--run-results", default="run_results.json", help="run_project 输出 JSON")
    parser.add_argument("--grade", default="final_grade.json", help="最终成绩 JSON")
    parser.add_argument("--report", default="REPORT.md", help="REPORT.md 路径（回退使用）")
    parser.add_argument("--readme", default="README.md", help="README 路径（回退使用）")
    parser.add_argument("--changelog", default="CHANGELOG.md", help="CHANGELOG 路径（回退使用）")
    parser.add_argument("--out", default="grade_report.pdf", help="输出 PDF 文件")
    parser.add_argument("--student-id", default="", help="学生学号")
    parser.add_argument("--student-name", default="", help="学生姓名")
    parser.add_argument("--class-name", default="", help="班级名称")
    parser.add_argument("--commit-sha", default="", help="提交 SHA")
    args = parser.parse_args()

    run_results = load_json(args.run_results, {})
    final_grade = load_json(args.grade, {"total_score": 0, "max_score": 25, "breakdown": {}})
    student_info = load_student_info(args)

    html_content = create_full_html(args, run_results, final_grade, student_info)

    # 保存 HTML 便于调试
    html_out = args.out.replace(".pdf", ".html")
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html_content)

    if HAS_PDF_SUPPORT:
        if convert_to_pdf(html_content, args.out, base_dir=os.getcwd()):
            print(f"✅ PDF report generated: {args.out}")
            return 0
        print("⚠️ PDF 生成失败，保留 HTML", file=sys.stderr)
        return 1
    else:
        print(f"ℹ️ weasyprint 未安装，已生成 HTML: {html_out}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
