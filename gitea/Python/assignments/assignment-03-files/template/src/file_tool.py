"""
文件批量处理工具

你的任务是实现 FileTool 类，批量处理目录下的文件。

功能要求：
1. 列出目录下所有文件（支持递归、支持隐藏文件筛选）
2. 按扩展名筛选文件
3. 批量重命名（添加前缀/后缀，支持 dry_run 预览模式）
4. 按文件类型整理到子目录
5. 统计文件大小分布

⚠️ 安全注意事项：
- 文件操作是危险的，错误的代码可能导致数据丢失
- 始终在测试目录中操作，不要在重要目录测试
- 先用 dry_run 模式预览，确认无误后再执行
- 重命名冲突时绝不应该静默覆盖已有文件

边界情况处理：
- 隐藏文件（以.开头）：默认不列出，可选包含
- 无扩展名文件：extension 字段返回空字符串，不应崩溃
- 重命名冲突：不覆盖已有文件，应跳过或报错
- 权限错误：无权限文件应跳过，不崩溃
- 符号链接：特殊处理，不跟随链接

示例用法：
tool = FileTool("/path/to/directory")
files = tool.list_files(recursive=True)
result = tool.batch_rename("*.txt", prefix="2024_", dry_run=True)  # 先预览
result = tool.batch_rename("*.txt", prefix="2024_")  # 确认后执行
stats = tool.get_size_stats()

提示：
- 使用 pathlib 库处理路径（比 os.path 更现代）
- 使用 fnmatch 或 glob 进行模式匹配
- 妥善处理各种异常：PermissionError, FileExistsError, FileNotFoundError
"""

from pathlib import Path
from typing import List, Dict, Optional
import fnmatch


class FileTool:
    """
    文件批量处理工具
    
    提供文件列出、筛选、重命名、整理、统计等功能。
    """

    def __init__(self, root_path: str):
        """
        初始化，设置工作目录
        
        Args:
            root_path: 工作目录路径
        """
        self.root = Path(root_path)
        # TODO: 你可以添加其他属性来辅助实现

    def list_files(self, recursive: bool = False, 
                   include_hidden: bool = False) -> List[Dict]:
        """
        列出目录内容
        
        Args:
            recursive: 是否递归子目录
            include_hidden: 是否包含隐藏文件（以.开头的文件）
            
        Returns:
            文件信息列表，每个元素包含：
            - 'name': 文件名
            - 'path': 完整路径（字符串）
            - 'size': 文件大小（字节），目录为 0
            - 'type': 'file' 或 'directory'
            - 'extension': 扩展名（如 '.txt'），无扩展名为空字符串
            
        示例返回：
            [
                {'name': 'file.txt', 'path': '/path/file.txt', 'size': 1024, 
                 'type': 'file', 'extension': '.txt'},
                {'name': 'subdir', 'path': '/path/subdir', 'size': 0, 
                 'type': 'directory', 'extension': ''},
            ]
        """
        # TODO: 在此实现你的代码
        pass

    def filter_by_extension(self, extensions: List[str]) -> List[Dict]:
        """
        按扩展名筛选文件
        
        Args:
            extensions: 扩展名列表，如 ['.txt', '.py', '.md']
            
        Returns:
            匹配的文件列表（格式同 list_files）
            
        注意：
        - 扩展名比较应不区分大小写（.TXT 和 .txt 应该匹配）
        - 只返回文件，不返回目录
        """
        # TODO: 在此实现你的代码
        pass

    def batch_rename(self, pattern: str, 
                     prefix: str = '', 
                     suffix: str = '',
                     dry_run: bool = False) -> Dict:
        """
        批量重命名
        
        Args:
            pattern: 文件名匹配模式（如 '*.txt', 'report_*.csv'）
            prefix: 添加前缀
            suffix: 添加后缀（在扩展名之前）
            dry_run: 如果为 True，只返回预览结果，不实际重命名
            
        Returns:
            {
                'success': [{'old': 'file.txt', 'new': 'prefix_file_suffix.txt'}, ...],
                'failed': [{'file': 'xxx', 'reason': '目标文件已存在'}, ...],
                'skipped': [{'file': 'xxx', 'reason': '无权限'}, ...]
            }
            
        重要：
        - dry_run=True 时只返回预览，不实际修改任何文件
        - 重命名冲突时（目标文件已存在）不应覆盖，应放入 failed 或 skipped
        - 无权限时应跳过，不崩溃
        
        示例：
            # 先预览
            result = tool.batch_rename("*.txt", prefix="2024_", dry_run=True)
            print(result)  # 查看会重命名哪些文件
            
            # 确认后执行
            result = tool.batch_rename("*.txt", prefix="2024_")
        """
        # TODO: 在此实现你的代码
        pass

    def organize_by_type(self, type_mapping: Optional[Dict[str, str]] = None,
                         dry_run: bool = False) -> Dict:
        """
        按文件类型分类到子目录
        
        Args:
            type_mapping: 扩展名到目录的映射，如：
                {'.txt': 'documents', '.py': 'code', '.jpg': 'images', '.png': 'images'}
                如果为 None，使用默认映射
            dry_run: 预览模式
            
        Returns:
            {
                'moved': [{'file': 'xxx', 'from': '...', 'to': '...'}, ...],
                'failed': [{'file': 'xxx', 'reason': '...'}, ...]
            }
            
        默认映射：
            - documents: .txt, .doc, .docx, .pdf, .md
            - code: .py, .js, .java, .c, .cpp, .h
            - images: .jpg, .jpeg, .png, .gif, .bmp
            - data: .csv, .json, .xml, .yaml, .yml
            - other: 其他未匹配的文件
        """
        # TODO: 在此实现你的代码
        pass

    def get_size_stats(self) -> Dict:
        """
        统计文件大小分布
        
        Returns:
            {
                'total_files': 100,           # 文件总数
                'total_size': 1024000,        # 总大小（字节）
                'by_size': {                  # 按大小分布
                    '<1KB': 20,
                    '1KB-100KB': 50,
                    '100KB-1MB': 20,
                    '>1MB': 10
                },
                'by_type': {                  # 按类型分布
                    '.txt': {'count': 30, 'size': 102400},
                    '.py': {'count': 20, 'size': 51200},
                    '': {'count': 5, 'size': 1024},  # 无扩展名
                    ...
                }
            }
            
        注意：
        - 只统计文件，不统计目录
        - 无扩展名文件的 key 为空字符串 ''
        """
        # TODO: 在此实现你的代码
        pass


