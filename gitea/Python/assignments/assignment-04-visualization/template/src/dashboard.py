"""
数据可视化仪表板

你的任务是实现 DataDashboard 类，从 CSV 文件加载数据，进行分析并生成可视化报告。

功能要求：
1. 加载 CSV 数据（处理编码问题）
2. 计算基本统计量
3. 生成柱状图、折线图、热图等可视化
4. 生成完整分析报告

🎯 核心问题：AI 可以生成图表代码，但"什么图表值得做"、"数据背后有什么故事"——这些需要你来判断。

数据集选项：
- air_quality.csv: 空气质量数据（城市、日期、AQI、PM2.5 等）
- ecommerce_sales.csv: 电商销售数据
- exam_results.csv: 考试成绩数据

边界情况处理：
- 缺失值：不能导致绘图崩溃
- 中文标签：需要配置字体正确显示
- 异常值：不能完全破坏图表
- 空数据：空列不导致崩溃

中文字体配置提示：
```python
import matplotlib.pyplot as plt
# macOS
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# Windows
# plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
# Linux
# plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False
```

示例用法：
dashboard = DataDashboard("data/air_quality.csv")
stats = dashboard.get_basic_stats()
dashboard.create_bar_chart('城市', 'AQI', title='各城市平均AQI', save_path='bar.png')
dashboard.create_line_chart('日期', 'AQI', title='AQI变化趋势', save_path='line.png')
dashboard.generate_report('output/')
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Optional


class DataDashboard:
    """
    数据可视化仪表板
    
    从 CSV 文件加载数据，提供统计分析和可视化功能。
    """

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
        - 尝试转换日期列为 datetime
        
        Args:
            filepath: CSV 文件路径
            
        Returns:
            bool: 是否加载成功
            
        提示：
        - 先尝试 UTF-8，失败再尝试 GBK
        - 可以使用 pd.to_datetime 转换日期列
        """
        # TODO: 在此实现你的代码
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
            
        注意：
        - numeric_summary 只包含数值列
        - missing_count 包含所有列的缺失值数量
        """
        # TODO: 在此实现你的代码
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
            
        示例：
            dashboard.create_bar_chart('城市', 'AQI', title='各城市平均AQI')
            
        注意：
        - 需要配置中文字体
        - 缺失值不应导致崩溃
        """
        # TODO: 在此实现你的代码
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
            
        示例：
            dashboard.create_line_chart('日期', 'AQI', title='AQI变化趋势')
        """
        # TODO: 在此实现你的代码
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
            
        示例：
            dashboard.create_heatmap(columns=['AQI', 'PM2.5', 'PM10'])
        """
        # TODO: 在此实现你的代码
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
        # TODO: 在此实现你的代码
        pass

    def generate_report(self, output_dir: str) -> Dict:
        """
        生成完整分析报告（多个图表）
        
        Args:
            output_dir: 输出目录
            
        Returns:
            {'generated_files': ['bar.png', 'line.png', ...]}
            
        报告应包含：
        - 至少一个柱状图
        - 至少一个折线图
        - 可选：热图、分布图等
        """
        # TODO: 在此实现你的代码
        pass


if __name__ == "__main__":
    # 测试你的实现
    import os
    
    # 配置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 检查数据文件是否存在
    data_file = "data/air_quality.csv"
    if not os.path.exists(data_file):
        print(f"请先准备数据文件: {data_file}")
        print("可以从作业说明中获取示例数据")
    else:
        dashboard = DataDashboard(data_file)
        
        # 测试基本统计
        print("=== 基本统计 ===")
        stats = dashboard.get_basic_stats()
        print(f"行数: {stats.get('row_count', 'N/A')}")
        print(f"列数: {stats.get('column_count', 'N/A')}")
        print(f"缺失值: {stats.get('missing_count', {})}")
        
        # 测试图表生成
        print("\n=== 生成图表 ===")
        os.makedirs("output", exist_ok=True)
        
        dashboard.create_bar_chart(
            '城市', 'AQI', 
            title='各城市平均AQI',
            save_path='output/bar_chart.png'
        )
        print("✅ 柱状图已生成")
        
        print("\n✅ 测试完成")

