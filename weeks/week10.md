# 第10周：数据可视化

> **课时**：2课时 | **阶段**：数据处理与可视化实战

## 🎯 学习目标

- 理解可视化的目的和原则
- 掌握 Matplotlib 和 Seaborn 基本用法
- 学会选择合适的图表类型

---

## 📚 课程内容

### 1. 可视化的目的：从数据到洞见（15分钟）

**为什么要可视化？**
- 发现数据中的模式和趋势
- 比较不同类别或时间段
- 发现异常值和离群点
- 向他人传达发现

**好的可视化原则**：
- 简洁明了
- 突出重点
- 避免误导
- 适合受众

### 2. 图表选择指南（20分钟）

| 目的 | 推荐图表 | 示例场景 |
|-----|---------|---------|
| 比较数值 | 柱状图 | 各班平均分对比 |
| 展示趋势 | 折线图 | 月度销售额变化 |
| 查看分布 | 直方图、箱线图 | 成绩分布情况 |
| 展示比例 | 饼图（慎用） | 各品类占比 |
| 探索关系 | 散点图 | 身高体重关系 |
| 展示相关性 | 热力图 | 变量相关性矩阵 |

### 3. Matplotlib 基础（30分钟）

**基本绑图**
```python
import matplotlib.pyplot as plt

# 折线图
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.title('销售趋势')
plt.xlabel('季度')
plt.ylabel('销售额(万)')
plt.show()

# 柱状图
plt.bar(['A班', 'B班', 'C班'], [85, 78, 92])
plt.title('各班平均分')
plt.show()

# 直方图
plt.hist(scores, bins=10)
plt.title('成绩分布')
plt.show()
```

**中文显示**
```python
import matplotlib.pyplot as plt

# 方法1：使用系统中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac
plt.rcParams['axes.unicode_minus'] = False
```

**多图布局**
```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(x, y1)
axes[0].set_title('图1')

axes[1].plot(x, y2)
axes[1].set_title('图2')

plt.tight_layout()
plt.show()
```

### 4. Seaborn 快速上手（25分钟）

**Seaborn = 更漂亮的 Matplotlib**

```python
import seaborn as sns

# 设置主题
sns.set_theme(style="whitegrid")

# 柱状图（自动统计）
sns.barplot(data=df, x='class', y='score')

# 箱线图
sns.boxplot(data=df, x='class', y='score')

# 热力图（相关性）
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')

# 散点图（带回归线）
sns.regplot(data=df, x='study_hours', y='score')
```

### 5. 实战：创建可视化报告（30分钟）

**任务**：为成绩数据创建分析报告

**包含图表**：
1. 各班平均分柱状图
2. 成绩分布直方图
3. 各班成绩箱线图
4. 趋势折线图（按月）

**代码框架**：
```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 图1：平均分对比
axes[0, 0].bar(...)

# 图2：成绩分布
axes[0, 1].hist(...)

# 图3：箱线图
sns.boxplot(..., ax=axes[1, 0])

# 图4：趋势
axes[1, 1].plot(...)

plt.suptitle('学生成绩分析报告', fontsize=16)
plt.tight_layout()
plt.savefig('report.png', dpi=300)
```

---

## 📝 课后作业

### 提交作业 4：数据可视化仪表板

**本周完成并提交**：
1. 通过所有测试用例（Core + Edge）
2. 完成 REPORT.md：
   - 你从数据中发现了什么有趣的规律？（2分）
   - AI 生成的图表有什么问题？你如何改进的？（2分）
   - 展示 2 个你和 AI 的对话迭代过程（2分）

**提交截止**：本周日

---

## 💡 教学提示

- 强调"可视化是讲故事"，不是为了画图而画图
- 让学生体验中文显示的坑，以及如何解决
- 鼓励学生用 AI 调整图表细节（颜色、标签、布局）
