"""
日记核心逻辑模块
提供日记管理的业务逻辑
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from .storage import DiaryStorage


class DiaryManager:
    """日记管理器"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初始化日记管理器
        
        Args:
            data_dir: 数据存储目录
        """
        self.storage = DiaryStorage(data_dir)
    
    def add(self, content: str, date: Optional[str] = None, tags: Optional[List[str]] = None) -> dict:
        """
        添加新日记
        
        Args:
            content: 日记内容
            date: 日期（可选）
            tags: 标签（可选）
        
        Returns:
            新创建的日记
        """
        if not content or not content.strip():
            raise ValueError("日记内容不能为空")
        
        # 验证日期格式
        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"日期格式无效: {date}，请使用 YYYY-MM-DD 格式")
        
        return self.storage.add_diary(content.strip(), date, tags)
    
    def get(self, diary_id: int) -> Optional[dict]:
        """
        获取指定日记
        
        Args:
            diary_id: 日记 ID
        
        Returns:
            日记记录
        """
        return self.storage.get_diary(diary_id)
    
    def get_by_date(self, date: str) -> Optional[dict]:
        """
        根据日期获取日记
        
        Args:
            date: 日期
        
        Returns:
            日记记录
        """
        return self.storage.get_diary_by_date(date)
    
    def list(self, month: Optional[str] = None, limit: int = 10) -> List[dict]:
        """
        列出日记
        
        Args:
            month: 月份筛选
            limit: 数量限制
        
        Returns:
            日记列表
        """
        return self.storage.list_diaries(month, limit)
    
    def search(self, keyword: str) -> List[dict]:
        """
        搜索日记
        
        Args:
            keyword: 关键词
        
        Returns:
            匹配的日记列表
        """
        if not keyword or not keyword.strip():
            raise ValueError("搜索关键词不能为空")
        
        return self.storage.search_diaries(keyword.strip())
    
    def delete(self, diary_id: int) -> bool:
        """
        删除日记
        
        Args:
            diary_id: 日记 ID
        
        Returns:
            是否删除成功
        """
        return self.storage.delete_diary(diary_id)
    
    def update_mood(self, diary_id: int, mood: str) -> Optional[dict]:
        """
        更新日记的情绪标签
        
        Args:
            diary_id: 日记 ID
            mood: 情绪标签
        
        Returns:
            更新后的日记
        """
        return self.storage.update_diary(diary_id, mood=mood)
    
    def get_month_diaries(self, month: str) -> List[dict]:
        """
        获取指定月份的所有日记
        
        Args:
            month: 月份（YYYY-MM）
        
        Returns:
            日记列表
        """
        # 验证月份格式
        try:
            datetime.strptime(month + "-01", "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"月份格式无效: {month}，请使用 YYYY-MM 格式")
        
        return self.storage.get_diaries_for_month(month)
    
    def export(self, output_path: str, month: Optional[str] = None) -> str:
        """
        导出日记
        
        Args:
            output_path: 输出路径
            month: 月份筛选
        
        Returns:
            导出文件路径
        """
        return self.storage.export_diaries(output_path, month)
    
    def format_diary(self, diary: dict) -> str:
        """
        格式化日记为可读字符串
        
        Args:
            diary: 日记记录
        
        Returns:
            格式化的字符串
        """
        lines = [
            f"📅 日期: {diary['date']}",
            f"🆔 ID: {diary['id']}",
        ]
        
        if diary.get("tags"):
            lines.append(f"🏷️  标签: {', '.join(diary['tags'])}")
        
        if diary.get("mood"):
            lines.append(f"😊 情绪: {diary['mood']}")
        
        lines.append("")
        lines.append(diary["content"])
        
        return "\n".join(lines)
    
    def format_diary_list(self, diaries: List[dict]) -> str:
        """
        格式化日记列表
        
        Args:
            diaries: 日记列表
        
        Returns:
            格式化的字符串
        """
        if not diaries:
            return "📭 没有找到日记"
        
        lines = [f"📚 找到 {len(diaries)} 篇日记：\n"]
        
        for diary in diaries:
            # 截取内容预览
            preview = diary["content"][:50]
            if len(diary["content"]) > 50:
                preview += "..."
            
            mood_emoji = ""
            if diary.get("mood"):
                mood_map = {
                    "开心": "😊",
                    "平静": "😌",
                    "难过": "😢",
                    "焦虑": "😰",
                    "愤怒": "😠",
                }
                mood_emoji = mood_map.get(diary["mood"], "")
            
            lines.append(f"[{diary['id']}] {diary['date']} {mood_emoji}")
            lines.append(f"    {preview}")
            lines.append("")
        
        return "\n".join(lines)

