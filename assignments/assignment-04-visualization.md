# 作业 4：数据可视化仪表板

> 📅 **布置周期**：第 8-10 周  
> 💯 **总分**：20 分  
> 🎯 **对应章节**：第 8-10 章（数据工具、清洗、可视化）

## 任务概述

分析公开数据集，生成可视化报告。这是数据处理阶段的综合作业，需要综合运用 Pandas 和 Matplotlib 技能。

**🎯 本作业的核心问题**：AI 可以生成图表，但**判断什么图表值得做**、**从数据中发现什么规律有意义**——这些能力属于你。

---

## 学习目标

完成本作业后，学生应能够：

1. ✅ 使用 Pandas 加载和清洗真实数据
2. ✅ 进行基本的探索性数据分析
3. ✅ 创建有意义的数据可视化
4. ✅ **从数据中发现并表述规律**——不只是画图
5. ✅ **理解用户真实需求**——可视化是为了传达信息

---

## 数据集选项

学生可选择以下数据集之一：

### 选项 A：中国城市空气质量数据

```
air_quality.csv
├── 字段：城市, 日期, AQI, PM2.5, PM10, SO2, NO2, CO, O3
├── 行数：约 10000 行
└── 特点：时间序列, 有缺失值, 可分析趋势和城市对比
```

### 选项 B：电商销售数据

```
ecommerce_sales.csv
├── 字段：订单ID, 日期, 商品类别, 商品名, 价格, 数量, 客户城市
├── 行数：约 5000 行
└── 特点：多维分析, 有异常值, 可分析销售趋势和热门品类
```

### 选项 C：学校考试成绩汇总

```
exam_results.csv
├── 字段：学号, 姓名, 班级, 语文, 数学, 英语, 物理, 化学
├── 行数：约 500 行
└── 特点：多科目, 有缺失, 可分析成绩分布和科目相关性
```

---

## 功能需求

### 类接口设计

```python
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Optional

class DataDashboard:
    """数据可视化仪表板"""
    
    def __init__(self, filepath: str):
        """
        初始化并加载数据
        
        Args:
            filepath: 数据文件路径（CSV）
        """
        self.df: pd.DataFrame = None
        self.filepath = filepath
        self.load_data(filepath)
    
    def load_data(self, filepath: str) -> bool:
        """
        加载并初步清洗数据
        
        处理要求：
        - 自动检测编码（UTF-8 或 GBK）
        - 记录缺失值情况
        - 转换数据类型（日期列转为 datetime）
        
        Returns:
            bool: 是否加载成功
        """
        pass
    
    def get_basic_stats(self) -> Dict:
        """
        计算基本统计量
        
        Returns:
            {
                'row_count': 1000,
                'column_count': 10,
                'columns': ['col1', 'col2', ...],
                'missing_count': {'col1': 5, 'col2': 10, ...},
                'numeric_summary': {
                    'col1': {'mean': 50, 'std': 10, 'min': 0, 'max': 100},
                    ...
                }
            }
        """
        pass
    
    def create_bar_chart(self, x_col: str, y_col: str, 
                         title: Optional[str] = None,
                         aggfunc: str = 'mean',
                         save_path: Optional[str] = None) -> None:
        """
        生成柱状图
        
        Args:
            x_col: X 轴列名（分类变量）
            y_col: Y 轴列名（数值变量）
            title: 图表标题
            aggfunc: 聚合函数（'mean', 'sum', 'count'）
            save_path: 保存路径，如果为 None 则显示图表
        """
        pass
    
    def create_line_chart(self, x_col: str, y_col: str,
                          title: Optional[str] = None,
                          save_path: Optional[str] = None) -> None:
        """
        生成折线趋势图
        
        Args:
            x_col: X 轴列名（通常是时间）
            y_col: Y 轴列名
            title: 图表标题
            save_path: 保存路径
        """
        pass
    
    def create_heatmap(self, columns: Optional[List[str]] = None,
                       title: Optional[str] = None,
                       save_path: Optional[str] = None) -> None:
        """
        生成相关性热图
        
        Args:
            columns: 要计算相关性的列，None 表示所有数值列
            title: 图表标题
            save_path: 保存路径
        """
        pass
    
    def create_distribution(self, column: str,
                            bins: int = 20,
                            title: Optional[str] = None,
                            save_path: Optional[str] = None) -> None:
        """
        生成分布直方图
        
        Args:
            column: 列名
            bins: 分箱数量
            title: 图表标题
            save_path: 保存路径
        """
        pass
    
    def generate_report(self, output_dir: str) -> Dict:
        """
        生成完整分析报告（多个图表）
        
        Args:
            output_dir: 输出目录
            
        Returns:
            {'generated_files': ['bar.png', 'line.png', ...]}
        """
        pass
```

