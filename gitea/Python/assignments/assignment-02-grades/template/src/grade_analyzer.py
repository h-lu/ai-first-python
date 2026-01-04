"""
成绩统计分析器

你的任务是实现 GradeAnalyzer 类，从 CSV 文件读取学生成绩数据，进行统计分析并生成报告。

功能要求：
1. 从 CSV 文件加载学生成绩数据（学号、姓名、各科成绩）
2. 计算各科目的平均分（需排除缺失值，不能将空值当作 0 分）
3. 生成分数分布统计（优秀/良好/及格/不及格）
4. 生成排名列表，需要处理并列情况（同分同名次，下一名跳过）
5. 导出分析报告到新文件

分数等级标准：
- 优秀：90-100 分
- 良好：80-89 分
- 及格：60-79 分
- 不及格：0-59 分

输入数据格式（CSV）：
学号,姓名,语文,数学,英语
2024001,张三,85,92,78
2024002,李四,76,88,82
2024003,王五,90,95,88
2024004,赵六,,80,75

边界情况处理：
- 缺失值：空单元格不应参与平均分计算，也不应视为 0 分
- 无效分数：负数或超过 100 的分数应被识别或标记
- 文件编码：可能需要处理 GBK/UTF-8 编码问题
- 重复学号：同一学号出现多次的情况
- 空文件：文件为空或只有表头的情况

示例用法：
analyzer = GradeAnalyzer()
analyzer.load_csv("grades.csv")
avg = analyzer.get_average("数学")  # 返回平均分
dist = analyzer.get_distribution("语文")  # 返回 {'优秀': 2, '良好': 3, ...}
ranking = analyzer.get_ranking("英语")  # 返回排名列表
analyzer.export_report("report.txt")  # 导出报告

提示：
- 思考：用什么数据结构存储学生数据？list of dict? dict of dict?
- 思考：并列排名如何处理？两个 95 分都排第 1，下一个 90 分排第 3（跳过 2）
- 思考：缺失值如何表示？None? 空字符串？如何区分"0分"和"缺失"？
- 可以让 AI 帮你设计代码结构，但你需要理解并验证每个部分
"""

import csv
from typing import List, Dict, Optional


class GradeAnalyzer:
    """
    成绩分析器
    
    从 CSV 文件读取学生成绩，提供统计分析功能。
    """

    def __init__(self):
        """
        初始化成绩分析器
        
        你需要决定如何存储学生数据。
        建议：使用列表存储，每个元素是一个字典，包含学号、姓名、各科成绩。
        """
        self.students: List[Dict] = []
        # TODO: 你可以添加其他属性来辅助实现

    def load_csv(self, filepath: str) -> bool:
        """
        加载 CSV 文件
        
        从指定路径读取 CSV 文件，解析学生成绩数据。
        需要处理：
        - 文件编码问题（UTF-8 或 GBK）
        - 缺失值（空单元格）
        - 数据类型转换（字符串转数字）
        
        Args:
            filepath: CSV 文件路径
            
        Returns:
            bool: 是否加载成功
            
        提示：
        - 可以使用 csv 模块或 pandas（如果允许）
        - 缺失值可以存储为 None 或空字符串，但要能区分"0分"和"缺失"
        - 建议先尝试 UTF-8，失败再尝试 GBK
        """
        # TODO: 在此实现你的代码
        pass

    def get_average(self, subject: str) -> float:
        """
        计算某科目平均分
        
        计算指定科目的平均分，排除缺失值。
        例如：如果有 3 个学生，但只有 2 个有数学成绩，则用 2 个成绩计算平均。
        
        Args:
            subject: 科目名称（'语文', '数学', '英语'）
            
        Returns:
            float: 平均分，保留 2 位小数
            
        示例：
            analyzer.get_average("数学")  # 返回 91.67
        """
        # TODO: 在此实现你的代码
        pass

    def get_distribution(self, subject: str) -> Dict[str, int]:
        """
        获取分数分布
        
        统计指定科目各等级的人数。
        
        Args:
            subject: 科目名称
            
        Returns:
            dict: 分数分布字典，格式如 {'优秀': 2, '良好': 5, '及格': 3, '不及格': 1}
            
        注意：
        - 只统计有成绩的学生（排除缺失值）
        - 如果某个等级没有人，该键也应存在，值为 0
        """
        # TODO: 在此实现你的代码
        pass

    def get_ranking(self, subject: str) -> List[Dict[str, any]]:
        """
        获取排名，处理并列情况
        
        返回指定科目的排名列表，按分数从高到低排序。
        并列处理规则：
        - 如果两个学生都是 95 分，他们并列第 1 名
        - 下一个 90 分的学生排第 3 名（跳过第 2 名）
        
        Args:
            subject: 科目名称
            
        Returns:
            list: 排名列表，每个元素是一个字典，包含：
                - 'rank': 排名（整数）
                - 'id': 学号（字符串）
                - 'name': 姓名（字符串）
                - 'score': 分数（浮点数或整数）
                
        示例：
            [
                {'rank': 1, 'id': '2024003', 'name': '王五', 'score': 95},
                {'rank': 1, 'id': '2024005', 'name': '钱七', 'score': 95},
                {'rank': 3, 'id': '2024002', 'name': '李四', 'score': 90},
                ...
            ]
            
        注意：
        - 只包含有成绩的学生（排除缺失值）
        - 排名从 1 开始
        """
        # TODO: 在此实现你的代码
        pass

    def export_report(self, filepath: str) -> bool:
        """
        导出分析报告
        
        将统计分析结果导出到文本文件。
        报告应包含：
        - 各科目平均分
        - 各科目分数分布
        - 各科目排名（前几名）
        
        Args:
            filepath: 导出文件路径
            
        Returns:
            bool: 是否导出成功
            
        提示：
        - 报告格式可以自由设计，但要清晰易读
        - 可以使用中文
        - 建议包含标题、分隔线等格式化元素
        """
        # TODO: 在此实现你的代码
        pass


if __name__ == "__main__":
    # 测试你的实现
    analyzer = GradeAnalyzer()
    
    # 加载测试数据（需要先创建 grades_normal.csv）
    if analyzer.load_csv("grades_normal.csv"):
        print("✅ CSV 加载成功")
        print(f"学生数量: {len(analyzer.students)}")
        
        # 测试平均分
        math_avg = analyzer.get_average("数学")
        print(f"数学平均分: {math_avg:.2f}")
        
        # 测试分数分布
        chinese_dist = analyzer.get_distribution("语文")
        print(f"语文分数分布: {chinese_dist}")
        
        # 测试排名
        english_ranking = analyzer.get_ranking("英语")
        print(f"英语排名（前3名）:")
        for item in english_ranking[:3]:
            print(f"  第{item['rank']}名: {item['name']} ({item['score']}分)")
        
        # 导出报告
        if analyzer.export_report("test_report.txt"):
            print("✅ 报告导出成功")
    else:
        print("❌ CSV 加载失败")
