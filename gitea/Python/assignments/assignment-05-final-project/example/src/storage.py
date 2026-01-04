"""
存储管理模块
负责日记数据的持久化存储
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict


class DiaryStorage:
    """日记存储管理器"""
    
    def __init__(self, data_dir: str = "data"):
        """
        初始化存储管理器
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.diary_file = self.data_dir / "diaries.json"
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """确保数据文件存在"""
        if not self.diary_file.exists():
            self._save_data([])
    
    def _load_data(self) -> List[Dict]:
        """加载所有日记数据"""
        try:
            with open(self.diary_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Dict]):
        """保存日记数据"""
        with open(self.diary_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_diary(self, content: str, date: Optional[str] = None, tags: Optional[List[str]] = None) -> dict:
        """
        添加一篇日记
        
        Args:
            content: 日记内容
            date: 日期（格式：YYYY-MM-DD），默认为今天
            tags: 标签列表
        
        Returns:
            新创建的日记记录
        """
        diaries = self._load_data()
        
        # 生成日期
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 生成 ID
        diary_id = len(diaries) + 1
        
        # 创建日记记录
        diary = {
            "id": diary_id,
            "date": date,
            "content": content,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "mood": None,  # 待 LLM 分析
        }
        
        diaries.append(diary)
        self._save_data(diaries)
        
        return diary
    
    def get_diary(self, diary_id: int) -> Optional[dict]:
        """
        根据 ID 获取日记
        
        Args:
            diary_id: 日记 ID
        
        Returns:
            日记记录，不存在则返回 None
        """
        diaries = self._load_data()
        for diary in diaries:
            if diary["id"] == diary_id:
                return diary
        return None
    
    def get_diary_by_date(self, date: str) -> Optional[dict]:
        """
        根据日期获取日记
        
        Args:
            date: 日期（格式：YYYY-MM-DD）
        
        Returns:
            日记记录，不存在则返回 None
        """
        diaries = self._load_data()
        for diary in diaries:
            if diary["date"] == date:
                return diary
        return None
    
    def list_diaries(self, month: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        列出日记
        
        Args:
            month: 筛选月份（格式：YYYY-MM），None 表示不筛选
            limit: 返回数量限制
        
        Returns:
            日记列表（按日期倒序）
        """
        diaries = self._load_data()
        
        # 按月份筛选
        if month:
            diaries = [d for d in diaries if d["date"].startswith(month)]
        
        # 按日期倒序
        diaries.sort(key=lambda x: x["date"], reverse=True)
        
        return diaries[:limit]
    
    def search_diaries(self, keyword: str) -> List[Dict]:
        """
        搜索日记
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的日记列表
        """
        diaries = self._load_data()
        results = []
        
        keyword_lower = keyword.lower()
        for diary in diaries:
            content_lower = diary["content"].lower()
            tags_str = " ".join(diary.get("tags", [])).lower()
            
            if keyword_lower in content_lower or keyword_lower in tags_str:
                results.append(diary)
        
        return results
    
    def update_diary(self, diary_id: int, **updates) -> Optional[dict]:
        """
        更新日记
        
        Args:
            diary_id: 日记 ID
            **updates: 要更新的字段
        
        Returns:
            更新后的日记记录
        """
        diaries = self._load_data()
        
        for i, diary in enumerate(diaries):
            if diary["id"] == diary_id:
                for key, value in updates.items():
                    if key in diary:
                        diary[key] = value
                diary["updated_at"] = datetime.now().isoformat()
                diaries[i] = diary
                self._save_data(diaries)
                return diary
        
        return None
    
    def delete_diary(self, diary_id: int) -> bool:
        """
        删除日记
        
        Args:
            diary_id: 日记 ID
        
        Returns:
            是否删除成功
        """
        diaries = self._load_data()
        original_len = len(diaries)
        
        diaries = [d for d in diaries if d["id"] != diary_id]
        
        if len(diaries) < original_len:
            self._save_data(diaries)
            return True
        
        return False
    
    def get_diaries_for_month(self, month: str) -> List[Dict]:
        """
        获取指定月份的所有日记
        
        Args:
            month: 月份（格式：YYYY-MM）
        
        Returns:
            该月的所有日记
        """
        diaries = self._load_data()
        return [d for d in diaries if d["date"].startswith(month)]
    
    def export_diaries(self, output_path: str, month: Optional[str] = None) -> str:
        """
        导出日记为文本文件
        
        Args:
            output_path: 输出文件路径
            month: 筛选月份
        
        Returns:
            导出文件路径
        """
        diaries = self.list_diaries(month=month, limit=1000)
        
        lines = ["# 日记导出\n"]
        for diary in diaries:
            lines.append(f"\n## {diary['date']}\n")
            if diary.get("tags"):
                lines.append(f"标签: {', '.join(diary['tags'])}\n")
            if diary.get("mood"):
                lines.append(f"情绪: {diary['mood']}\n")
            lines.append(f"\n{diary['content']}\n")
            lines.append("\n---\n")
        
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        return output_path

