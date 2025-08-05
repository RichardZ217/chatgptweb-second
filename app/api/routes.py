#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Ruizhe Zhang
@time: 2025/8/5 17:13 
@file: routes.py
@describe: API 路由处理
"""
from flask import Blueprint, request, jsonify, Response, stream_with_context
from app.services import chat_service
from app.core import config
import json

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/chat-process', methods=['POST'])
def chat_process():
    # 设置内容类型为 octet-stream，确保浏览器不缓冲响应
    response = Response(content_type='application/octet-stream')
    response.headers['X-Accel-Buffering'] = 'no'  # 禁用Nginx缓冲
    
    # 获取请求参数
    data = request.get_json()
    prompt = data.get('prompt')
    options = data.get('options', {})
    system_message = data.get('systemMessage')
    temperature = data.get('temperature', 0.8)
    top_p = data.get('top_p', 1.0)

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    def generate():
        first_chunk = True
        try:
            # 直接使用生成器传递流式响应
            for chunk in chat_service.chat_reply_process(
                prompt, 
                options, 
                system_message, 
                temperature, 
                top_p
            ):
                if first_chunk:
                    yield json.dumps(chunk)
                    first_chunk = False
                else:
                    # 每个后续块前面加上换行符
                    yield f"\n{json.dumps(chunk)}"
                # 添加小延迟以确保浏览器渲染
                # import time
                # time.sleep(0.01)
        except Exception as e:
            print(f"Stream error: {str(e)}")
            yield json.dumps({"error": True, "text": str(e)})
            
    return Response(stream_with_context(generate()), 
                    mimetype='application/octet-stream',
                    headers={'X-Accel-Buffering': 'no'})

@api_bp.route('/config', methods=['POST'])
def get_config():
    config_data = chat_service.get_chat_config()
    return jsonify({"status": "Success", "data": config_data})

@api_bp.route('/session', methods=['POST'])
def get_session():
    has_auth = bool(config.AUTH_SECRET_KEY)
    model = chat_service.get_current_model()
    return jsonify({
        "status": "Success",
        "message": "",
        "data": {"auth": has_auth, "model": model}
    })

@api_bp.route('/verify', methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({"status": "Fail", "message": "Secret key is empty", "data": None})

    if token != config.AUTH_SECRET_KEY:
        return jsonify({"status": "Fail", "message": "密钥无效 | Secret key is invalid", "data": None})

    return jsonify({"status": "Success", "message": "Verify successfully", "data": None})

# 创建一个在根路径下的蓝图，确保与原 Node.js 版本兼容
def create_root_routes():
    root_bp = Blueprint('root', __name__)
    
    # 复制所有 API 蓝图的路由到根路径
    @root_bp.route('/chat-process', methods=['POST'])
    def chat_process():
        return api_bp.view_functions['chat_process']()
    
    @root_bp.route('/config', methods=['POST'])
    def get_config():
        return api_bp.view_functions['get_config']()
    
    @root_bp.route('/session', methods=['POST'])
    def get_session():
        return api_bp.view_functions['get_session']()
    
    @root_bp.route('/verify', methods=['POST'])
    def verify_token():
        return api_bp.view_functions['verify_token']()
    
    return root_bp

@api_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the API"}), 200

def create_app():
    from flask import Flask
    app = Flask(__name__, static_url_path='', static_folder='static')
    
    # 注册蓝图
    app.register_blueprint(api_bp)
    app.register_blueprint(create_root_routes())
    
    return app