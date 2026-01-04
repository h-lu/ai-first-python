"""
Edge 测试 - 边界情况（隐藏）
测试边界处理：缺失值、中文标签、异常值、空数据
"""

import pytest
from pathlib import Path
import pandas as pd
from src.dashboard import DataDashboard


class TestEdgeMissingData:
    """测试缺失值处理"""

    def test_edge_missing_data_chart(self, tmp_path):
        """缺失值应该被正确处理，不导致崩溃"""
        content = """日期,值
2024-01-01,100
2024-01-02,
2024-01-03,150
2024-01-04,
2024-01-05,200"""
        
        csv_file = tmp_path / "missing.csv"
        csv_file.write_text(content, encoding='utf-8')
        
        dashboard = DataDashboard(str(csv_file))
        
        # 生成折线图不应崩溃
        output = tmp_path / "chart.png"
        dashboard.create_line_chart('日期', '值', save_path=str(output))
        
        assert output.exists()

    def test_edge_missing_stats(self, tmp_path):
        """统计应该正确报告缺失值"""
        content = """A,B,C
1,,3
4,5,
7,8,9"""
        
        csv_file = tmp_path / "missing.csv"
        csv_file.write_text(content, encoding='utf-8')
        
        dashboard = DataDashboard(str(csv_file))
        stats = dashboard.get_basic_stats()
        
        # 应该记录缺失值数量
        assert 'missing_count' in stats
        assert stats['missing_count'].get('B', 0) >= 1


class TestEdgeChineseLabels:
    """测试中文标签处理"""

    def test_edge_chinese_labels(self, tmp_path):
        """中文标签应该正确显示"""
        content = """城市,销量
北京,100
上海,150
广州,120"""
        
        csv_file = tmp_path / "chinese.csv"
        csv_file.write_text(content, encoding='utf-8')
        
        dashboard = DataDashboard(str(csv_file))
        
        output = tmp_path / "chinese_chart.png"
        dashboard.create_bar_chart(
            x_col='城市',
            y_col='销量',
            title='各城市销量对比',
            save_path=str(output)
        )
        
        # 检查图片是否生成
        assert output.exists()
        assert output.stat().st_size > 0


class TestEdgeOutlier:
    """测试异常值处理"""

    def test_edge_outlier_handling(self, tmp_path):
        """异常值不应该完全破坏图表"""
        content = """类别,值
A,100
B,150
C,10000
D,120"""  # C 是异常值
        
        csv_file = tmp_path / "outlier.csv"
        csv_file.write_text(content, encoding='utf-8')
        
        dashboard = DataDashboard(str(csv_file))
        output = tmp_path / "chart.png"
        
        # 生成柱状图不应崩溃
        dashboard.create_bar_chart('类别', '值', save_path=str(output))
        
        assert output.exists()


class TestEdgeEmptyData:
    """测试空数据处理"""

    def test_edge_empty_column(self, tmp_path):
        """空列不导致崩溃"""
        content = """A,B,C
1,,
2,,
3,,"""
        
        csv_file = tmp_path / "empty_col.csv"
        csv_file.write_text(content, encoding='utf-8')
        
        dashboard = DataDashboard(str(csv_file))
        
        # 获取统计不应崩溃
        stats = dashboard.get_basic_stats()
        assert stats is not None

    def test_edge_header_only(self, tmp_path):
        """只有表头的文件不崩溃"""
        content = """A,B,C\n"""
        
        csv_file = tmp_path / "header_only.csv"
        csv_file.write_text(content, encoding='utf-8')
        
        dashboard = DataDashboard(str(csv_file))
        
        stats = dashboard.get_basic_stats()
        assert stats['row_count'] == 0


class TestEdgeEncoding:
    """测试编码处理"""

    def test_edge_encoding_gbk(self, tmp_path):
        """测试 GBK 编码文件"""
        content = "城市,数值\n北京,100\n上海,200"
        
        csv_file = tmp_path / "gbk.csv"
        csv_file.write_bytes(content.encode('gbk'))
        
        dashboard = DataDashboard(str(csv_file))
        
        # 应该能成功加载
        assert dashboard.df is not None
        assert len(dashboard.df) == 2

