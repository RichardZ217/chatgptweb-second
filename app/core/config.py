#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Ruizhe Zhang
@time: 2025/8/5 17:11 
@file: config.py.py
@describe: 应用配置管理
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# API 配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ACCESS_TOKEN = os.getenv('OPENAI_ACCESS_TOKEN')
OPENAI_API_BASE_URL = os.getenv('OPENAI_API_BASE_URL')
OPENAI_API_MODEL = os.getenv('OPENAI_API_MODEL', 'glm-4-flash')
API_REVERSE_PROXY = os.getenv('API_REVERSE_PROXY')
OPENAI_API_DISABLE_DEBUG = os.getenv('OPENAI_API_DISABLE_DEBUG') == 'true'

# 代理配置
HTTPS_PROXY = os.getenv('HTTPS_PROXY') or os.getenv('ALL_PROXY')
SOCKS_PROXY_HOST = os.getenv('SOCKS_PROXY_HOST')
SOCKS_PROXY_PORT = os.getenv('SOCKS_PROXY_PORT')
SOCKS_PROXY_USERNAME = os.getenv('SOCKS_PROXY_USERNAME')
SOCKS_PROXY_PASSWORD = os.getenv('SOCKS_PROXY_PASSWORD')

# 其他配置
TIMEOUT_MS = int(os.getenv('TIMEOUT_MS', 100000))
MAX_REQUEST_PER_HOUR = os.getenv('MAX_REQUEST_PER_HOUR')
AUTH_SECRET_KEY = os.getenv('AUTH_SECRET_KEY')