---

## 测试用例设计

### Core 测试（10 分）

| 测试类别 | 测试名称 | 说明 |
|---------|---------|------|
| 数据加载 | `test_load_csv_success` | 成功加载 CSV 文件 |
| 数据加载 | `test_load_csv_dataframe` | 返回有效的 DataFrame |
| 统计 | `test_basic_stats_structure` | 统计结果包含必要字段 |
| 统计 | `test_basic_stats_values` | 统计值计算正确 |
| 柱状图 | `test_bar_chart_create` | 成功生成柱状图 |
| 柱状图 | `test_bar_chart_save` | 成功保存为 PNG |
| 折线图 | `test_line_chart_create` | 成功生成折线图 |
| 折线图 | `test_line_chart_save` | 成功保存为 PNG |
| 热图 | `test_heatmap_create` | 成功生成相关性热图 |
| 报告 | `test_generate_report` | 成功生成多个图表 |

#### 示例测试代码

```python
import pytest
from pathlib import Path
import pandas as pd
from src.dashboard import DataDashboard


@pytest.fixture
def sample_csv(tmp_path):
    """创建测试数据"""
    content = """日期,城市,AQI,PM2.5
2024-01-01,北京,120,80
2024-01-01,上海,85,55
2024-01-02,北京,100,65
2024-01-02,上海,90,60
2024-01-03,北京,150,100
2024-01-03,上海,75,50"""
    p = tmp_path / "test_data.csv"
    p.write_text(content, encoding='utf-8')
    return str(p)


def test_load_csv_success(sample_csv):
    """测试数据加载"""
    dashboard = DataDashboard(sample_csv)
    
    assert dashboard.df is not None
    assert len(dashboard.df) == 6
    assert isinstance(dashboard.df, pd.DataFrame)


def test_basic_stats_structure(sample_csv):
    """测试基本统计结构"""
    dashboard = DataDashboard(sample_csv)
    stats = dashboard.get_basic_stats()
    
    assert 'row_count' in stats
    assert 'column_count' in stats
    assert 'missing_count' in stats
    assert stats['row_count'] == 6
    assert stats['column_count'] == 4


def test_bar_chart_save(sample_csv, tmp_path):
    """测试柱状图保存"""
    dashboard = DataDashboard(sample_csv)
    
    output_path = tmp_path / "bar_chart.png"
    dashboard.create_bar_chart(
        x_col='城市',
        y_col='AQI',
        title='各城市平均AQI',
        save_path=str(output_path)
    )
    
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_generate_report(sample_csv, tmp_path):
    """测试报告生成"""
    dashboard = DataDashboard(sample_csv)
    output_dir = tmp_path / "report"
    output_dir.mkdir()
    
    result = dashboard.generate_report(str(output_dir))
    
    assert 'generated_files' in result
    assert len(result['generated_files']) > 0
```

### Edge 测试（4 分）

