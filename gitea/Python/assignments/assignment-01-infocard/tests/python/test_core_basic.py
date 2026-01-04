"""
Core 测试 - 基础功能（隐藏）
测试核心功能：布局、中文支持、邮箱校验、手机号标准化
"""

import pytest
from src.card_generator import generate_card


class TestCoreLayout:
    """测试卡片基本布局"""

    def test_card_basic_layout(self):
        """测试卡片包含所有必要元素"""
        card = generate_card(
            name="张三",
            email="zhangsan@example.com",
            phone="13812345678",
            school="上海应用技术大学",
            major="经济与管理学院",
        )
        assert "个人信息卡" in card
        assert "张三" in card
        assert "zhangsan@example.com" in card
        assert "上海应用技术大学" in card
        assert "经济与管理学院" in card

    def test_card_border_structure(self):
        """测试卡片边框结构"""
        card = generate_card(
            name="李四",
            email="lisi@test.com",
            phone="13900001111",
        )
        lines = card.strip().splitlines()
        # 顶部边框
        assert lines[0].startswith("┌")
        assert lines[0].endswith("┐")
        # 底部边框
        assert lines[-1].startswith("└")
        assert lines[-1].endswith("┘")


class TestCoreChineseName:
    """测试中文姓名支持"""

    def test_card_chinese_name(self):
        """测试中文姓名正确显示"""
        card = generate_card("李雷", "lilei@example.com", "13900001111")
        assert "李雷" in card

    def test_card_long_chinese_name(self):
        """测试较长的中文姓名"""
        card = generate_card("欧阳娜娜", "ouyang@example.com", "13800138000")
        assert "欧阳娜娜" in card


class TestCoreEmailValidation:
    """测试邮箱校验"""

    def test_card_email_valid(self):
        """测试有效邮箱"""
        card = generate_card("张三", "valid@example.com", "13812345678")
        assert "valid@example.com" in card

    def test_card_email_invalid_no_at(self):
        """测试无效邮箱（缺少@）应抛出异常"""
        with pytest.raises((ValueError, Exception)):
            generate_card("张三", "invalid_email.com", "13812345678")

    def test_card_email_invalid_no_dot(self):
        """测试无效邮箱（缺少.）应抛出异常"""
        with pytest.raises((ValueError, Exception)):
            generate_card("张三", "invalid@email", "13812345678")


class TestCorePhoneNormalize:
    """测试手机号标准化"""

    def test_card_phone_plain(self):
        """测试纯数字手机号标准化"""
        card = generate_card("张三", "test@test.com", "13812345678")
        assert "138-1234-5678" in card

    def test_card_phone_with_spaces(self):
        """测试带空格的手机号标准化"""
        card = generate_card("张三", "test@test.com", "138 1234 5678")
        assert "138-1234-5678" in card

    def test_card_phone_with_dashes(self):
        """测试带横线的手机号标准化"""
        card = generate_card("张三", "test@test.com", "138-1234-5678")
        assert "138-1234-5678" in card

    def test_card_phone_consistency(self):
        """测试不同格式输入产生一致输出"""
        card1 = generate_card("张三", "test@test.com", "138 1234 5678")
        card2 = generate_card("张三", "test@test.com", "138-1234-5678")
        card3 = generate_card("张三", "test@test.com", "13812345678")
        # 所有格式都应该输出 138-1234-5678
        assert "138-1234-5678" in card1
        assert "138-1234-5678" in card2
        assert "138-1234-5678" in card3
