# 作业 3：文件批量处理工具

> 📅 **布置周期**：第 6-7 周  
> 💯 **总分**：20 分  
> 🎯 **对应章节**：第 6-7 章（文件操作、错误处理）

## 任务概述

批量重命名、整理、统计目录下的文件。这是学生第一次接触文件系统操作，需要理解路径处理和异常处理。

**⚠️ 本作业涉及真实文件操作，错误的代码可能导致数据丢失。这是学习"为结果负责"的最佳场景。**

---

## 学习目标

完成本作业后，学生应能够：

1. ✅ 使用 `pathlib` 进行文件系统操作
2. ✅ 实现批量文件处理逻辑
3. ✅ 正确处理各种文件系统异常
4. ✅ 理解防御式编程思维
5. ✅ **为代码结果负责**——文件操作不可轻率

---

## 功能需求

### 类接口设计

```python
from pathlib import Path
from typing import List, Dict, Optional

class FileTool:
    """文件批量处理工具"""
    
    def __init__(self, root_path: str):
        """
        初始化，设置工作目录
        
        Args:
            root_path: 工作目录路径
        """
        self.root = Path(root_path)
    
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
            - 'path': 完整路径
            - 'size': 文件大小（字节）
            - 'type': 'file' 或 'directory'
            - 'extension': 扩展名（无扩展名为空字符串）
        """
        pass
    
    def filter_by_extension(self, extensions: List[str]) -> List[Dict]:
        """
        按扩展名筛选文件
        
        Args:
            extensions: 扩展名列表，如 ['.txt', '.py', '.md']
            
        Returns:
            匹配的文件列表
        """
        pass
    
    def batch_rename(self, pattern: str, 
                     prefix: str = '', 
                     suffix: str = '',
                     dry_run: bool = False) -> Dict:
        """
        批量重命名
        
        Args:
            pattern: 文件名匹配模式（如 '*.txt'）
            prefix: 添加前缀
            suffix: 添加后缀（在扩展名之前）
            dry_run: 如果为 True，只返回预览结果，不实际重命名
            
        Returns:
            {
                'success': [{'old': '...', 'new': '...'}, ...],
                'failed': [{'file': '...', 'reason': '...'}, ...],
                'skipped': [{'file': '...', 'reason': '...'}, ...]
            }
            
        注意：
        - 重命名冲突时不应覆盖已有文件
        - 无权限文件应跳过，不崩溃
        - dry_run 模式用于预览，让用户确认后再执行
        """
        pass
    
    def organize_by_type(self, type_mapping: Optional[Dict[str, str]] = None,
                         dry_run: bool = False) -> Dict:
        """
        按文件类型分类到子目录
        
        Args:
            type_mapping: 扩展名到目录的映射
                默认: {'.txt': 'documents', '.py': 'code', 
                       '.jpg': 'images', '.png': 'images', ...}
            dry_run: 预览模式
            
        Returns:
            移动结果统计 {'moved': [...], 'failed': [...]}
        """
        pass
    
    def get_size_stats(self) -> Dict:
        """
        统计文件大小分布
        
        Returns:
            {
                'total_files': 100,
                'total_size': 1024000,  # 字节
                'by_size': {
                    '<1KB': 20,
                    '1KB-100KB': 50,
                    '100KB-1MB': 20,
                    '>1MB': 10
                },
                'by_type': {
                    '.txt': {'count': 30, 'size': 102400},
                    '.py': {'count': 20, 'size': 51200},
                    ...
                }
            }
        """
        pass
```

---

## 测试用例设计

### Core 测试（10 分）

| 测试类别 | 测试名称 | 说明 |
|---------|---------|------|
| 列出文件 | `test_list_files_basic` | 列出目录下的文件和文件夹 |
| 列出文件 | `test_list_files_recursive` | 递归列出子目录内容 |
| 列出文件 | `test_list_files_info` | 返回正确的文件信息（大小、类型） |
| 筛选 | `test_filter_single_ext` | 按单个扩展名筛选 |
| 筛选 | `test_filter_multiple_ext` | 按多个扩展名筛选 |
| 重命名 | `test_batch_rename_prefix` | 批量添加前缀 |
| 重命名 | `test_batch_rename_suffix` | 批量添加后缀 |
| 重命名 | `test_batch_rename_dry_run` | 预览模式不实际修改文件 |
| 整理 | `test_organize_default_mapping` | 使用默认映射整理文件 |
| 统计 | `test_size_stats_count` | 文件数量统计正确 |
| 统计 | `test_size_stats_by_type` | 按类型统计正确 |

#### 示例测试代码