if __name__ == "__main__":
    # 测试你的实现
    import tempfile
    import os
    
    # 创建临时测试目录
    with tempfile.TemporaryDirectory() as tmp_dir:
        # 创建测试文件
        Path(tmp_dir, "file1.txt").write_text("hello")
        Path(tmp_dir, "file2.py").write_text("print('hi')")
        Path(tmp_dir, "report_01.txt").write_text("report 1")
        Path(tmp_dir, "report_02.txt").write_text("report 2")
        Path(tmp_dir, ".hidden").write_text("hidden file")
        Path(tmp_dir, "README").write_text("no extension")
        Path(tmp_dir, "subdir").mkdir()
        
        tool = FileTool(tmp_dir)
        
        # 测试列出文件
        print("=== 列出文件（不含隐藏）===")
        files = tool.list_files()
        for f in files:
            print(f"  {f['name']} ({f['type']}, {f['size']} bytes)")
        
        # 测试列出文件（含隐藏）
        print("\n=== 列出文件（含隐藏）===")
        files = tool.list_files(include_hidden=True)
        for f in files:
            print(f"  {f['name']} ({f['type']})")
        
        # 测试筛选
        print("\n=== 筛选 .txt 文件 ===")
        txt_files = tool.filter_by_extension(['.txt'])
        for f in txt_files:
            print(f"  {f['name']}")
        
        # 测试重命名（预览）
        print("\n=== 重命名预览 ===")
        result = tool.batch_rename("report_*.txt", prefix="2024_", dry_run=True)
        print(f"  预览结果: {result}")
        
        # 测试统计
        print("\n=== 文件统计 ===")
        stats = tool.get_size_stats()
        print(f"  总文件数: {stats.get('total_files', 'N/A')}")
        print(f"  总大小: {stats.get('total_size', 'N/A')} bytes")

