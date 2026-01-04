"""
LLM 功能模块
提供基于大语言模型的智能功能
"""

from __future__ import annotations

import os
from typing import Optional, List, Dict
from openai import OpenAI


class LLMFeatures:
    """LLM 智能功能"""
    
    def __init__(self):
        """初始化 LLM 客户端"""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("请设置 DEEPSEEK_API_KEY 环境变量")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = "deepseek-chat"
    
    def _call_llm(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> Optional[str]:
        """
        调用 LLM API
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            max_tokens: 最大输出 token 数
        
        Returns:
            LLM 响应文本
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ LLM 调用失败: {e}")
            return None
    
    def analyze_mood(self, content: str) -> Optional[str]:
        """
        分析日记情绪
        
        Args:
            content: 日记内容
        
        Returns:
            情绪标签（开心/平静/难过/焦虑/愤怒）
        """
        system_prompt = """你是一个情绪分析专家。分析用户日记的整体情绪，只返回一个情绪标签。
        
可选的情绪标签：开心、平静、难过、焦虑、愤怒

只返回情绪标签，不要返回其他内容。"""
        
        user_prompt = f"请分析以下日记的情绪：\n\n{content}"
        
        result = self._call_llm(system_prompt, user_prompt, max_tokens=20)
        
        # 验证返回的是有效情绪
        valid_moods = ["开心", "平静", "难过", "焦虑", "愤怒"]
        if result and result in valid_moods:
            return result
        
        # 尝试从返回中提取有效情绪
        if result:
            for mood in valid_moods:
                if mood in result:
                    return mood
        
        return "平静"  # 默认返回
    
    def get_mood_analysis(self, content: str) -> Optional[str]:
        """
        获取详细的情绪分析
        
        Args:
            content: 日记内容
        
        Returns:
            详细分析文本
        """
        system_prompt = """你是一个温暖的心理分析师。请分析用户日记中的情绪，给出：
1. 主要情绪及其可能的原因
2. 一句温暖的回应或建议

请用简洁友好的语气，控制在 100 字以内。"""
        
        user_prompt = f"请分析以下日记：\n\n{content}"
        
        return self._call_llm(system_prompt, user_prompt, max_tokens=200)
    
    def generate_monthly_summary(self, diaries: List[Dict]) -> Optional[str]:
        """
        生成月度总结
        
        Args:
            diaries: 当月的日记列表
        
        Returns:
            月度总结文本
        """
        if not diaries:
            return None
        
        # 准备日记内容
        diary_texts = []
        for d in diaries:
            mood_str = f"[情绪: {d['mood']}]" if d.get("mood") else ""
            diary_texts.append(f"{d['date']} {mood_str}\n{d['content']}")
        
        all_diaries = "\n\n---\n\n".join(diary_texts)
        
        system_prompt = """你是一个善于总结的助手。请根据用户这个月的所有日记，生成一份温暖的月度总结。

总结应包含：
1. 📊 本月概况（记录天数、主要情绪分布）
2. ✨ 本月亮点（值得记住的好事）
3. 💪 成长与收获
4. 🌟 下月期望（一句鼓励的话）

请用友好的语气，总结控制在 300 字以内。"""
        
        user_prompt = f"以下是我这个月的日记，请帮我总结：\n\n{all_diaries}"
        
        return self._call_llm(system_prompt, user_prompt, max_tokens=600)
    
    def get_writing_suggestion(self, content: str) -> Optional[str]:
        """
        获取写作建议
        
        Args:
            content: 日记内容
        
        Returns:
            写作建议文本
        """
        system_prompt = """你是一个写作教练。请为用户的日记提供简短的写作建议，帮助他们更好地记录生活。

建议方向：
- 可以补充的细节（感官、对话、想法）
- 表达方式的优化
- 值得深入思考的点

请给出 2-3 条具体、可操作的建议，语气友好鼓励，总共不超过 150 字。"""
        
        user_prompt = f"请为以下日记提供写作建议：\n\n{content}"
        
        return self._call_llm(system_prompt, user_prompt, max_tokens=300)
    
    def generate_prompt(self, topic: Optional[str] = None) -> Optional[str]:
        """
        生成写作提示
        
        Args:
            topic: 可选的主题
        
        Returns:
            写作提示
        """
        system_prompt = """你是一个日记写作引导者。请生成一个有趣的日记写作提示，帮助用户开始写作。

提示应该：
- 具体且易于回答
- 能引发思考或回忆
- 积极正面

只返回一个提示问题，不超过 50 字。"""
        
        if topic:
            user_prompt = f"请生成一个关于「{topic}」的日记写作提示"
        else:
            user_prompt = "请生成一个今日日记写作提示"
        
        return self._call_llm(system_prompt, user_prompt, max_tokens=100)