```python
import pytest
from pathlib import Path
from src.file_tool import FileTool


def test_list_files_basic(tmp_path):
    """测试列出目录"""
    # 创建测试文件
    (tmp_path / "file1.txt").write_text("hello")
    (tmp_path / "file2.py").write_text("print('hi')")
    (tmp_path / "subdir").mkdir()
    
    tool = FileTool(str(tmp_path))
    files = tool.list_files()
    
    assert len(files) == 3  # 2 文件 + 1 目录
    names = [f['name'] for f in files]
    assert "file1.txt" in names
    assert "file2.py" in names
    assert "subdir" in names


def test_batch_rename_prefix(tmp_path):
    """测试批量添加前缀"""
    (tmp_path / "report_01.txt").write_text("a")
    (tmp_path / "report_02.txt").write_text("b")
    (tmp_path / "other.py").write_text("c")
    
    tool = FileTool(str(tmp_path))
    result = tool.batch_rename("report_*.txt", prefix="2024_")
    
    assert len(result['success']) == 2
    assert (tmp_path / "2024_report_01.txt").exists()
    assert (tmp_path / "2024_report_02.txt").exists()
    assert (tmp_path / "other.py").exists()  # 不匹配的文件不变


def test_batch_rename_dry_run(tmp_path):
    """测试预览模式"""
    (tmp_path / "file.txt").write_text("content")
    
    tool = FileTool(str(tmp_path))
    result = tool.batch_rename("*.txt", prefix="new_", dry_run=True)
    
    # 预览模式应返回结果但不实际重命名
    assert len(result['success']) == 1
    assert (tmp_path / "file.txt").exists()  # 原文件仍在
    assert not (tmp_path / "new_file.txt").exists()  # 新文件未创建
```

### Edge 测试（5 分）

| 测试类别 | 测试名称 | 说明 | AI 常见遗漏 |
|---------|---------|------|-------------|
| 隐藏文件 | `test_hidden_files_default` | 默认不列出隐藏文件 | 不区分隐藏文件 |
| 隐藏文件 | `test_hidden_files_include` | 可选列出隐藏文件 | 无配置选项 |
| 无扩展名 | `test_no_extension_file` | 正确处理无扩展名文件 | 无扩展名导致崩溃 |
| 重命名冲突 | `test_rename_conflict` | 冲突时不覆盖已有文件 | 直接覆盖 |
| 权限错误 | `test_permission_error` | 无权限文件跳过不崩溃 | 程序崩溃 |
| 符号链接 | `test_symlink_handling` | 正确处理符号链接 | 跟随链接导致问题 |
| 空目录 | `test_empty_directory` | 空目录不崩溃 | 空目录异常 |

#### 边界测试示例

```python
def test_hidden_files_default(tmp_path):
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


def test_rename_conflict(tmp_path):
    """重命名冲突时不应覆盖已有文件"""
    (tmp_path / "file.txt").write_text("original")
    (tmp_path / "new_file.txt").write_text("existing")
    
    tool = FileTool(str(tmp_path))
    result = tool.batch_rename("file.txt", prefix="new_")
    
    # 应该失败，而不是覆盖
    assert len(result['failed']) == 1 or len(result['skipped']) == 1
    
    # 原有文件内容不应改变
    assert (tmp_path / "new_file.txt").read_text() == "existing"


def test_no_extension_file(tmp_path):
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


def test_permission_error(tmp_path):
    """无权限文件应该跳过，不崩溃"""
    test_file = tmp_path / "readonly.txt"
    test_file.write_text("content")
    test_file.chmod(0o000)  # 移除所有权限
    
    tool = FileTool(str(tmp_path))
    
    try:
        result = tool.batch_rename("*.txt", prefix="new_")
        # 应该在 skipped 或 failed 中
        assert len(result.get('skipped', [])) > 0 or len(result.get('failed', [])) > 0
    finally:
        test_file.chmod(0o644)  # 恢复权限以便清理
```

---

## REPORT.md 要求（5 分）

### 设计理念

> 🎯 **本作业的核心问题**：文件操作是危险的。AI 可以快速生成代码，但谁来为代码的后果负责？
>
> 在 AI 时代，代码可以生成，Bug 可以修复——但**为结果负责的能力**，永远属于你。

### 必答内容

学生需要填写 `REPORT.md` 文件，包含以下部分：

