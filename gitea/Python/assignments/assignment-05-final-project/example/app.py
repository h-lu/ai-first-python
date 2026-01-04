"""
智能日记助手 - Streamlit Web 界面
"""

import streamlit as st
from datetime import datetime, date
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.diary import DiaryManager
from src.llm_features import LLMFeatures
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="📔 智能日记助手",
    page_icon="📔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .diary-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #4CAF50;
    }
    .mood-happy { border-left-color: #FFD700; }
    .mood-calm { border-left-color: #87CEEB; }
    .mood-sad { border-left-color: #808080; }
    .mood-anxious { border-left-color: #FFA500; }
    .mood-angry { border-left-color: #FF6347; }
    .stTextArea textarea { font-size: 16px; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_manager():
    """获取日记管理器（缓存）"""
    return DiaryManager("data")


@st.cache_resource
def get_llm():
    """获取 LLM 功能（缓存）"""
    try:
        return LLMFeatures()
    except ValueError as e:
        st.error(f"⚠️ {e}")
        return None


def mood_emoji(mood: str) -> str:
    """情绪对应的 emoji"""
    emojis = {
        "开心": "😊",
        "平静": "😌",
        "难过": "😢",
        "焦虑": "😰",
        "愤怒": "😠",
    }
    return emojis.get(mood, "📝")


def main():
    """主函数"""
    manager = get_manager()
    llm = get_llm()
    
    # 侧边栏
    with st.sidebar:
        st.title("📔 智能日记助手")
        st.markdown("---")
        
        page = st.radio(
            "功能导航",
            ["✍️ 写日记", "📚 查看日记", "🔍 搜索", "📊 月度总结", "📤 导出"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 💡 今日提示")
        
        if llm and st.button("生成写作灵感"):
            with st.spinner("思考中..."):
                prompt = llm.generate_prompt()
                if prompt:
                    st.info(prompt)
    
    # 主内容区
    if page == "✍️ 写日记":
        render_write_page(manager, llm)
    elif page == "📚 查看日记":
        render_list_page(manager, llm)
    elif page == "🔍 搜索":
        render_search_page(manager)
    elif page == "📊 月度总结":
        render_summary_page(manager, llm)
    elif page == "📤 导出":
        render_export_page(manager)


def render_write_page(manager: DiaryManager, llm):
    """写日记页面"""
    st.header("✍️ 写日记")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        diary_date = st.date_input("日期", value=date.today())
    
    with col2:
        tags_input = st.text_input("标签（逗号分隔）", placeholder="生活, 学习")
    
    content = st.text_area(
        "今天想记录什么？",
        height=300,
        placeholder="写下你的想法、经历、感受...",
        key="diary_content"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        auto_analyze = st.checkbox("自动分析情绪", value=True)
    
    with col2:
        if st.button("💾 保存日记", type="primary", use_container_width=True):
            if content.strip():
                tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else None
                
                try:
                    diary = manager.add(
                        content=content,
                        date=diary_date.strftime("%Y-%m-%d"),
                        tags=tags
                    )
                    
                    st.success(f"✅ 日记保存成功！ID: {diary['id']}")
                    
                    # 自动分析情绪
                    if auto_analyze and llm:
                        with st.spinner("🔍 分析情绪中..."):
                            mood = llm.analyze_mood(content)
                            if mood:
                                manager.update_mood(diary["id"], mood)
                                st.info(f"情绪分析: {mood_emoji(mood)} {mood}")
                                
                                analysis = llm.get_mood_analysis(content)
                                if analysis:
                                    st.markdown(f"**💬 温馨提示**: {analysis}")
                    
                    # 清空输入
                    st.rerun()
                    
                except ValueError as e:
                    st.error(f"❌ {e}")
            else:
                st.warning("⚠️ 请输入日记内容")


def render_list_page(manager: DiaryManager, llm):
    """查看日记页面"""
    st.header("📚 我的日记")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        month_filter = st.text_input(
            "按月筛选 (YYYY-MM)",
            placeholder="例如: 2024-12",
            key="month_filter"
        )
    
    with col2:
        limit = st.slider("显示数量", 5, 50, 10)
    
    # 获取日记
    diaries = manager.list(
        month=month_filter if month_filter else None,
        limit=limit
    )
    
    if not diaries:
        st.info("📭 暂无日记，快去写第一篇吧！")
        return
    
    st.markdown(f"共找到 **{len(diaries)}** 篇日记")
    
    for diary in diaries:
        mood = diary.get("mood", "")
        mood_class = f"mood-{mood}" if mood else ""
        
        with st.expander(
            f"{mood_emoji(mood) if mood else '📝'} {diary['date']} - {diary['content'][:30]}...",
            expanded=False
        ):
            st.markdown(f"**ID**: {diary['id']}")
            if diary.get("tags"):
                st.markdown(f"**标签**: {', '.join(diary['tags'])}")
            if mood:
                st.markdown(f"**情绪**: {mood_emoji(mood)} {mood}")
            
            st.markdown("---")
            st.markdown(diary["content"])
            
            # 操作按钮
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if llm and st.button("🔍 分析情绪", key=f"analyze_{diary['id']}"):
                    with st.spinner("分析中..."):
                        new_mood = llm.analyze_mood(diary["content"])
                        if new_mood:
                            manager.update_mood(diary["id"], new_mood)
                            st.success(f"情绪: {mood_emoji(new_mood)} {new_mood}")
                            st.rerun()
            
            with col2:
                if llm and st.button("💡 写作建议", key=f"suggest_{diary['id']}"):
                    with st.spinner("生成建议中..."):
                        suggestion = llm.get_writing_suggestion(diary["content"])
                        if suggestion:
                            st.info(suggestion)
            
            with col3:
                if st.button("🗑️ 删除", key=f"delete_{diary['id']}"):
                    if manager.delete(diary["id"]):
                        st.success("已删除")
                        st.rerun()


def render_search_page(manager: DiaryManager):
    """搜索页面"""
    st.header("🔍 搜索日记")
    
    keyword = st.text_input("搜索关键词", placeholder="输入要搜索的内容...")
    
    if keyword:
        results = manager.search(keyword)
        
        if results:
            st.success(f"找到 {len(results)} 篇相关日记")
            
            for diary in results:
                mood = diary.get("mood", "")
                with st.expander(f"{diary['date']} - {diary['content'][:50]}..."):
                    st.markdown(diary["content"])
                    if mood:
                        st.markdown(f"情绪: {mood_emoji(mood)} {mood}")
        else:
            st.info("😔 没有找到匹配的日记")


def render_summary_page(manager: DiaryManager, llm):
    """月度总结页面"""
    st.header("📊 月度总结")
    
    month = st.text_input(
        "选择月份 (YYYY-MM)",
        value=datetime.now().strftime("%Y-%m"),
        placeholder="例如: 2024-12"
    )
    
    if st.button("生成总结", type="primary"):
        if not llm:
            st.error("⚠️ LLM 功能不可用，请检查 API Key 配置")
            return
        
        try:
            diaries = manager.get_month_diaries(month)
        except ValueError as e:
            st.error(f"❌ {e}")
            return
        
        if not diaries:
            st.info(f"📭 {month} 没有日记记录")
            return
        
        st.info(f"📚 {month} 共有 {len(diaries)} 篇日记")
        
        with st.spinner("🤖 AI 正在生成月度总结..."):
            summary = llm.generate_monthly_summary(diaries)
            
            if summary:
                st.markdown("---")
                st.markdown(f"## 📅 {month} 月度总结")
                st.markdown(summary)
            else:
                st.error("生成总结失败，请稍后重试")


def render_export_page(manager: DiaryManager):
    """导出页面"""
    st.header("📤 导出日记")
    
    month = st.text_input(
        "导出月份 (留空导出全部)",
        placeholder="例如: 2024-12"
    )
    
    if st.button("导出为 Markdown", type="primary"):
        output_path = f"output/diary_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            path = manager.export(output_path, month if month else None)
            
            # 读取文件内容
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            st.success(f"✅ 导出成功！")
            
            # 提供下载
            st.download_button(
                label="📥 下载文件",
                data=content,
                file_name=os.path.basename(path),
                mime="text/markdown"
            )
            
            # 预览
            with st.expander("预览内容"):
                st.markdown(content)
                
        except Exception as e:
            st.error(f"❌ 导出失败: {e}")


if __name__ == "__main__":
    main()

