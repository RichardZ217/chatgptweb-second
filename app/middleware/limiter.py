#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Ruizhe Zhang
@time: 2025/8/5 17:17
@file: limiter.py
@describe: 速率限制中间件
"""
from functools import wraps
from flask import request, jsonify
import time
import threading
from app.core import config
from app.utils.is_helpers import is_not_empty_string

# 请求计数器和锁
request_counts = {}
request_lock = threading.Lock()

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 如果没有设置速率限制，直接通过
        if not is_not_empty_string(config.MAX_REQUEST_PER_HOUR):
            return f(*args, **kwargs)
            
        # 获取客户端IP
        ip = request.remote_addr
        max_requests = int(config.MAX_REQUEST_PER_HOUR)
        current_hour = int(time.time() / 3600)
        
        with request_lock:
            # 清理过期记录
            for key in list(request_counts.keys()):
                if key[1] != current_hour:
                    del request_counts[key]
                    
            # 检查当前IP的请求次数
            count = request_counts.get((ip, current_hour), 0)
            
            if count >= max_requests:
                return jsonify({
                    "status": "Too Many Requests",
                    "message": "您的请求次数已超过限制",
                    "data": None
                }), 429
                
            # 增加计数
            request_counts[(ip, current_hour)] = count + 1
            
        return f(*args, **kwargs)
    return decorated_function
