"""
公开测试 - 学生可见
这些测试帮助你验证基本功能是否正确
"""

import pytest
from src.grade_analyzer import GradeAnalyzer


@pytest.fixture
def sample_csv(tmp_path):
    """创建测试用的 CSV 文件"""
    content = """学号,姓名,语文,数学,英语
2024001,张三,85,92,78
2024002,李四,76,88,82
2024003,王五,90,95,88"""
    p = tmp_path / "test_grades.csv"
    p.write_text(content, encoding='utf-8')
    return str(p)


def test_load_csv(sample_csv):
    """测试能否成功加载 CSV 文件"""
    analyzer = GradeAnalyzer()
    result = analyzer.load_csv(sample_csv)
    assert result == True
    assert len(analyzer.students) == 3


def test_get_average(sample_csv):
    """测试平均分计算是否正确"""
    analyzer = GradeAnalyzer()
    analyzer.load_csv(sample_csv)
    # 数学: (92 + 88 + 95) / 3 = 91.67
    avg = analyzer.get_average("数学")
    assert abs(avg - 91.67) < 0.1


def test_get_ranking_structure(sample_csv):
    """测试排名返回值的数据结构"""
    analyzer = GradeAnalyzer()
    analyzer.load_csv(sample_csv)
    ranking = analyzer.get_ranking("英语")
    
    assert isinstance(ranking, list)
    assert len(ranking) > 0
    # 检查必要字段
    first = ranking[0]
    assert 'rank' in first
    assert 'name' in first
    assert 'score' in first