| 测试类别 | 测试名称 | 说明 | AI 常见遗漏 |
|---------|---------|------|-------------|
| 缺失值 | `test_missing_data_chart` | 缺失值不导致图表错误 | 缺失值导致绘图崩溃 |
| 中文 | `test_chinese_labels` | 中文标签正确显示 | 中文乱码 |
| 异常值 | `test_outlier_handling` | 异常值不完全破坏图表 | 坐标轴范围异常 |
| 空数据 | `test_empty_column` | 空列不导致崩溃 | 除零错误或空图 |

#### 边界测试示例

```python
def test_missing_data_chart(tmp_path):
    """缺失值应该被正确处理"""
    content = """日期,值
2024-01-01,100
2024-01-02,
2024-01-03,150
2024-01-04,
2024-01-05,200"""
    
    csv_file = tmp_path / "missing.csv"
    csv_file.write_text(content, encoding='utf-8')
    
    dashboard = DataDashboard(str(csv_file))
    
    # 生成折线图不应崩溃
    output = tmp_path / "chart.png"
    dashboard.create_line_chart('日期', '值', save_path=str(output))
    
    assert output.exists()


def test_chinese_labels(sample_csv, tmp_path):
    """中文标签应该正确显示"""
    dashboard = DataDashboard(sample_csv)
    
    output = tmp_path / "chinese_chart.png"
    dashboard.create_bar_chart(
        x_col='城市',
        y_col='AQI',
        title='各城市空气质量指数对比',
        save_path=str(output)
    )
    
    assert output.exists()
    
    # 验证图片可读
    from PIL import Image
    img = Image.open(output)
    assert img.size[0] > 0


def test_outlier_handling(tmp_path):
    """异常值不应该完全破坏图表"""
    content = """类别,值
A,100
B,150
C,10000
D,120"""  # C 是异常值
    
    csv_file = tmp_path / "outlier.csv"
    csv_file.write_text(content, encoding='utf-8')
    
    dashboard = DataDashboard(str(csv_file))
    output = tmp_path / "chart.png"
    
    # 生成柱状图
    dashboard.create_bar_chart('类别', '值', save_path=str(output))
    
    # 图表应该能正常生成
    assert output.exists()
```

---

## REPORT.md 要求（6 分）

### 设计理念

> 🎯 **本作业的核心问题**：AI 可以秒速生成图表代码，但**什么图表值得做**？**数据背后有什么故事**？
>
> 在 AI 时代，图表可以自动生成——但**判断什么值得做的能力**、**理解用户真实需求的能力**，永远属于你。

### 必答内容

学生需要填写 `REPORT.md` 文件，包含以下部分：

```markdown
# 作业 4 反思报告

## 1. 数据发现（重点，3分）

你从数据中发现了什么？不是"我画了什么图"，而是"我发现了什么"。

### 发现 1：[用一句话描述你的发现]

- **现象**：具体描述你观察到的现象
- **数据支撑**：用具体数字或图表说明
- **可能原因**：你对这个现象的解释或猜测
- **价值**：这个发现有什么用？谁会关心？

### 发现 2：[用一句话描述你的发现]

- **现象**：...
- **数据支撑**：...
- **可能原因**：...
- **价值**：...

> [至少写 2 个发现]

## 2. 图表选择的思考

你选择了哪些类型的图表？为什么？

- 为什么用柱状图而不是饼图？
- 为什么用折线图而不是散点图？
- 你放弃了哪些图表？为什么？

> [在此处回答]

## 3. AI 图表的问题

AI 生成的图表代码，有什么问题？

### 问题 1：[问题描述]
- AI 原代码的行为：
- 问题所在：
- 你的修改：

### 问题 2：[问题描述]
- ...

> [至少找出 1 个问题]

## 4. 从"画图"到"讲故事"

如果你要用这些图表给领导/客户做汇报，你会如何组织？

- 先展示什么？后展示什么？
- 每张图要传达什么信息？
- 哪些细节需要强调？

> [在此处回答]
```

### 评分标准