```markdown
# 作业 3 反思报告

## 1. 安全意识

在测试批量重命名功能时，你是如何确保不会误操作重要文件的？

- 你使用了 dry_run 模式吗？
- 你是在哪个目录测试的？
- 如果代码有 bug，最坏情况会发生什么？

> [在此处回答]

## 2. 冲突处理的决策

当重命名遇到冲突（目标文件已存在）时，可能的处理方式有：
- A. 直接覆盖
- B. 跳过
- C. 添加数字后缀（如 file_1.txt）
- D. 抛出异常

你选择了哪种方式？为什么？这个决策有什么权衡？

> [在此处回答]

## 3. AI 代码审查

AI 生成的文件操作代码，你发现了哪些潜在风险？

- AI 初版代码是否考虑了权限问题？
- AI 初版代码是否考虑了冲突问题？
- 你做了哪些修改来让代码更安全？

> [在此处回答]

## 4. 责任思考

如果这个工具要给其他人使用，你会添加什么安全措施？

（提示：确认提示、日志记录、备份机制、撤销功能等）

> [在此处回答]
```

### 评分标准

| 评分维度 | 分值 | 说明 |
|---------|------|------|
| 安全意识 | 2 分 | 展示了谨慎测试的意识，理解操作风险 |
| 决策思考 | 1 分 | 对冲突处理有思考，不是随意选择 |
| 代码审查 | 1 分 | 发现并修复了 AI 代码的安全问题 |
| 责任思考 | 1 分 | 对"为结果负责"有自己的理解 |

---

## 仓库结构

```
assignment-03-files/
├── src/
│   ├── __init__.py
│   └── file_tool.py         # 学生在此实现
├── tests/
│   └── test_public.py       # 公开测试（学生可见）
├── test_files/               # 测试用文件目录
│   ├── documents/
│   ├── code/
│   ├── images/
│   └── mixed/
├── README.md
├── REPORT.md
└── requirements.txt
```

---

## 提供的测试目录结构

```
test_files/
├── documents/
│   ├── report_2023.docx
│   ├── report_2024.docx
│   └── notes.txt
├── code/
│   ├── main.py
│   ├── utils.py
│   └── .gitignore           # 隐藏文件
├── images/
│   ├── photo1.jpg
│   ├── photo2.png
│   └── screenshot.bmp
├── mixed/
│   ├── data.csv
│   ├── config.json
│   ├── README               # 无扩展名
│   └── .hidden_file         # 隐藏文件
└── empty/                    # 空目录
```

---

## Prompt 建议

```
请帮我实现一个文件批量处理工具类 FileTool，功能如下：

1. list_files: 列出目录下所有文件
   - 支持递归子目录
   - 支持选择是否包含隐藏文件（.开头的文件）
   - 返回文件信息（名称、路径、大小、类型、扩展名）

2. filter_by_extension: 按扩展名筛选文件

3. batch_rename: 批量重命名
   - 支持通配符匹配
   - 支持添加前缀和后缀
   - **重要**：必须有 dry_run 预览模式
   - **重要**：重命名冲突时不能覆盖已有文件

4. organize_by_type: 按文件类型整理到子目录

5. get_size_stats: 统计文件大小分布

安全要求：
- 所有操作都要处理权限错误
- 无扩展名文件不能导致崩溃
- 符号链接要特殊处理

请使用 pathlib 库，并添加完善的错误处理。
```

---

## 评分权重

```
┌─────────────────────────────────────┐
│  core 测试    ██████████ 10 分      │
│  edge 测试    █████░░░░░  5 分      │
│  REPORT.md    █████░░░░░  5 分      │
├─────────────────────────────────────┤
│  总分                     20 分     │
└─────────────────────────────────────┘
```

---

## 安全提示

> ⚠️ **重要**：本作业涉及文件系统操作，请：
> 
> 1. **始终在测试目录中操作**，不要在重要目录测试
> 2. **先用 dry_run 模式预览**，确认无误后再执行
> 3. **建议实现操作日志**，记录每次修改
> 4. **考虑撤销机制**，保留原文件名的映射

这不仅是技术要求，更是**对自己代码负责**的体现。

---

## 常见问题 FAQ

**Q: 隐藏文件的定义是什么？**  
A: 以 `.` 开头的文件或目录，如 `.gitignore`、`.env`。

**Q: 无扩展名文件怎么处理？**  
A: `extension` 字段返回空字符串 `''`，不应导致任何异常。

**Q: 重命名冲突的推荐处理方式？**  
A: 推荐"跳过并报告"，让用户决定。也可以添加数字后缀。绝不应该静默覆盖。

**Q: dry_run 模式必须实现吗？**  
A: 强烈建议实现。这是防止误操作的关键功能，也是 Edge 测试的一部分。

---

## 关键知识点

- **pathlib**：现代 Python 路径处理方式（优于 os.path）
- **glob 模式**：文件名匹配（`*.txt`、`report_*.csv`）
- **异常处理**：`PermissionError`、`FileExistsError`、`FileNotFoundError`
- **防御式编程**：预判可能的错误情况
- **dry_run 模式**：预览-确认-执行的安全模式
