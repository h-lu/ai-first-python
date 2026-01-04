#!/usr/bin/env python3
"""
生成专业的 PDF 成绩报告

适用于打印归档，包含：
- 封面页（课程信息、学生信息）
- 后端开发反思报告
- 前端开发反思报告  
- 评分详情页
- 防伪水印
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import markdown
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    HAS_PDF_SUPPORT = True
except ImportError:
    HAS_PDF_SUPPORT = False


def load_json(filepath, default=None):
    """安全加载 JSON 文件"""
    if not os.path.exists(filepath):
        return default or {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return default or {}


def read_file(filepath):
    """读取文件内容"""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def fix_image_paths(content, images_dir):
    """修复图片路径为绝对路径"""
    if not images_dir or not os.path.isdir(images_dir):
        return content
    
    abs_images_dir = os.path.abspath(images_dir)
    
    def replace_img(match):
        alt = match.group(1)
        src = match.group(2)
        if not src.startswith(('http://', 'https://', 'file://', '/')):
            abs_src = os.path.join(abs_images_dir, os.path.basename(src))
            if os.path.exists(abs_src):
                return f'![{alt}](file://{abs_src})'
        return match.group(0)
    
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_img, content)
    return content


def markdown_to_html(md_content):
    """将 Markdown 转换为 HTML（仅内容部分）"""
    extensions = ['tables', 'fenced_code', 'nl2br']
    return markdown.markdown(md_content, extensions=extensions)


def generate_watermark_id(student_id, commit_sha):
    """生成唯一的水印标识"""
    raw = f"{student_id}-{commit_sha}-{datetime.now().isoformat()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()


def generate_cover_page(student_id, student_name="", class_name="", 
                       assignment_name="VibeVault 期末大作业"):
    """生成封面页 HTML"""
    current_date = datetime.now().strftime('%Y年%m月%d日')
    current_semester = "2025年秋季学期"
    
    # 如果有学生姓名，直接显示；否则留空供手写
    name_value = student_name if student_name else '&emsp;' * 8
    class_value = class_name if class_name else '&emsp;' * 8
    id_value = student_id if student_id else '&emsp;' * 8
    
    return f'''
    <div class="cover-page">
        <div class="cover-header">
            <div class="university-name">课程大作业报告</div>
        </div>
        
        <div class="cover-title">
            <h1>《Java 程序设计》</h1>
            <h2>期末大作业</h2>
            <h3>{assignment_name}</h3>
        </div>
        
        <div class="cover-info">
            <table class="info-table">
                <tr>
                    <td class="label">学&emsp;&emsp;号：</td>
                    <td class="value underline">{id_value}</td>
                </tr>
                <tr>
                    <td class="label">姓&emsp;&emsp;名：</td>
                    <td class="value underline">{name_value}</td>
                </tr>
                <tr>
                    <td class="label">班&emsp;&emsp;级：</td>
                    <td class="value underline">{class_value}</td>
                </tr>
                <tr>
                    <td class="label">提交日期：</td>
                    <td class="value underline">{current_date}</td>
                </tr>
            </table>
        </div>
        
        <div class="cover-footer">
            <p>{current_semester}</p>
        </div>
    </div>
    '''


def generate_report_section(title, content, icon="📝"):
    """生成报告章节 HTML"""
    if not content or content.strip() in ['', '*（未提交）*']:
        html_content = '<p class="empty-notice">（未提交）</p>'
    else:
        html_content = markdown_to_html(content)
    
    return f'''
    <div class="report-section">
        <h1 class="section-title">{icon} {title}</h1>
        <div class="section-content">
            {html_content}
        </div>
    </div>
    '''


def generate_grade_page(final_grade):
    """生成评分详情页 HTML"""
    total = final_grade.get("total_score", 0)
    max_score = final_grade.get("max_score", 100)
    breakdown = final_grade.get("breakdown", {})
    
    # 编程测试详情
    prog = breakdown.get("programming", {})
    prog_rows = ""
    if prog.get("groups"):
        for group_name, group_info in prog["groups"].items():
            prog_rows += f'''
            <tr>
                <td>{group_name}</td>
                <td>{group_info.get('passed', 0)} / {group_info.get('total', 0)}</td>
                <td>{group_info.get('score', 0):.1f}</td>
                <td>{group_info.get('max_score', 0)}</td>
            </tr>
            '''
    
    # LLM 评分详情
    def format_llm_details(section_data):
        criteria = section_data.get("criteria", [])
        if not criteria:
            return f'<p class="no-detail">无详细评分</p>'
        
        rows = ""
        for c in criteria:
            reason = c.get("reason", "").replace("<", "&lt;").replace(">", "&gt;")
            rows += f'''
            <tr>
                <td>{c.get('id', '')}</td>
                <td class="score-cell">{c.get('score', 0)}</td>
                <td class="reason-cell">{reason}</td>
            </tr>
            '''
        
        confidence = section_data.get("confidence")
        flags = section_data.get("flags", [])
        footer = ""
        if confidence:
            footer += f'<span class="confidence">置信度: {confidence:.2f}</span>'
        if flags:
            footer += f'<span class="flags">标记: {", ".join(flags)}</span>'
        
        return f'''
        <table class="detail-table">
            <thead>
                <tr><th>评分项</th><th>得分</th><th>评语</th></tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        <div class="detail-footer">{footer}</div>
        '''
    
    report = breakdown.get("report", {})
    frontend = breakdown.get("frontend", {})
    
    return f'''
    <div class="grade-page">
        <h1 class="page-title">📊 评分详情</h1>
        
        <div class="total-score">
            <div class="score-circle">
                <span class="score-value">{total:.1f}</span>
                <span class="score-max">/ {max_score}</span>
            </div>
            <div class="score-label">总分</div>
        </div>
        
        <div class="grade-summary">
            <h2>成绩汇总</h2>
            <table class="summary-table">
                <thead>
                    <tr><th>项目</th><th>得分</th><th>满分</th><th>占比</th></tr>
                </thead>
                <tbody>
                    <tr>
                        <td>编程测试</td>
                        <td class="score-cell">{prog.get('score', 0):.1f}</td>
                        <td>{prog.get('max_score', 80)}</td>
                        <td>{prog.get('max_score', 80)}%</td>
                    </tr>
                    <tr>
                        <td>后端反思报告</td>
                        <td class="score-cell">{report.get('score', 0):.1f}</td>
                        <td>{report.get('max_score', 10)}</td>
                        <td>{report.get('max_score', 10)}%</td>
                    </tr>
                    <tr>
                        <td>前端反思报告</td>
                        <td class="score-cell">{frontend.get('score', 0):.1f}</td>
                        <td>{frontend.get('max_score', 10)}</td>
                        <td>{frontend.get('max_score', 10)}%</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="grade-details">
            <h2>编程测试详情</h2>
            <table class="detail-table">
                <thead>
                    <tr><th>测试组</th><th>通过数</th><th>得分</th><th>满分</th></tr>
                </thead>
                <tbody>{prog_rows or '<tr><td colspan="4">无测试数据</td></tr>'}</tbody>
            </table>
        </div>
        
        <div class="grade-details">
            <h2>后端反思报告评分</h2>
            {format_llm_details(report)}
        </div>
        
        <div class="grade-details">
            <h2>前端反思报告评分</h2>
            {format_llm_details(frontend)}
        </div>
        
        <div class="grade-footer">
            <p>报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>本报告由自动评分系统生成</p>
        </div>
    </div>
    '''


def get_css_styles(watermark_text="", commit_sha=""):
    """获取 PDF 样式，包含水印和版本标记"""
    
    # 水印样式
    watermark_css = ""
    if watermark_text:
        watermark_css = f'''
    /* 水印 */
    body::after {{
        content: "{watermark_text}";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        font-size: 60pt;
        color: rgba(200, 200, 200, 0.15);
        white-space: nowrap;
        pointer-events: none;
        z-index: 9999;
    }}
    
    .report-section::before,
    .grade-page::before {{
        content: "{watermark_text}";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        font-size: 48pt;
        color: rgba(200, 200, 200, 0.12);
        white-space: nowrap;
        pointer-events: none;
        z-index: -1;
    }}
    '''
    
    # 版本标记（右上角）
    commit_marker = ""
    if commit_sha:
        short_sha = commit_sha[:7] if len(commit_sha) > 7 else commit_sha
        commit_marker = f'''
        @top-right {{
            content: "{short_sha}";
            font-size: 8pt;
            color: #999;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
    '''
    
    return f'''
    @page {{
        size: A4;
        margin: 2cm 2.5cm;
        {commit_marker}
        @bottom-center {{
            content: counter(page);
            font-size: 10pt;
            color: #666;
        }}
    }}
    
    @page cover {{
        margin: 0;
        @bottom-center {{ content: none; }}
    }}
    
    @font-face {{
        font-family: 'Noto Sans CJK SC';
        src: local('Noto Sans CJK SC'), local('Noto Sans SC'), 
             local('Source Han Sans SC'), local('Source Han Sans CN'),
             local('PingFang SC'), local('Microsoft YaHei'),
             local('SimHei'), local('WenQuanYi Micro Hei');
    }}
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        font-family: 'Noto Sans CJK SC', 'Source Han Sans SC', 'PingFang SC', 
                     'Microsoft YaHei', 'SimHei', 'WenQuanYi Micro Hei', sans-serif;
        font-size: 11pt;
        line-height: 1.8;
        color: #333;
    }}
    
    {watermark_css}
    
    /* 封面页样式 */
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
    
    .cover-header {{
        margin-bottom: 4cm;
    }}
    
    .university-name {{
        font-size: 18pt;
        color: #1a5490;
        letter-spacing: 0.5em;
        font-weight: bold;
    }}
    
    .cover-title h1 {{
        font-size: 26pt;
        color: #1a5490;
        margin-bottom: 0.5cm;
        font-weight: bold;
    }}
    
    .cover-title h2 {{
        font-size: 20pt;
        color: #333;
        margin-bottom: 0.3cm;
        font-weight: normal;
    }}
    
    .cover-title h3 {{
        font-size: 14pt;
        color: #666;
        font-weight: normal;
    }}
    
    .cover-info {{
        margin-top: 3cm;
    }}
    
    .info-table {{
        margin: 0 auto;
        border-collapse: collapse;
    }}
    
    .info-table td {{
        padding: 0.4cm 0.5cm;
        font-size: 12pt;
    }}
    
    .info-table .label {{
        text-align: right;
        color: #333;
    }}
    
    .info-table .value {{
        text-align: left;
        min-width: 6cm;
    }}
    
    .info-table .underline {{
        border-bottom: 1px solid #333;
    }}
    
    .cover-footer {{
        margin-top: 4cm;
        color: #666;
        font-size: 11pt;
    }}
    
    /* 报告章节样式 */
    .report-section {{
        page-break-before: always;
        position: relative;
    }}
    
    .section-title {{
        font-size: 18pt;
        color: #1a5490;
        border-bottom: 2px solid #1a5490;
        padding-bottom: 0.3cm;
        margin-bottom: 0.8cm;
    }}
    
    .section-content {{
        text-align: justify;
    }}
    
    .section-content h1 {{
        font-size: 16pt;
        color: #1a5490;
        margin: 1cm 0 0.5cm 0;
    }}
    
    .section-content h2 {{
        font-size: 14pt;
        color: #333;
        margin: 0.8cm 0 0.4cm 0;
    }}
    
    .section-content h3 {{
        font-size: 12pt;
        color: #555;
        margin: 0.6cm 0 0.3cm 0;
    }}
    
    .section-content p {{
        margin: 0.4cm 0;
        text-indent: 2em;
    }}
    
    .section-content ul, .section-content ol {{
        margin: 0.4cm 0 0.4cm 1.5cm;
    }}
    
    .section-content li {{
        margin: 0.2cm 0;
    }}
    
    .section-content img {{
        max-width: 100%;
        height: auto;
        margin: 0.5cm auto;
        display: block;
        border: 1px solid #ddd;
    }}
    
    .section-content code {{
        font-family: 'Consolas', 'Monaco', monospace;
        background: #f5f5f5;
        padding: 0.1cm 0.2cm;
        border-radius: 3px;
        font-size: 10pt;
    }}
    
    .section-content pre {{
        background: #f5f5f5;
        padding: 0.5cm;
        border-radius: 5px;
        overflow-x: auto;
        font-size: 9pt;
        margin: 0.5cm 0;
    }}
    
    .section-content blockquote {{
        border-left: 4px solid #1a5490;
        padding-left: 0.5cm;
        margin: 0.5cm 0;
        color: #555;
        background: #f9f9f9;
        padding: 0.3cm 0.5cm;
    }}
    
    .section-content table {{
        width: 100%;
        border-collapse: collapse;
        margin: 0.5cm 0;
        font-size: 10pt;
    }}
    
    .section-content th, .section-content td {{
        border: 1px solid #ddd;
        padding: 0.3cm;
        text-align: left;
    }}
    
    .section-content th {{
        background: #1a5490;
        color: white;
    }}
    
    .section-content tr:nth-child(even) {{
        background: #f9f9f9;
    }}
    
    .empty-notice {{
        color: #999;
        font-style: italic;
        text-align: center;
        padding: 2cm;
    }}
    
    /* 评分页样式 */
    .grade-page {{
        page-break-before: always;
        position: relative;
    }}
    
    .page-title {{
        font-size: 18pt;
        color: #1a5490;
        text-align: center;
        margin-bottom: 1cm;
    }}
    
    .total-score {{
        text-align: center;
        margin: 1cm 0;
    }}
    
    .score-circle {{
        display: inline-block;
        width: 4cm;
        height: 4cm;
        border: 4px solid #1a5490;
        border-radius: 50%;
        line-height: 4cm;
        text-align: center;
    }}
    
    .score-value {{
        font-size: 28pt;
        font-weight: bold;
        color: #1a5490;
    }}
    
    .score-max {{
        font-size: 14pt;
        color: #666;
    }}
    
    .score-label {{
        font-size: 12pt;
        color: #666;
        margin-top: 0.3cm;
    }}
    
    .grade-summary, .grade-details {{
        margin: 0.8cm 0;
    }}
    
    .grade-summary h2, .grade-details h2 {{
        font-size: 14pt;
        color: #333;
        border-bottom: 1px solid #ddd;
        padding-bottom: 0.2cm;
        margin-bottom: 0.4cm;
    }}
    
    .summary-table, .detail-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 10pt;
    }}
    
    .summary-table th, .summary-table td,
    .detail-table th, .detail-table td {{
        border: 1px solid #ddd;
        padding: 0.25cm 0.4cm;
        text-align: left;
    }}
    
    .summary-table th, .detail-table th {{
        background: #1a5490;
        color: white;
        font-weight: normal;
    }}
    
    .summary-table tr:nth-child(even),
    .detail-table tr:nth-child(even) {{
        background: #f9f9f9;
    }}
    
    .score-cell {{
        text-align: center;
        font-weight: bold;
        color: #1a5490;
    }}
    
    .reason-cell {{
        font-size: 9pt;
        color: #555;
        max-width: 10cm;
    }}
    
    .detail-footer {{
        font-size: 9pt;
        color: #666;
        margin-top: 0.2cm;
    }}
    
    .detail-footer .confidence {{
        margin-right: 1cm;
    }}
    
    .detail-footer .flags {{
        color: #c00;
    }}
    
    .no-detail {{
        color: #999;
        font-style: italic;
        padding: 0.5cm;
        text-align: center;
    }}
    
    .grade-footer {{
        margin-top: 1cm;
        padding-top: 0.5cm;
        border-top: 1px solid #ddd;
        font-size: 9pt;
        color: #999;
        text-align: center;
    }}
    
    .grade-footer p {{
        margin: 0.1cm 0;
        text-indent: 0;
    }}
    '''


def create_full_html(args, final_grade, student_info):
    """创建完整的 HTML 文档"""
    
    # 读取报告内容
    report_content = read_file(args.report)
    frontend_content = read_file(args.frontend)
    
    # 修复图片路径
    frontend_content = fix_image_paths(frontend_content, args.images)
    
    # 移除报告中的标题行（避免重复）
    report_content = re.sub(r'^#\s*后端开发反思报告.*\n', '', report_content, flags=re.MULTILINE)
    frontend_content = re.sub(r'^#\s*前端开发反思报告.*\n', '', frontend_content, flags=re.MULTILINE)
    
    # 提取学生信息
    student_id = student_info.get("student_id", "")
    student_name = student_info.get("name", "")
    class_name = student_info.get("class_name", "")
    commit_sha = student_info.get("commit_sha", "")
    
    # 生成水印文本
    watermark_text = ""
    if student_id:
        watermark_id = generate_watermark_id(student_id, commit_sha)
        watermark_text = f"{student_id} · {watermark_id}"
    
    # 构建 HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Java程序设计 - 期末大作业报告</title>
    <style>{get_css_styles(watermark_text, commit_sha)}</style>
</head>
<body>
    {generate_cover_page(student_id, student_name, class_name)}
    {generate_report_section("后端开发反思报告", report_content)}
    {generate_report_section("前端开发反思报告", frontend_content, "🎨")}
    {generate_grade_page(final_grade)}
</body>
</html>'''
    
    return html


def convert_to_pdf(html_content, pdf_file, images_dir=None):
    """使用 weasyprint 生成 PDF"""
    if not HAS_PDF_SUPPORT:
        print("weasyprint not available", file=sys.stderr)
        return False
    
    try:
        font_config = FontConfiguration()
        base_url = os.path.abspath(images_dir) if images_dir else os.getcwd()
        
        HTML(string=html_content, base_url=base_url).write_pdf(
            pdf_file,
            font_config=font_config
        )
        return True
    except Exception as e:
        print(f"PDF generation error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate professional PDF grade report")
    parser.add_argument("--report", default="REPORT.md", help="REPORT.md file path")
    parser.add_argument("--frontend", default="FRONTEND.md", help="FRONTEND.md file path")
    parser.add_argument("--grade", default="final_grade.json", help="Final grade JSON file")
    parser.add_argument("--images", default="images", help="Images directory")
    parser.add_argument("--out", default="grade_report.pdf", help="Output PDF file")
    parser.add_argument("--student-id", default="", help="Student ID")
    parser.add_argument("--student-name", default="", help="Student name")
    parser.add_argument("--class-name", default="", help="Class name")
    parser.add_argument("--commit-sha", default="", help="Commit SHA for watermark")
    args = parser.parse_args()
    
    # 从环境变量获取学生信息
    student_id = args.student_id or os.getenv("STUDENT_ID", "")
    student_name = args.student_name or os.getenv("STUDENT_NAME", "")
    class_name = args.class_name or os.getenv("CLASS_NAME", "")
    commit_sha = args.commit_sha or os.getenv("COMMIT_SHA", "")
    
    # 从仓库名提取学生 ID
    if not student_id:
        repo = os.getenv("REPO", "")
        match = re.search(r'-stu[_-]?st?(\d+)$', repo)
        if match:
            student_id = match.group(1)
        else:
            match = re.search(r'-stu[_-]([a-zA-Z0-9_]+)$', repo)
            if match:
                student_id = match.group(1)
    
    student_info = {
        "student_id": student_id,
        "name": student_name,
        "class_name": class_name,
        "commit_sha": commit_sha
    }
    
    # 加载成绩
    final_grade = load_json(args.grade, {"total_score": 0, "max_score": 100, "breakdown": {}})
    
    # 创建 HTML
    html_content = create_full_html(args, final_grade, student_info)
    
    # 保存 HTML（调试用）
    html_out = args.out.replace(".pdf", ".html")
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # 生成 PDF
    if HAS_PDF_SUPPORT:
        if convert_to_pdf(html_content, args.out, args.images):
            print(f"✅ PDF report generated: {args.out}")
            return 0
        else:
            print(f"⚠️ PDF generation failed", file=sys.stderr)
            return 1
    else:
        print(f"ℹ️ weasyprint not installed, HTML saved: {html_out}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
