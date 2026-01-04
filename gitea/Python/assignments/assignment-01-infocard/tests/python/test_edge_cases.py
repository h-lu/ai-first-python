"""
Edge 测试 - 边界情况（隐藏）
测试边界处理：空字段、超长内容、多手机号、特殊字符
"""

import pytest
from src.card_generator import generate_card


class TestEdgeEmptyFields:
    """测试空字段处理"""

    def test_card_empty_school(self):
        """测试学校为空时显示占位符"""
        card = generate_card("张三", "test@test.com", "13812345678", school=None)
        assert "未填写" in card

    def test_card_empty_major(self):
        """测试专业为空时显示占位符"""
        card = generate_card("张三", "test@test.com", "13812345678", major=None)
        assert "未填写" in card

    def test_card_both_optional_empty(self):
        """测试学校和专业都为空"""
        card = generate_card("张三", "test@test.com", "13812345678")
        # 应该有两处"未填写"
        assert card.count("未填写") >= 2


class TestEdgeLongContent:
    """测试超长内容处理"""

    def test_card_long_name(self):
        """测试超长姓名不会破坏卡片布局"""
        long_name = "阿" * 50
        card = generate_card(long_name, "test@test.com", "13812345678")
        # 每行不应该太宽
        for line in card.splitlines():
            assert len(line) < 80, f"行太长: {len(line)} 字符"

    def test_card_long_email(self):
        """测试超长邮箱不会破坏卡片布局"""
        long_email = "a" * 40 + "@example.com"
        card = generate_card("张三", long_email, "13812345678")
        # 卡片应该能正常生成
        assert "张三" in card


class TestEdgeMultiplePhones:
    """测试多手机号支持"""

    def test_card_multiple_phones_list(self):
        """测试传入手机号列表"""
        card = generate_card(
            "张三", 
            "test@test.com", 
            ["13812345678", "13999998888"]
        )
        # 两个手机号都应该出现（标准化格式）
        assert "138-1234-5678" in card
        assert "139-9999-8888" in card

    def test_card_multiple_phones_separator(self):
        """测试多手机号有分隔符"""
        card = generate_card(
            "张三",
            "test@test.com",
            ["13812345678", "13999998888"]
        )
        # 应该有某种分隔方式
        assert "/" in card or "、" in card or "\n" in card.split("手机")[1].split("学校")[0]


class TestEdgeSpecialChars:
    """测试特殊字符处理"""

    def test_card_special_chars_in_name(self):
        """测试姓名中的特殊字符"""
        card = generate_card("张三(实习)", "test@test.com", "13812345678")
        assert "张三(实习)" in card

    def test_card_unicode_name(self):
        """测试 Unicode 姓名"""
        card = generate_card("김철수", "kim@test.com", "13812345678")
        assert "김철수" in card