| 评分维度 | 分值 | 说明 |
|---------|------|------|
| 数据发现的深度 | 3 分 | 不是描述图表，而是发现规律，有数据支撑和思考 |
| 图表选择的思考 | 1 分 | 有选择理由，不是"AI 生成了这个" |
| AI 问题发现 | 1 分 | 发现并修复了实际问题 |
| 信息传达意识 | 1 分 | 理解可视化是为了沟通，不是为了完成作业 |

---

## 可视化要求

### 必须包含的图表

1. **柱状图**：类别对比（如：不同城市的 AQI 对比）
2. **折线图**：时间趋势（如：某城市 AQI 月度变化）
3. **至少一个额外图表**（热图、饼图、散点图、直方图等）

### 图表规范

- ✅ 有清晰的标题（说明图表展示什么）
- ✅ X/Y 轴有标签（带单位）
- ✅ 中文标签正确显示
- ✅ 图例清晰（如果有多系列）
- ✅ 颜色区分度好
- ✅ 保存为 PNG 格式（分辨率足够）

---

## 中文显示配置

```python
import matplotlib.pyplot as plt

# macOS
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Windows
# plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']

# Linux
# plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
```

---

## 仓库结构

```
assignment-04-visualization/
├── data/
│   ├── air_quality.csv       # 数据集选项 A
│   ├── ecommerce_sales.csv   # 数据集选项 B
│   └── exam_results.csv      # 数据集选项 C
├── src/
│   ├── __init__.py
│   └── dashboard.py          # 学生在此实现
├── output/                    # 生成的图表
│   ├── bar_chart.png
│   ├── line_chart.png
│   └── ...
├── tests/
│   └── test_public.py
├── README.md
├── REPORT.md
└── requirements.txt
```

---

## Prompt 建议

```
请帮我用 Pandas 和 Matplotlib 实现一个数据可视化仪表板类 DataDashboard：

1. load_data: 加载 CSV 数据
   - 处理 UTF-8 和 GBK 编码
   - 记录缺失值情况

2. get_basic_stats: 计算基本统计量
   - 行数、列数、缺失值统计
   - 数值列的均值、标准差、最大最小值

3. create_bar_chart: 生成柱状图
   - 支持自定义标题
   - 支持聚合函数（mean/sum/count）
   - 保存为 PNG

4. create_line_chart: 生成折线图

5. create_heatmap: 生成相关性热图

6. create_distribution: 生成分布直方图

7. generate_report: 生成完整报告（多个图表）

注意：
- 缺失值不能导致绘图崩溃
- 中文标签要正确显示（配置字体）
- 异常值不能完全破坏图表

数据集是空气质量数据，包含：城市、日期、AQI、PM2.5 等字段。
```

---

## 评分权重

```
┌─────────────────────────────────────┐
│  core 测试    ██████████ 10 分      │
│  edge 测试    ████░░░░░░  4 分      │
│  REPORT.md    ██████░░░░  6 分      │
├─────────────────────────────────────┤
│  总分                     20 分     │
└─────────────────────────────────────┘
```

---

## 常见问题 FAQ

**Q: 数据发现要写多少？**  
A: 至少 2 个有深度的发现。重点是"发现了什么"，而不是"画了什么图"。

**Q: 中文乱码怎么办？**  
A: 参考上面的字体配置代码。不同操作系统需要不同的字体。

**Q: 异常值要怎么处理？**  
A: 可以选择：过滤掉、用对数坐标、或在图表中标注。重点是图表仍然可读。

**Q: 可以用 Seaborn 吗？**  
A: 可以！Seaborn 是 Matplotlib 的高级封装，更适合统计图表。

---

## 关键知识点

- **Pandas**：数据加载、清洗、聚合、分组
- **Matplotlib**：基础绑图 API、样式配置、保存图片
- **数据分析思维**：从数据中发现规律，而不只是画图
- **可视化原则**：选择合适的图表类型，清晰传达信息
