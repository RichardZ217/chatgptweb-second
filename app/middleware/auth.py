#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Ruizhe Zhang
@time: 2025/8/5 17:17
@file: auth.py
@describe: 认证中间件
"""
from functools import wraps
from flask import request, jsonify
from app.core import config
from app.utils.is_helpers import is_not_empty_string

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查是否启用了认证
        if not is_not_empty_string(config.AUTH_SECRET_KEY):
            return f(*args, **kwargs)
            
        # 获取认证头
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                "status": "Unauthorized",
                "message": "Missing API key",
                "data": None
            }), 401
            
        # 验证token
        token = auth_header.replace('Bearer ', '')
        if token != config.AUTH_SECRET_KEY:
            return jsonify({
                "status": "Unauthorized",
                "message": "Invalid API key",
                "data": None
            }), 401
            
        return f(*args, **kwargs)
    return decorated_function
