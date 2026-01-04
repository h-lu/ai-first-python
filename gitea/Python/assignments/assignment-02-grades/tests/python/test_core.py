"""
Core 测试 - 基础功能（隐藏）
测试核心功能：CSV加载、平均分、分布统计、排名、导出
"""

import pytest
import os
from src.grade_analyzer import GradeAnalyzer


@pytest.fixture
def sample_csv(tmp_path):
    """创建标准测试数据"""
    content = """学号,姓名,语文,数学,英语
2024001,张三,85,92,78
2024002,李四,76,88,82
2024003,王五,90,95,88"""
    p = tmp_path / "test_grades.csv"
    p.write_text(content, encoding='utf-8')
    return str(p)


class TestCoreLoadCSV:
    """测试 CSV 加载功能"""

    def test_core_load_csv_success(self, sample_csv):
        """测试成功加载 CSV"""
        analyzer = GradeAnalyzer()
        assert analyzer.load_csv(sample_csv) == True
        assert len(analyzer.students) == 3

    def test_core_load_csv_student_data(self, sample_csv):
        """测试学生数据是否正确解析"""
        analyzer = GradeAnalyzer()
        analyzer.load_csv(sample_csv)
        # 检查是否包含学生信息
        names = [s.get('姓名', s.get('name', '')) for s in analyzer.students]
        assert '张三' in names or any('张三' in str(s) for s in analyzer.students)


class TestCoreAverage:
    """测试平均分计算"""

    def test_core_average_math(self, sample_csv):
        """测试数学平均分"""
        analyzer = GradeAnalyzer()
        analyzer.load_csv(sample_csv)
        # (92 + 88 + 95) / 3 = 91.67
        assert abs(analyzer.get_average("数学") - 91.67) < 0.1

    def test_core_average_chinese(self, sample_csv):
        """测试语文平均分"""
        analyzer = GradeAnalyzer()
        analyzer.load_csv(sample_csv)
        # (85 + 76 + 90) / 3 = 83.67
        assert abs(analyzer.get_average("语文") - 83.67) < 0.1

    def test_core_average_english(self, sample_csv):
        """测试英语平均分"""
        analyzer = GradeAnalyzer()
        analyzer.load_csv(sample_csv)
        # (78 + 82 + 88) / 3 = 82.67
        assert abs(analyzer.get_average("英语") - 82.67) < 0.1


class TestCoreDistribution:
    """测试分数分布统计"""

    def test_core_distribution_english(self, sample_csv):
        """测试英语分数分布"""
        analyzer = GradeAnalyzer()
        analyzer.load_csv(sample_csv)
        # 英语: 78(及格), 82(良好), 88(良好)
        dist = analyzer.get_distribution("英语")
        assert dist.get("良好", 0) == 2
        assert dist.get("及格", 0) == 1
        assert dist.get("优秀", 0) == 0

    def test_core_distribution_math(self, sample_csv):
        """测试数学分数分布"""
        analyzer = GradeAnalyzer()
        analyzer.load_csv(sample_csv)
        # 数学: 92(优秀), 88(良好), 95(优秀)
        dist = analyzer.get_distribution("数学")
        assert dist.get("优秀", 0) == 2
        assert dist.get("良好", 0) == 1


class TestCoreRanking:
    """测试排名功能"""

    def test_core_ranking_basic(self, sample_csv):
        """测试基本排名"""
        analyzer = GradeAnalyzer()
        analyzer.load_csv(sample_csv)
        ranking = analyzer.get_ranking("数学")
        
        assert len(ranking) == 3
        # 第一名应该是 95 分
        assert ranking[0]['score'] == 95
        assert ranking[0]['rank'] == 1

    def test_core_ranking_tie(self, tmp_path):
        """测试并列排名处理"""
        content = """学号,姓名,数学
2024001,A,95
2024002,B,90
2024003,C,95
2024004,D,80"""
        p = tmp_path / "ranking.csv"
        p.write_text(content, encoding='utf-8')
        
        analyzer = GradeAnalyzer()
        analyzer.load_csv(str(p))
        ranking = analyzer.get_ranking("数学")
        
        # 找出 95 分的学生
        top_scores = [r for r in ranking if r['score'] == 95]
        assert len(top_scores) == 2
        # 两个 95 分都应该是第 1 名
        assert all(r['rank'] == 1 for r in top_scores)
        
        # 90 分应该是第 3 名（跳过第 2）
        third = [r for r in ranking if r['score'] == 90][0]
        assert third['rank'] == 3


class TestCoreExport:
    """测试导出功能"""

    def test_core_export_success(self, sample_csv, tmp_path):
        """测试导出报告"""
        analyzer = GradeAnalyzer()
        analyzer.load_csv(sample_csv)
        output_path = tmp_path / "report.txt"
        
        assert analyzer.export_report(str(output_path)) == True
        assert os.path.exists(str(output_path))

    def test_core_export_content(self, sample_csv, tmp_path):
        """测试导出报告内容"""
        analyzer = GradeAnalyzer()
        analyzer.load_csv(sample_csv)
        output_path = tmp_path / "report.txt"
        analyzer.export_report(str(output_path))
        
        content = output_path.read_text(encoding='utf-8')
        # 报告应包含科目信息
        assert "数学" in content or "语文" in content or "英语" in content
