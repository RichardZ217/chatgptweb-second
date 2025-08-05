#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Ruizhe Zhang
@time: 2025/8/5 17:12 
@file: chat_service.py
@describe: 聊天服务实现
"""
import openai
from openai import OpenAI
import requests
import time
from datetime import datetime
import socks
import socket
import urllib3
from app.core import config
from app.utils.is_helpers import is_not_empty_string
from app.utils.response_helpers import send_response

# --- 错误代码映射 ---
ERROR_CODE_MESSAGE = {
    401: '[OpenAI] 提供错误的API密钥 | Incorrect API key provided',
    403: '[OpenAI] 服务器拒绝访问，请稍后再试 | Server refused to access, please try again later',
    502: '[OpenAI] 错误的网关 |  Bad Gateway',
    503: '[OpenAI] 服务器繁忙，请稍后再试 | Server is busy, please try again later',
    504: '[OpenAI] 网关超时 | Gateway Time-out',
    500: '[OpenAI] 服务器繁忙，请稍后再试 | Internal Server Error',
}

# --- API模型类型 ---
api_model = "ChatGPTAPI"
http_client = None

# --- 配置代理 ---
def setup_proxy():
    global http_client
    
    # 设置SOCKS代理
    if is_not_empty_string(config.SOCKS_PROXY_HOST) and is_not_empty_string(config.SOCKS_PROXY_PORT):
        socks.set_default_proxy(
            socks.SOCKS5, 
            config.SOCKS_PROXY_HOST, 
            int(config.SOCKS_PROXY_PORT),
            username=config.SOCKS_PROXY_USERNAME if is_not_empty_string(config.SOCKS_PROXY_USERNAME) else None,
            password=config.SOCKS_PROXY_PASSWORD if is_not_empty_string(config.SOCKS_PROXY_PASSWORD) else None
        )
        socket.socket = socks.socksocket
    # 设置HTTPS代理
    elif is_not_empty_string(config.HTTPS_PROXY):
        proxies = {
            "http": config.HTTPS_PROXY,
            "https": config.HTTPS_PROXY,
        }
        http_client = urllib3.ProxyManager(config.HTTPS_PROXY)

# --- 初始化OpenAI客户端 ---
def init_openai_client():
    client_args = {}
    
    # 设置API密钥
    if is_not_empty_string(config.OPENAI_API_KEY):
        client_args["api_key"] = config.OPENAI_API_KEY
        
        # 设置API基础URL
        if is_not_empty_string(config.OPENAI_API_BASE_URL):
            if "/v1" in config.OPENAI_API_BASE_URL:
                client_args["base_url"] = config.OPENAI_API_BASE_URL
            elif "/v4" in config.OPENAI_API_BASE_URL:
                client_args["base_url"] = config.OPENAI_API_BASE_URL
            else:
                client_args["base_url"] = f"{config.OPENAI_API_BASE_URL}/v1"
        
        return OpenAI(**client_args)
    else:
        raise ValueError("Missing OpenAI API key")

# 初始化代理和OpenAI客户端
setup_proxy()
client = init_openai_client()

# --- 聊天回复主函数 ---
def chat_reply_process(message, last_context=None, system_message=None, temperature=None, top_p=None):
    try:
        # 准备消息
        messages = []
        if is_not_empty_string(system_message):
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": message})
        
        # 准备参数
        params = {
            "model": config.OPENAI_API_MODEL,
            "messages": messages,
            "stream": True,
        }
        
        if temperature is not None:
            params["temperature"] = temperature
            
        if top_p is not None:
            params["top_p"] = top_p
        
        # 创建流式响应
        response_stream = client.chat.completions.create(**params)
        
        # 跟踪完整内容
        full_content = ""
        response_id = None
        
        # 处理每个响应块
        for chunk in response_stream:
            # 提取响应ID
            if response_id is None and hasattr(chunk, 'id'):
                response_id = chunk.id
            
            # 确保我们有一个有效的响应ID
            if response_id is None:
                response_id = f"chatcmpl-{He}"
            
            # 处理内容增量
            content = ""
            if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    content = delta.content
            
            # 如果有新内容，更新并生成响应
            if content:
                full_content += content
                yield {
                    "id": response_id,
                    "text": full_content,
                    "delta": content,
                    "detail": {
                        "role": "assistant"
                    }
                }
                
    except openai.APIError as e:
        # 处理API错误
        code = e.status_code if hasattr(e, 'status_code') else 500
        print(f"OpenAI API error: {e}")
        
        error_message = ERROR_CODE_MESSAGE.get(code, str(e))
        yield {"error": True, "text": error_message}
        
    except Exception as e:
        # 处理其他异常
        print(f"Unexpected error: {str(e)}")
        yield {"error": True, "text": str(e)}

# --- 获取使用情况 ---
def fetch_usage():
    if not is_not_empty_string(config.OPENAI_API_KEY):
        return "-"
        
    try:
        # 计算开始和结束日期
        start_date, end_date = format_date()
        
        # 基础URL
        api_base_url = config.OPENAI_API_BASE_URL if is_not_empty_string(config.OPENAI_API_BASE_URL) else "https://api.openai.com"
        
        # 构建请求URL
        url_usage = f"{api_base_url}/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
        
        # 设置请求头
        headers = {
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        
        # 发送请求
        response = requests.get(url_usage, headers=headers)
        if not response.ok:
            return "-"
            
        usage_data = response.json()
        usage = round(usage_data.get("total_usage", 0)) / 100
        return f"${usage}" if usage else "-"
        
    except Exception as e:
        print(f"Error fetching usage: {e}")
        return "-"

# --- 格式化日期 ---
def format_date():
    today = datetime.now()
    year = today.year
    month = today.month
    
    # 计算当月第一天和最后一天
    first_day = f"{year}-{month:02d}-01"
    
    if month == 12:
        last_day = f"{year}-{month:02d}-31"
    else:
        last_day = f"{year}-{month:02d}-{(datetime(year, month+1, 1) - datetime(1, 1, 1)).days:02d}"
        
    return [first_day, last_day]

# --- 获取配置信息 ---
def get_chat_config():
    usage = fetch_usage()
    reverse_proxy = config.API_REVERSE_PROXY if is_not_empty_string(config.API_REVERSE_PROXY) else "-"
    https_proxy = config.HTTPS_PROXY if is_not_empty_string(config.HTTPS_PROXY) else "-"
    socks_proxy = f"{config.SOCKS_PROXY_HOST}:{config.SOCKS_PROXY_PORT}" if (is_not_empty_string(config.SOCKS_PROXY_HOST) and is_not_empty_string(config.SOCKS_PROXY_PORT)) else "-"
    
    return send_response({
        "type": "Success",
        "data": {
            "apiModel": api_model,
            "reverseProxy": reverse_proxy,
            "timeoutMs": config.TIMEOUT_MS,
            "socksProxy": socks_proxy,
            "httpsProxy": https_proxy,
            "usage": usage
        }
    })

# --- 获取当前模型 ---
def get_current_model():
    return api_model