# 第5周：数据结构直觉

> **课时**：2课时 | **阶段**：人机协同编程基础

## 🎯 学习目标

- 建立对常用数据结构的直觉
- 知道什么时候用列表、字典、集合
- 学会处理 JSON 格式数据

---

## 📚 课程内容

### 1. 数据结构选择：什么时候用什么？（30分钟）

| 数据结构 | 特点 | 适用场景 | 示例 |
|---------|------|---------|------|
| **列表 list** | 有序、可重复 | 一组同类数据 | 成绩：`[85, 90, 75]` |
| **字典 dict** | 键值对 | 有名字的数据 | 学生：`{"name": "张三", "age": 20}` |
| **集合 set** | 无序、不重复 | 去重、成员判断 | 标签：`{"Python", "AI"}` |
| **元组 tuple** | 有序、不可变 | 固定的组合数据 | 坐标：`(x, y)` |

**选择决策树**：
```
需要存储数据？
├── 需要用名字查找 → 字典
├── 需要去重 → 集合
├── 数据固定不变 → 元组
└── 其他情况 → 列表
```

### 2. 让 AI 帮你选择数据结构（20分钟）

**Prompt 示例**：
```
我需要存储以下数据，帮我选择合适的数据结构：
- 10个学生的姓名、学号、成绩
- 需要能按学号查找
- 需要能按成绩排序

请解释为什么选择这种结构。
```

**课堂讨论**：让学生描述自己的数据需求，讨论用什么结构

### 3. JSON 数据处理实战（30分钟）

**JSON 是什么**：一种通用的数据交换格式

```json
{
  "students": [
    {"id": "001", "name": "张三", "scores": [85, 90, 78]},
    {"id": "002", "name": "李四", "scores": [92, 88, 95]}
  ],
  "class_name": "计算机1班"
}
```

**Python 处理 JSON**：
```python
import json

# 读取 JSON 文件
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 访问数据
for student in data['students']:
    print(f"{student['name']}: {sum(student['scores'])/len(student['scores']):.1f}")

# 写入 JSON 文件
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 4. 实战：处理真实学生信息数据（40分钟）

**课堂项目**：通讯录管理

**需求**：
- 存储：姓名、手机、邮箱、分组
- 功能：添加、查找、修改、删除
- 持久化：保存到 JSON 文件

**分步实现**：

1. **设计数据结构**（让学生先思考）
```python
# 方案1：列表套字典
contacts = [
    {"name": "张三", "phone": "13800138001", "email": "zhang@example.com", "group": "同学"},
    {"name": "李四", "phone": "13900139001", "email": "li@example.com", "group": "同事"}
]

# 方案2：字典套字典（按手机号索引）
contacts = {
    "13800138001": {"name": "张三", "email": "zhang@example.com", "group": "同学"},
    "13900139001": {"name": "李四", "email": "li@example.com", "group": "同事"}
}
```

2. **用 AI 生成功能函数**
```
写一个函数 add_contact(contacts, name, phone, email, group)：
- 添加新联系人到通讯录
- 如果手机号已存在，返回False
- 成功添加返回True
```

---

## 📝 课后作业

### 继续作业 2：成绩统计分析器

**本周任务**：
1. 处理 Edge 测试中的边界情况：
   - `test_grade_missing_value`: 缺失成绩处理
   - `test_grade_invalid_score`: 非法分数检测
   - `test_grade_duplicate_id`: 重复学号检测

2. 完成 REPORT.md

**提交截止**：本周日

---

## 🔧 练习题

**练习 1**：选择数据结构

> 需要存储一个图书馆的书籍信息（书名、ISBN、作者、借阅状态），需要能按 ISBN 快速查找，应该用什么数据结构？

**练习 2**：JSON 处理

给定 JSON 文件：
```json
{
  "grades": [
    {"name": "张三", "python": 85, "math": 90},
    {"name": "李四", "python": 92, "math": 78}
  ]
}
```

写一个程序：计算每个学生的平均分，输出到新 JSON 文件。

---

## 💡 教学提示

- 重点培养"直觉"而非"背诵"
- 用真实场景来解释数据结构选择
- JSON 是后续作业（API、文件处理）的基础，要确保学生理解
