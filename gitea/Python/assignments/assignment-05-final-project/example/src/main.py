#!/usr/bin/env python3
"""
智能日记助手 - 命令行入口
记录日记，LLM 情绪分析，月度总结
"""

import argparse
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.diary import DiaryManager
from src.llm_features import LLMFeatures


def cmd_add(args, manager: DiaryManager):
    """添加日记"""
    # 解析标签
    tags = None
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",")]
    
    try:
        diary = manager.add(args.content, args.date, tags)
        print(f"✅ 日记添加成功！")
        print(f"   ID: {diary['id']}")
        print(f"   日期: {diary['date']}")
        
        # 如果启用了自动分析
        if args.analyze:
            llm = LLMFeatures()
            print("\n🔍 正在分析情绪...")
            mood = llm.analyze_mood(diary["content"])
            if mood:
                manager.update_mood(diary["id"], mood)
                print(f"   情绪: {mood}")
    except ValueError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


def cmd_list(args, manager: DiaryManager):
    """列出日记"""
    diaries = manager.list(month=args.month, limit=args.limit)
    print(manager.format_diary_list(diaries))


def cmd_show(args, manager: DiaryManager):
    """显示日记详情"""
    diary = None
    
    if args.id:
        diary = manager.get(args.id)
    elif args.date:
        diary = manager.get_by_date(args.date)
    else:
        print("❌ 请指定 --id 或 --date")
        sys.exit(1)
    
    if diary:
        print(manager.format_diary(diary))
    else:
        print("❌ 未找到指定日记")
        sys.exit(1)


def cmd_search(args, manager: DiaryManager):
    """搜索日记"""
    try:
        results = manager.search(args.keyword)
        print(manager.format_diary_list(results))
    except ValueError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


def cmd_delete(args, manager: DiaryManager):
    """删除日记"""
    if manager.delete(args.id):
        print(f"✅ 日记 {args.id} 已删除")
    else:
        print(f"❌ 未找到日记 {args.id}")
        sys.exit(1)


def cmd_analyze(args, manager: DiaryManager):
    """分析日记情绪"""
    diary = None
    
    if args.id:
        diary = manager.get(args.id)
    elif args.date:
        diary = manager.get_by_date(args.date)
    else:
        # 默认分析最新一篇
        diaries = manager.list(limit=1)
        if diaries:
            diary = diaries[0]
    
    if not diary:
        print("❌ 未找到要分析的日记")
        sys.exit(1)
    
    print(f"🔍 正在分析日记 [{diary['id']}] {diary['date']}...")
    print(f"   内容: {diary['content'][:50]}...")
    print()
    
    llm = LLMFeatures()
    mood = llm.analyze_mood(diary["content"])
    
    if mood:
        manager.update_mood(diary["id"], mood)
        print(f"✅ 情绪分析结果: {mood}")
        
        # 获取详细分析
        analysis = llm.get_mood_analysis(diary["content"])
        if analysis:
            print(f"\n📝 详细分析:\n{analysis}")
    else:
        print("❌ 情绪分析失败")


def cmd_summary(args, manager: DiaryManager):
    """生成月度总结"""
    month = args.month
    if not month:
        month = datetime.now().strftime("%Y-%m")
    
    try:
        diaries = manager.get_month_diaries(month)
    except ValueError as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)
    
    if not diaries:
        print(f"📭 {month} 没有日记记录")
        sys.exit(0)
    
    print(f"📊 正在生成 {month} 月度总结...")
    print(f"   共 {len(diaries)} 篇日记")
    print()
    
    llm = LLMFeatures()
    summary = llm.generate_monthly_summary(diaries)
    
    if summary:
        print("=" * 50)
        print(f"📅 {month} 月度总结")
        print("=" * 50)
        print(summary)
    else:
        print("❌ 生成总结失败")


def cmd_suggest(args, manager: DiaryManager):
    """获取写作建议"""
    diary = None
    
    if args.id:
        diary = manager.get(args.id)
    elif args.date:
        diary = manager.get_by_date(args.date)
    
    if not diary:
        print("❌ 未找到指定日记")
        sys.exit(1)
    
    print(f"💡 正在为日记 [{diary['id']}] 生成写作建议...")
    print()
    
    llm = LLMFeatures()
    suggestion = llm.get_writing_suggestion(diary["content"])
    
    if suggestion:
        print("📝 写作建议:")
        print(suggestion)
    else:
        print("❌ 生成建议失败")


def cmd_export(args, manager: DiaryManager):
    """导出日记"""
    output_path = args.output or f"output/diary_export_{datetime.now().strftime('%Y%m%d')}.md"
    
    try:
        path = manager.export(output_path, args.month)
        print(f"✅ 日记已导出到: {path}")
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="📔 智能日记助手 - 记录生活，AI 分析情绪",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s add --content "今天天气很好，心情不错"
  %(prog)s add --content "学习了 Python" --tags "学习,编程" --analyze
  %(prog)s list --month 2024-12
  %(prog)s show --id 1
  %(prog)s search "心情"
  %(prog)s analyze --date 2024-12-06
  %(prog)s summary --month 2024-12
  %(prog)s suggest --id 1
  %(prog)s export --month 2024-12
        """
    )
    
    parser.add_argument("--data-dir", default="data", help="数据存储目录")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加新日记")
    add_parser.add_argument("--content", "-c", required=True, help="日记内容")
    add_parser.add_argument("--date", "-d", help="日期 (YYYY-MM-DD)，默认今天")
    add_parser.add_argument("--tags", "-t", help="标签，逗号分隔")
    add_parser.add_argument("--analyze", "-a", action="store_true", help="自动分析情绪")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出日记")
    list_parser.add_argument("--month", "-m", help="月份筛选 (YYYY-MM)")
    list_parser.add_argument("--limit", "-l", type=int, default=10, help="显示数量")
    
    # show 命令
    show_parser = subparsers.add_parser("show", help="显示日记详情")
    show_parser.add_argument("--id", "-i", type=int, help="日记 ID")
    show_parser.add_argument("--date", "-d", help="日期 (YYYY-MM-DD)")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索日记")
    search_parser.add_argument("keyword", help="搜索关键词")
    
    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除日记")
    delete_parser.add_argument("--id", "-i", type=int, required=True, help="日记 ID")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析日记情绪 (LLM)")
    analyze_parser.add_argument("--id", "-i", type=int, help="日记 ID")
    analyze_parser.add_argument("--date", "-d", help="日期 (YYYY-MM-DD)")
    
    # summary 命令
    summary_parser = subparsers.add_parser("summary", help="生成月度总结 (LLM)")
    summary_parser.add_argument("--month", "-m", help="月份 (YYYY-MM)，默认当前月")
    
    # suggest 命令
    suggest_parser = subparsers.add_parser("suggest", help="获取写作建议 (LLM)")
    suggest_parser.add_argument("--id", "-i", type=int, help="日记 ID")
    suggest_parser.add_argument("--date", "-d", help="日期 (YYYY-MM-DD)")
    
    # export 命令
    export_parser = subparsers.add_parser("export", help="导出日记")
    export_parser.add_argument("--output", "-o", help="输出文件路径")
    export_parser.add_argument("--month", "-m", help="月份筛选 (YYYY-MM)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # 初始化管理器
    manager = DiaryManager(args.data_dir)
    
    # 执行命令
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "show": cmd_show,
        "search": cmd_search,
        "delete": cmd_delete,
        "analyze": cmd_analyze,
        "summary": cmd_summary,
        "suggest": cmd_suggest,
        "export": cmd_export,
    }
    
    if args.command in commands:
        commands[args.command](args, manager)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

