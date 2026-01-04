# 第6周：文件操作与外部数据

> **课时**：2课时 | **阶段**：人机协同编程基础

## 🎯 学习目标

- 掌握文件读写操作（文本、CSV、JSON）
- 学会用 AI 处理文件路径问题
- 培养自动化脚本思维

---

## 📚 课程内容

### 1. 文件读写基础（30分钟）

**文本文件**
```python
# 读取
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()        # 读取全部
    # 或
    lines = f.readlines()     # 读取为行列表

# 写入
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("Hello, World!\n")
    f.writelines(["Line 1\n", "Line 2\n"])
```

**CSV 文件**
```python
import csv

# 读取
with open('grades.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['score'])

# 写入
with open('output.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'score'])
    writer.writeheader()
    writer.writerow({'name': '张三', 'score': 85})
```

**常见问题**：
- 编码问题：始终使用 `encoding='utf-8'`
- 路径问题：使用 `pathlib` 或 `os.path`

### 2. Prompt 技巧：文件路径处理（20分钟）

**常见路径问题**：
- Windows 路径 `C:\Users\xxx` vs Unix 路径 `/home/xxx`
- 相对路径 vs 绝对路径
- 文件不存在的处理

**Prompt 示例**：
```
写一个函数 read_file_safe(filepath)：
- 读取文件内容
- 自动处理 UTF-8 和 GBK 编码
- 如果文件不存在，返回 None 而不是报错
- 支持 Windows 和 Mac/Linux 路径
```

**pathlib 推荐用法**：
```python
from pathlib import Path

# 跨平台路径处理
data_dir = Path('data')
file_path = data_dir / 'grades.csv'  # 自动处理路径分隔符

if file_path.exists():
    content = file_path.read_text(encoding='utf-8')
```

### 3. 实战：批量处理文件（40分钟）

**场景**：整理下载文件夹

**需求**：
1. 列出目录下所有文件
2. 按扩展名分类（图片、文档、视频等）
3. 移动到对应子目录
4. 生成整理报告

**分步 Prompt**：

```
# 步骤1
写一个函数 list_files(directory)：
- 列出目录下所有文件（不包括子目录）
- 返回文件路径列表
```

```
# 步骤2
写一个函数 get_file_category(filename)：
- 根据扩展名返回类别
- .jpg/.png/.gif → "images"
- .doc/.docx/.pdf → "documents"  
- .mp4/.avi → "videos"
- 其他 → "others"
```

```
# 步骤3
写一个函数 organize_files(source_dir)：
- 遍历源目录所有文件
- 按类别移动到对应子目录
- 处理重名文件（添加数字后缀）
- 返回整理报告
```

### 4. 自动化脚本思维（20分钟）

**什么任务适合自动化？**
- 重复性高
- 规则明确
- 人工容易出错

**示例场景**：
- 批量重命名照片（按日期）
- 整理下载文件
- 合并多个 CSV 文件
- 批量处理 Excel 数据

**讨论**：你日常有什么重复性工作可以用 Python 自动化？

---

## 📝 课后作业

### 开始作业 3：文件批量处理工具

**本周任务**：
1. 实现核心功能：
   - `list_dir(path)` - 列出目录内容
   - `filter_by_ext(files, ext)` - 按扩展名筛选
   - `batch_rename(files, prefix)` - 批量重命名

2. 测试 Core 用例

**注意**：本周专注于 Core 测试，下周处理 Edge 情况

---

## 🔧 代码模板

```python
from pathlib import Path

def list_files(directory):
    """列出目录下所有文件
    
    Args:
        directory: 目录路径
        
    Returns:
        文件路径列表
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    return [f for f in dir_path.iterdir() if f.is_file()]

def organize_by_type(source_dir, target_dir):
    """按类型整理文件
    
    Args:
        source_dir: 源目录
        target_dir: 目标目录
        
    Returns:
        整理报告字典 {'images': 5, 'documents': 3, ...}
    """
    pass  # TODO: 用 AI 实现
```

---

## 💡 教学提示

- 强调 `with` 语句的重要性（自动关闭文件）
- 让学生在自己电脑上运行文件操作代码
- 提醒：操作文件要小心，先用 `--dry-run` 预览
