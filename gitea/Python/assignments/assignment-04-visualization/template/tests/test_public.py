"""
公开测试 - 学生可见
这些测试帮助你验证基本功能是否正确
"""

import pytest
from pathlib import Path
import pandas as pd
from src.dashboard import DataDashboard


@pytest.fixture
def sample_csv(tmp_path):
    """创建测试用的 CSV 文件"""
    content = """日期,城市,AQI,PM2.5
2024-01-01,北京,120,80
2024-01-01,上海,85,55
2024-01-02,北京,100,65
2024-01-02,上海,90,60
2024-01-03,北京,150,100
2024-01-03,上海,75,50"""
    p = tmp_path / "test_data.csv"
    p.write_text(content, encoding='utf-8')
    return str(p)


def test_load_csv(sample_csv):
    """测试能否成功加载 CSV 文件"""
    dashboard = DataDashboard(sample_csv)
    
    assert dashboard.df is not None
    assert len(dashboard.df) == 6
    assert isinstance(dashboard.df, pd.DataFrame)


def test_basic_stats(sample_csv):
    """测试基本统计功能"""
    dashboard = DataDashboard(sample_csv)
    stats = dashboard.get_basic_stats()
    
    assert 'row_count' in stats
    assert 'column_count' in stats
    assert 'missing_count' in stats
    assert stats['row_count'] == 6
    assert stats['column_count'] == 4


def test_bar_chart_save(sample_csv, tmp_path):
    """测试柱状图保存"""
    dashboard = DataDashboard(sample_csv)
    
    output_path = tmp_path / "bar_chart.png"
    dashboard.create_bar_chart(
        x_col='城市',
        y_col='AQI',
        title='各城市平均AQI',
        save_path=str(output_path)
    )
    
    assert output_path.exists()
    assert output_path.stat().st_size > 0

