"""
Edge 测试 - 边界情况（隐藏）
测试边界处理：隐藏文件、无扩展名、重命名冲突、权限错误
"""

import pytest
import os
from pathlib import Path
from src.file_tool import FileTool


class TestEdgeHiddenFiles:
    """测试隐藏文件处理"""

    def test_edge_hidden_files_default(self, tmp_path):
        """默认不列出隐藏文件"""
        (tmp_path / ".gitignore").write_text("*.pyc")
        (tmp_path / ".env").write_text("SECRET=xxx")
        (tmp_path / "normal.txt").write_text("hello")
        
        tool = FileTool(str(tmp_path))
        files = tool.list_files(include_hidden=False)
        
        names = [f['name'] for f in files]
        assert "normal.txt" in names
        assert ".gitignore" not in names
        assert ".env" not in names

    def test_edge_hidden_files_include(self, tmp_path):
        """可选列出隐藏文件"""
        (tmp_path / ".gitignore").write_text("*.pyc")
        (tmp_path / "normal.txt").write_text("hello")
        
        tool = FileTool(str(tmp_path))
        files = tool.list_files(include_hidden=True)
        
        names = [f['name'] for f in files]
        assert "normal.txt" in names
        assert ".gitignore" in names


class TestEdgeNoExtension:
    """测试无扩展名文件"""

    def test_edge_no_extension_file(self, tmp_path):
        """正确处理无扩展名文件"""
        (tmp_path / "README").write_text("readme content")
        (tmp_path / "Makefile").write_text("make content")
        (tmp_path / "normal.txt").write_text("txt content")
        
        tool = FileTool(str(tmp_path))
        files = tool.list_files()
        
        # 应该能列出无扩展名文件
        names = [f['name'] for f in files]
        assert "README" in names
        assert "Makefile" in names
        
        # 无扩展名文件的 extension 应为空字符串
        readme = next(f for f in files if f['name'] == 'README')
        assert readme['extension'] == ''


class TestEdgeRenameConflict:
    """测试重命名冲突"""

    def test_edge_rename_conflict(self, tmp_path):
        """重命名冲突时不应覆盖已有文件"""
        (tmp_path / "file.txt").write_text("original")
        (tmp_path / "new_file.txt").write_text("existing content")
        
        tool = FileTool(str(tmp_path))
        result = tool.batch_rename("file.txt", prefix="new_")
        
        # 应该失败或跳过，而不是覆盖
        assert len(result.get('failed', [])) >= 1 or len(result.get('skipped', [])) >= 1
        
        # 原有文件内容不应改变
        assert (tmp_path / "new_file.txt").read_text() == "existing content"


class TestEdgePermission:
    """测试权限错误"""

    @pytest.mark.skipif(os.name == 'nt', reason="Windows 权限处理不同")
    def test_edge_permission_error(self, tmp_path):
        """无权限文件应该跳过，不崩溃"""
        test_file = tmp_path / "readonly.txt"
        test_file.write_text("content")
        test_file.chmod(0o000)  # 移除所有权限
        
        tool = FileTool(str(tmp_path))
        
        try:
            result = tool.batch_rename("*.txt", prefix="new_")
            # 应该在 skipped 或 failed 中，而不是崩溃
            total_handled = len(result.get('skipped', [])) + len(result.get('failed', []))
            assert total_handled >= 1
        finally:
            test_file.chmod(0o644)  # 恢复权限以便清理


class TestEdgeEmptyDirectory:
    """测试空目录"""

    def test_edge_empty_directory(self, tmp_path):
        """空目录不崩溃"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        tool = FileTool(str(empty_dir))
        files = tool.list_files()
        
        assert files == []

    def test_edge_empty_stats(self, tmp_path):
        """空目录统计不崩溃"""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        
        tool = FileTool(str(empty_dir))
        stats = tool.get_size_stats()
        
        assert stats['total_files'] == 0
        assert stats['total_size'] == 0


class TestEdgeSymlink:
    """测试符号链接"""

    @pytest.mark.skipif(os.name == 'nt', reason="Windows 符号链接需要特权")
    def test_edge_symlink_handling(self, tmp_path):
        """正确处理符号链接"""
        # 创建文件和符号链接
        real_file = tmp_path / "real.txt"
        real_file.write_text("real content")
        
        link_file = tmp_path / "link.txt"
        link_file.symlink_to(real_file)
        
        tool = FileTool(str(tmp_path))
        files = tool.list_files()
        
        # 应该能列出符号链接
        names = [f['name'] for f in files]
        assert "real.txt" in names
        assert "link.txt" in names

