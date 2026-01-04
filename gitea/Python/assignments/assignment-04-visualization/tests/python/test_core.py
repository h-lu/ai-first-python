"""
Core 测试 - 基础功能（隐藏）
测试核心功能：数据加载、统计、柱状图、折线图、报告生成
"""

import pytest
import os
from pathlib import Path
import pandas as pd
from src.dashboard import DataDashboard


@pytest.fixture
def sample_csv(tmp_path):
    """创建标准测试数据"""
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


class TestCoreLoadData:
    """测试数据加载功能"""

    def test_core_load_csv_success(self, sample_csv):
        """测试成功加载 CSV"""
        dashboard = DataDashboard(sample_csv)
        
        assert dashboard.df is not None
        assert len(dashboard.df) == 6

    def test_core_load_csv_dataframe(self, sample_csv):
        """测试返回有效的 DataFrame"""
        dashboard = DataDashboard(sample_csv)
        
        assert isinstance(dashboard.df, pd.DataFrame)
        assert len(dashboard.df.columns) == 4


class TestCoreStats:
    """测试统计功能"""

    def test_core_basic_stats_structure(self, sample_csv):
        """测试统计结果包含必要字段"""
        dashboard = DataDashboard(sample_csv)
        stats = dashboard.get_basic_stats()
        
        assert 'row_count' in stats
        assert 'column_count' in stats
        assert 'missing_count' in stats

    def test_core_basic_stats_values(self, sample_csv):
        """测试统计值计算正确"""
        dashboard = DataDashboard(sample_csv)
        stats = dashboard.get_basic_stats()
        
        assert stats['row_count'] == 6
        assert stats['column_count'] == 4


class TestCoreBarChart:
    """测试柱状图功能"""

    def test_core_bar_chart_create(self, sample_csv, tmp_path):
        """测试成功生成柱状图"""
        dashboard = DataDashboard(sample_csv)
        output_path = tmp_path / "bar.png"
        
        # 应该不抛出异常
        dashboard.create_bar_chart(
            x_col='城市',
            y_col='AQI',
            save_path=str(output_path)
        )

    def test_core_bar_chart_save(self, sample_csv, tmp_path):
        """测试成功保存为 PNG"""
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


class TestCoreLineChart:
    """测试折线图功能"""

    def test_core_line_chart_create(self, sample_csv, tmp_path):
        """测试成功生成折线图"""
        dashboard = DataDashboard(sample_csv)
        output_path = tmp_path / "line.png"
        
        dashboard.create_line_chart(
            x_col='日期',
            y_col='AQI',
            save_path=str(output_path)
        )

    def test_core_line_chart_save(self, sample_csv, tmp_path):
        """测试成功保存为 PNG"""
        dashboard = DataDashboard(sample_csv)
        output_path = tmp_path / "line_chart.png"
        
        dashboard.create_line_chart(
            x_col='日期',
            y_col='AQI',
            title='AQI变化趋势',
            save_path=str(output_path)
        )
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0


class TestCoreHeatmap:
    """测试热图功能"""

    def test_core_heatmap_create(self, sample_csv, tmp_path):
        """测试成功生成相关性热图"""
        dashboard = DataDashboard(sample_csv)
        output_path = tmp_path / "heatmap.png"
        
        dashboard.create_heatmap(
            columns=['AQI', 'PM2.5'],
            save_path=str(output_path)
        )
        
        assert output_path.exists()


class TestCoreReport:
    """测试报告生成功能"""

    def test_core_generate_report(self, sample_csv, tmp_path):
        """测试成功生成多个图表"""
        dashboard = DataDashboard(sample_csv)
        output_dir = tmp_path / "report"
        output_dir.mkdir()
        
        result = dashboard.generate_report(str(output_dir))
        
        assert 'generated_files' in result
        assert len(result['generated_files']) > 0

