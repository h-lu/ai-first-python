"""
公开测试 - 学生可见
这些测试帮助你验证基本功能是否正确
"""

import pytest
from src.card_generator import generate_card


def test_card_basic_info():
    """测试基本信息是否正确显示"""
    card = generate_card(
        name="张三",
        email="zhangsan@example.com",
        phone="13812345678",
        school="上海应用技术大学",
        major="经济与管理学院",
    )
    # 检查基本内容
    assert "张三" in card
    assert "zhangsan@example.com" in card
    assert "上海应用技术大学" in card
    assert "个人信息卡" in card


def test_card_has_border():
    """测试卡片是否有边框"""
    card = generate_card(
        name="张三",
        email="test@example.com",
        phone="13812345678",
    )
    lines = card.strip().splitlines()
    # 检查边框字符
    assert lines[0].startswith("┌")
    assert lines[0].endswith("┐")
    assert lines[-1].startswith("└")
    assert lines[-1].endswith("┘")


def test_card_phone_format():
    """测试手机号是否标准化为 138-1234-5678 格式"""
    card = generate_card("张三", "test@example.com", "13812345678")
    assert "138-1234-5678" in card
