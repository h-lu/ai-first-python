# 第9周：数据清洗与预处理

> **课时**：2课时 | **阶段**：数据处理与可视化实战

## 🎯 学习目标

- 理解"脏数据"的常见问题
- 掌握 Pandas 数据清洗基本操作
- 学会用 AI 生成清洗代码

---

## 📚 课程内容

### 1. 真实数据的"脏"（25分钟）

**常见数据问题**：

| 问题类型 | 示例 | 后果 |
|---------|------|------|
| **缺失值** | 某些学生没有成绩 | 计算平均分出错 |
| **异常值** | 成绩 = -10 或 999 | 统计结果失真 |
| **格式不一致** | "张三" vs "张 三" | 无法正确匹配 |
| **重复数据** | 同一学生录入两次 | 统计重复计算 |
| **类型错误** | 成绩存为字符串 "85" | 无法做数学运算 |

**案例展示**：展示一份"脏"数据
```
学号,姓名,成绩
001,张三,85
002,李四,
003,王五,92
003,王五,95
004,赵六,-10
005,钱七,excellent
```

### 2. Pandas 数据清洗（40分钟）

**缺失值处理**
```python
import pandas as pd

# 检测缺失值
df.isna().sum()                    # 统计各列缺失值数量

# 删除缺失值
df.dropna()                        # 删除含缺失值的行
df.dropna(subset=['score'])        # 只看特定列

# 填充缺失值
df.fillna(0)                       # 填充0
df['score'].fillna(df['score'].mean())  # 填充平均值
```

**异常值处理**
```python
# 发现异常值
df[df['score'] < 0]                # 负数
df[df['score'] > 100]              # 超过100

# IQR 方法检测离群点
Q1 = df['score'].quantile(0.25)
Q3 = df['score'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['score'] < Q1 - 1.5*IQR) | (df['score'] > Q3 + 1.5*IQR)]
```

**格式统一**
```python
# 去除空格
df['name'] = df['name'].str.strip()

# 统一大小写
df['name'] = df['name'].str.lower()

# 类型转换
df['score'] = pd.to_numeric(df['score'], errors='coerce')  # 无法转换的变成 NaN
```

**去重**
```python
# 检测重复
df.duplicated()
df.duplicated(subset=['id'])       # 按学号检测

# 删除重复
df.drop_duplicates()
df.drop_duplicates(subset=['id'], keep='last')  # 保留最后一条
```

### 3. 用 AI 生成清洗代码（25分钟）

**Prompt 示例**：
```
我有一份成绩数据 DataFrame，包含列 ['学号', '姓名', '成绩']，存在以下问题：
1. 部分成绩为空
2. 有些成绩是负数或大于100
3. 同一学号可能有多条记录

请帮我清洗数据：
- 空成绩用0填充
- 删除无效成绩（<0 或 >100）
- 按学号去重，保留最高成绩
```

### 4. 实战：清洗并准备分析用数据（30分钟）

**课堂项目**：清洗电商销售数据

**数据问题**：
- 日期格式不统一
- 价格列有缺失
- 存在重复订单
- 部分金额为负数

**清洗流程**：
```python
# 1. 加载数据
df = pd.read_csv('sales.csv')

# 2. 检查问题
print(df.info())
print(df.isna().sum())

# 3. 处理缺失值
df['price'].fillna(df['price'].median(), inplace=True)

# 4. 处理异常值
df = df[df['price'] > 0]

# 5. 去重
df.drop_duplicates(subset=['order_id'], inplace=True)

# 6. 保存清洗后数据
df.to_csv('sales_cleaned.csv', index=False)
```

---

## 📝 课后作业

### 继续作业 4：数据可视化仪表板

**本周任务**：
1. 清洗你的数据集：
   - 处理缺失值
   - 处理异常值
   - 格式统一

2. 通过 Core 测试用例：
   - `test_viz_load_data`
   - `test_viz_basic_stats`

3. 记录清洗过程

---

## 💡 教学提示

- 用真实的脏数据让学生体验"数据清洗的必要性"
- 强调：清洗前要先理解数据，不能盲目删除
- 清洗策略要记录，便于复现和审核
