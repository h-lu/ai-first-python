"""
Edge 测试 - 边界情况（隐藏）
测试边界处理：缺失值、无效分数、编码问题、空文件
"""

import pytest
from src.grade_analyzer import GradeAnalyzer


class TestEdgeMissingValue:
    """测试缺失值处理"""

    def test_edge_missing_single(self, tmp_path):
        """测试单个缺失值"""
        content = """学号,姓名,语文,数学,英语
2024001,张三,85,,78
2024002,李四,76,88,82"""
        p = tmp_path / "missing.csv"
        p.write_text(content, encoding='utf-8')
        
        analyzer = GradeAnalyzer()
        analyzer.load_csv(str(p))
        
        # 数学只有李四有成绩，平均分应该是 88
        avg = analyzer.get_average("数学")
        assert avg == 88.0

    def test_edge_missing_multiple(self, tmp_path):
        """测试多个缺失值"""
        content = """学号,姓名,语文,数学,英语
2024001,张三,85,,78
2024002,李四,,88,
2024003,王五,90,95,88"""
        p = tmp_path / "missing_multi.csv"
        p.write_text(content, encoding='utf-8')
        
        analyzer = GradeAnalyzer()
        analyzer.load_csv(str(p))
        
        # 语文: (85 + 90) / 2 = 87.5
        assert abs(analyzer.get_average("语文") - 87.5) < 0.1
        # 数学: (88 + 95) / 2 = 91.5
        assert abs(analyzer.get_average("数学") - 91.5) < 0.1

    def test_edge_missing_not_zero(self, tmp_path):
        """测试缺失值不应被当作 0 分"""
        content = """学号,姓名,数学
2024001,张三,
2024002,李四,80"""
        p = tmp_path / "missing_zero.csv"
        p.write_text(content, encoding='utf-8')
        
        analyzer = GradeAnalyzer()
        analyzer.load_csv(str(p))
        
        # 如果缺失值被当作 0，平均分会是 40；正确应该是 80
        avg = analyzer.get_average("数学")
        assert avg == 80.0, "缺失值不应参与平均分计算"


class TestEdgeEncoding:
    """测试编码问题"""

    def test_edge_encoding_gbk(self, tmp_path):
        """测试 GBK 编码文件"""
        content = "学号,姓名,语文\n2024001,张三,85"
        p = tmp_path / "gbk.csv"
        p.write_bytes(content.encode('gbk'))
        
        analyzer = GradeAnalyzer()
        try:
            result = analyzer.load_csv(str(p))
            # 应该能成功加载
            assert result == True
            assert len(analyzer.students) == 1
        except UnicodeDecodeError:
            pytest.fail("应该能处理 GBK 编码")


class TestEdgeEmptyFile:
    """测试空文件处理"""

    def test_edge_empty_file(self, tmp_path):
        """测试完全空的文件"""
        p = tmp_path / "empty.csv"
        p.touch()
        
        analyzer = GradeAnalyzer()
        analyzer.load_csv(str(p))
        assert len(analyzer.students) == 0

    def test_edge_header_only(self, tmp_path):
        """测试只有表头的文件"""
        content = "学号,姓名,语文,数学,英语\n"
        p = tmp_path / "header_only.csv"
        p.write_text(content, encoding='utf-8')
        
        analyzer = GradeAnalyzer()
        analyzer.load_csv(str(p))
        assert len(analyzer.students) == 0


class TestEdgeInvalidScore:
    """测试无效分数处理"""

    def test_edge_negative_score(self, tmp_path):
        """测试负分数"""
        content = """学号,姓名,语文
2024001,张三,-10
2024002,李四,85"""
        p = tmp_path / "negative.csv"
        p.write_text(content, encoding='utf-8')
        
        analyzer = GradeAnalyzer()
        analyzer.load_csv(str(p))
        
        # 负分应该被排除或标记，不影响正常数据
        # 如果实现了 invalid_count，检查它
        if hasattr(analyzer, 'invalid_count'):
            assert analyzer.invalid_count >= 1

    def test_edge_over_100_score(self, tmp_path):
        """测试超过 100 的分数"""
        content = """学号,姓名,语文
2024001,张三,150
2024002,李四,85"""
        p = tmp_path / "over100.csv"
        p.write_text(content, encoding='utf-8')
        
        analyzer = GradeAnalyzer()
        analyzer.load_csv(str(p))
        
        # 超过 100 分应该被识别
        if hasattr(analyzer, 'invalid_count'):
            assert analyzer.invalid_count >= 1
