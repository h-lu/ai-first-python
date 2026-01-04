"""
Core 测试 - 基础功能（隐藏）
测试核心功能：列出文件、筛选、重命名、整理、统计
"""

import pytest
from pathlib import Path
from src.file_tool import FileTool


@pytest.fixture
def sample_dir(tmp_path):
    """创建标准测试目录"""
    # 创建文件
    (tmp_path / "file1.txt").write_text("hello world")
    (tmp_path / "file2.py").write_text("print('hi')")
    (tmp_path / "report_01.txt").write_text("report 1 content")
    (tmp_path / "report_02.txt").write_text("report 2 content")
    (tmp_path / "data.csv").write_text("a,b,c\n1,2,3")
    # 创建子目录和嵌套文件
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "nested.txt").write_text("nested file")
    (tmp_path / "subdir" / "deep").mkdir()
    (tmp_path / "subdir" / "deep" / "deepfile.py").write_text("deep")
    return tmp_path


class TestCoreListFiles:
    """测试列出文件功能"""

    def test_core_list_files_basic(self, sample_dir):
        """测试基本列出功能"""
        tool = FileTool(str(sample_dir))
        files = tool.list_files()
        
        names = [f['name'] for f in files]
        assert "file1.txt" in names
        assert "file2.py" in names
        assert "subdir" in names

    def test_core_list_files_recursive(self, sample_dir):
        """测试递归列出"""
        tool = FileTool(str(sample_dir))
        files = tool.list_files(recursive=True)
        
        names = [f['name'] for f in files]
        assert "nested.txt" in names
        assert "deepfile.py" in names

    def test_core_list_files_info(self, sample_dir):
        """测试文件信息完整性"""
        tool = FileTool(str(sample_dir))
        files = tool.list_files()
        
        # 找到 file1.txt
        txt_file = next(f for f in files if f['name'] == 'file1.txt')
        
        assert txt_file['type'] == 'file'
        assert txt_file['extension'] == '.txt'
        assert txt_file['size'] > 0
        assert 'path' in txt_file

    def test_core_list_directory_type(self, sample_dir):
        """测试目录类型标识"""
        tool = FileTool(str(sample_dir))
        files = tool.list_files()
        
        subdir = next(f for f in files if f['name'] == 'subdir')
        assert subdir['type'] == 'directory'


class TestCoreFilter:
    """测试筛选功能"""

    def test_core_filter_single_ext(self, sample_dir):
        """测试单个扩展名筛选"""
        tool = FileTool(str(sample_dir))
        txt_files = tool.filter_by_extension(['.txt'])
        
        names = [f['name'] for f in txt_files]
        assert "file1.txt" in names
        assert "report_01.txt" in names
        assert "file2.py" not in names

    def test_core_filter_multiple_ext(self, sample_dir):
        """测试多个扩展名筛选"""
        tool = FileTool(str(sample_dir))
        files = tool.filter_by_extension(['.txt', '.py'])
        
        names = [f['name'] for f in files]
        assert "file1.txt" in names
        assert "file2.py" in names
        assert "data.csv" not in names


class TestCoreRename:
    """测试重命名功能"""

    def test_core_batch_rename_prefix(self, sample_dir):
        """测试批量添加前缀"""
        tool = FileTool(str(sample_dir))
        result = tool.batch_rename("report_*.txt", prefix="2024_")
        
        assert len(result['success']) == 2
        assert (sample_dir / "2024_report_01.txt").exists()
        assert (sample_dir / "2024_report_02.txt").exists()

    def test_core_batch_rename_suffix(self, sample_dir):
        """测试批量添加后缀"""
        tool = FileTool(str(sample_dir))
        result = tool.batch_rename("file1.txt", suffix="_backup")
        
        assert len(result['success']) == 1
        assert (sample_dir / "file1_backup.txt").exists()

    def test_core_batch_rename_dry_run(self, sample_dir):
        """测试预览模式"""
        tool = FileTool(str(sample_dir))
        result = tool.batch_rename("*.txt", prefix="new_", dry_run=True)
        
        # 预览模式应返回结果
        assert len(result['success']) >= 1
        # 但文件不应实际重命名
        assert (sample_dir / "file1.txt").exists()
        assert not (sample_dir / "new_file1.txt").exists()


class TestCoreOrganize:
    """测试整理功能"""

    def test_core_organize_default_mapping(self, sample_dir):
        """测试使用默认映射整理"""
        tool = FileTool(str(sample_dir))
        result = tool.organize_by_type()
        
        # 应该有文件被移动
        assert len(result.get('moved', [])) > 0


class TestCoreStats:
    """测试统计功能"""

    def test_core_size_stats_count(self, sample_dir):
        """测试文件数量统计"""
        tool = FileTool(str(sample_dir))
        stats = tool.get_size_stats()
        
        assert 'total_files' in stats
        assert stats['total_files'] >= 5  # 至少有 5 个文件

    def test_core_size_stats_by_type(self, sample_dir):
        """测试按类型统计"""
        tool = FileTool(str(sample_dir))
        stats = tool.get_size_stats()
        
        assert 'by_type' in stats
        # 应该有 .txt 类型
        assert '.txt' in stats['by_type']
        assert stats['by_type']['.txt']['count'] >= 1

