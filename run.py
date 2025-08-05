#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Ruizhe Zhang
@file: run.py
@describe: 应用入口
"""
import os
from check_structure import check_and_create_structure
from app import create_app

# 检查项目结构
check_and_create_structure()

# 创建应用
app = create_app()

if __name__ == "__main__":
    print("Server is running on port 3002")
    # 设置更长的响应超时时间
    app.run(host='0.0.0.0', port=3002, debug=False, threaded=True)