# 第7周：错误处理与健壮性

> **课时**：2课时 | **阶段**：人机协同编程基础

## 🎯 学习目标

- 理解程序为什么会崩溃
- 掌握异常处理的基本用法
- 学会用 AI 预判和处理潜在错误

---

## 📚 课程内容

### 1. 程序为什么会崩溃？（25分钟）

**常见错误类型**：

| 错误类型 | 原因 | 示例 |
|---------|------|------|
| `FileNotFoundError` | 文件不存在 | `open('不存在.txt')` |
| `ZeroDivisionError` | 除以零 | `10 / 0` |
| `TypeError` | 类型不匹配 | `"hello" + 5` |
| `KeyError` | 字典键不存在 | `d['不存在的键']` |
| `IndexError` | 列表越界 | `[1,2,3][10]` |
| `ValueError` | 值不合法 | `int("abc")` |

**案例分析**：
```python
def calculate_average(scores):
    total = sum(scores)
    return total / len(scores)  # 如果 scores 是空列表？

calculate_average([])  # ZeroDivisionError!
```

### 2. 异常处理：try-except（30分钟）

**基本语法**：
```python
try:
    # 可能出错的代码
    result = risky_operation()
except SomeError as e:
    # 出错时的处理
    print(f"出错了: {e}")
else:
    # 没出错时执行
    print("成功!")
finally:
    # 无论如何都执行（清理工作）
    cleanup()
```

**实际应用**：
```python
def safe_read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件不存在: {filepath}")
        return None
    except UnicodeDecodeError:
        # 尝试其他编码
        with open(filepath, 'r', encoding='gbk') as f:
            return f.read()

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
```

### 3. 让 AI 预判潜在错误（25分钟）

**Prompt 技巧**：
```
审查这段代码，列出所有可能发生的错误，并添加适当的异常处理：

[粘贴代码]
```

```
这个函数需要处理以下边界情况：
- 空输入
- 无效输入
- 文件不存在
请帮我添加错误处理代码
```

**课堂练习**：
```python
# 让 AI 帮你改进这段代码
def get_student_score(students, student_id):
    return students[student_id]['score']

# 可能的错误：
# 1. students 是 None
# 2. student_id 不存在
# 3. 学生没有 score 字段
```

### 4. 防御式编程思维（20分钟）

**原则**：
1. **假设输入可能有问题** - 总是验证
2. **快速失败** - 早发现早报错
3. **明确错误信息** - 帮助调试
4. **合理的默认值** - 而不是崩溃

**示例**：
```python
def process_score(score):
    # 防御式：先验证输入
    if score is None:
        raise ValueError("分数不能为None")
    if not isinstance(score, (int, float)):
        raise TypeError(f"分数必须是数字，收到 {type(score)}")
    if score < 0 or score > 100:
        raise ValueError(f"分数必须在0-100之间，收到 {score}")
    
    # 正常处理
    return score >= 60
```

---

## 📝 课后作业

### 完成作业 3：文件批量处理工具

**本周任务**：处理 Edge 测试
- `test_file_hidden_files`: 隐藏文件处理
- `test_file_no_extension`: 无扩展名文件
- `test_file_duplicate_name`: 重命名冲突处理
- `test_file_permission_error`: 无权限文件跳过

**REPORT.md 要求**：
- 展示你的 Prompt 如何描述"重命名冲突"这个需求
- 对比 AI 第一次生成的代码和你最终版本的差异

**提交截止**：本周日

---

## 🔧 代码模板

```python
def safe_batch_rename(directory, prefix):
    """安全的批量重命名
    
    处理以下边界情况：
    - 目录不存在
    - 无权限访问
    - 重名冲突
    """
    from pathlib import Path
    
    dir_path = Path(directory)
    
    # 验证目录存在
    if not dir_path.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")
    
    results = {'success': [], 'failed': []}
    
    for file in dir_path.iterdir():
        if not file.is_file():
            continue
            
        try:
            new_name = f"{prefix}_{file.name}"
            new_path = file.parent / new_name
            
            # 处理重名
            counter = 1
            while new_path.exists():
                stem = file.stem
                suffix = file.suffix
                new_name = f"{prefix}_{stem}_{counter}{suffix}"
                new_path = file.parent / new_name
                counter += 1
            
            file.rename(new_path)
            results['success'].append(str(file))
            
        except PermissionError:
            results['failed'].append((str(file), "权限不足"))
        except Exception as e:
            results['failed'].append((str(file), str(e)))
    
    return results
```

---

## 💡 教学提示

- 用真实的错误场景让学生体验"崩溃"
- 强调：好的程序是"优雅地处理错误"而不是"不出错"
- 让学生养成习惯：写完代码问 AI "这段代码可能有什么问题"
