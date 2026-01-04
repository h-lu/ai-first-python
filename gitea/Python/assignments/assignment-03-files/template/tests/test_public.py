"""
公开测试 - 学生可见
这些测试帮助你验证基本功能是否正确
"""

import pytest
from pathlib import Path
from src.file_tool import FileTool


@pytest.fixture
def sample_dir(tmp_path):
    """创建测试目录结构"""
    # 创建文件
    (tmp_path / "file1.txt").write_text("hello")
    (tmp_path / "file2.py").write_text("print('hi')")
    (tmp_path / "report_01.txt").write_text("report 1")
    (tmp_path / "report_02.txt").write_text("report 2")
    # 创建子目录
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "nested.txt").write_text("nested")
    return tmp_path


def test_list_files_basic(sample_dir):
    """测试基本列出文件功能"""
    tool = FileTool(str(sample_dir))
    files = tool.list_files()
    
    # 应该包含文件和目录
    names = [f['name'] for f in files]
    assert "file1.txt" in names
    assert "file2.py" in names
    assert "subdir" in names


def test_list_files_info(sample_dir):
    """测试文件信息是否完整"""
    tool = FileTool(str(sample_dir))
    files = tool.list_files()
    
    # 找到 file1.txt
    txt_file = next(f for f in files if f['name'] == 'file1.txt')
    
    assert txt_file['type'] == 'file'
    assert txt_file['extension'] == '.txt'
    assert txt_file['size'] > 0
    assert 'path' in txt_file


def test_filter_by_extension(sample_dir):
    """测试按扩展名筛选"""
    tool = FileTool(str(sample_dir))
    txt_files = tool.filter_by_extension(['.txt'])
    
    names = [f['name'] for f in txt_files]
    assert "file1.txt" in names
    assert "report_01.txt" in names
    assert "file2.py" not in names


def test_batch_rename_dry_run(sample_dir):
    """测试重命名预览模式"""
    tool = FileTool(str(sample_dir))
    result = tool.batch_rename("report_*.txt", prefix="2024_", dry_run=True)
    
    # 预览模式应该返回结果
    assert 'success' in result
    assert len(result['success']) == 2
    
    # 但文件不应该被实际重命名
    assert (sample_dir / "report_01.txt").exists()
    assert not (sample_dir / "2024_report_01.txt").exists()

