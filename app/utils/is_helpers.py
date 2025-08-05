#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Ruizhe Zhang
@time: 2025/8/5 17:15
@file: is_helpers.py
@describe: 辅助函数
"""

def is_not_empty_string(value):
    """
    检查值是否为非空字符串
    """
    return isinstance(value, str) and value.strip() != ""
