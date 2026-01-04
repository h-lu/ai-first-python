# 第8周：数据科学工具链

> **课时**：2课时 | **阶段**：数据处理与可视化实战

## 🎯 学习目标

- 认识 Python 数据科学生态系统
- 学会用 AI 快速上手 NumPy、Pandas
- 掌握 Jupyter Notebook 交互式编程

---

## 📚 课程内容

### 1. Python 数据科学生态速览（20分钟）

**核心库**：

| 库 | 用途 | 一句话说明 |
|---|------|----------|
| **NumPy** | 数值计算 | 高效的数组运算 |
| **Pandas** | 数据处理 | Excel 的 Python 版本 |
| **Matplotlib** | 基础绑图 | 生成各种图表 |
| **Seaborn** | 统计可视化 | 更漂亮的图表 |

**安装**：
```bash
pip install numpy pandas matplotlib seaborn jupyter
```

### 2. 不需要背 API：用 AI 查询和生成代码（30分钟）

**重要理念**：数据科学库的 API 非常多，不可能背下来

**Prompt 示例**：
```
我有一个 Pandas DataFrame，包含列 ['name', 'age', 'score']：
- 筛选出 score > 80 的行
- 按 age 分组，计算平均 score
- 结果按平均分降序排列
```

```
用 Matplotlib 画一个柱状图：
- X轴：['A班', 'B班', 'C班']
- Y轴：[85, 78, 92]
- 添加标题"各班平均分"
- 柱子颜色用蓝色
```

**课堂演示**：让 AI 生成代码，逐行解释

### 3. Jupyter Notebook 交互式编程（30分钟）

**启动**：
```bash
jupyter notebook
```

**基本操作**：
- 创建新 Notebook
- Cell 类型：Code / Markdown
- 运行 Cell：Shift+Enter
- 添加/删除 Cell

**为什么用 Notebook**：
- 边写边运行，即时看结果
- 代码和说明混排
- 可视化直接显示
- 适合数据探索

### 4. 实战：加载并探索真实数据集（40分钟）

**数据集**：学生成绩数据（`grades.csv`）

**探索流程**：

```python
import pandas as pd

# 1. 加载数据
df = pd.read_csv('grades.csv')

# 2. 初步了解
print(df.head())        # 前5行
print(df.info())        # 数据类型
print(df.describe())    # 统计摘要

# 3. 基本分析
print(df['score'].mean())                    # 平均分
print(df.groupby('class')['score'].mean())   # 按班级分组

# 4. 简单可视化
import matplotlib.pyplot as plt
df['score'].hist()
plt.title('成绩分布')
plt.show()
```

**课堂任务**：
1. 找出最高分和最低分的学生
2. 计算各班的及格率
3. 画出各班平均分的柱状图

---

## 📝 课后作业

### 开始作业 4：数据可视化仪表板

**本周任务**：
1. 下载指定数据集（任选其一）：
   - 中国城市空气质量数据
   - 电商销售数据
   - 学校考试成绩汇总

2. 用 Jupyter Notebook 进行数据探索：
   - 加载数据
   - 查看基本信息
   - 计算基本统计量
   - 画 1-2 个简单图表

3. 记录探索过程

---

## 🔧 Pandas 常用操作速查

```python
# 读取数据
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')

# 查看数据
df.head()           # 前5行
df.tail()           # 后5行
df.shape            # 行数和列数
df.columns          # 列名
df.dtypes           # 数据类型

# 选择数据
df['column']        # 选择一列
df[['col1', 'col2']] # 选择多列
df[df['col'] > 10]  # 条件筛选

# 统计
df.describe()       # 描述统计
df['col'].mean()    # 平均值
df.groupby('col').mean()  # 分组统计

# 缺失值
df.isna().sum()     # 统计缺失值
df.dropna()         # 删除缺失值
df.fillna(0)        # 填充缺失值
```

---

## 💡 教学提示

- 重点是"会用"而非"背 API"
- 鼓励学生遇到不会的就问 AI
- Jupyter 是数据探索的好工具，后续作业可以在其中完成
- 本周侧重"动手探索"，下周才深入分析
