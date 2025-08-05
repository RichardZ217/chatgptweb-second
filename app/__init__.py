#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: Ruizhe Zhang
@time: 2025/8/5 16:54 
@file: __init__.py.py
@describe: Flask 应用初始化
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

def create_app():
    # 设置静态文件夹为项目根目录下的 static 文件夹
    app = Flask(__name__, static_folder='../static', static_url_path='')
    CORS(app)
    
    # 注册蓝图
    from app.api.routes import api_bp
    app.register_blueprint(api_bp)
    
    # 使蓝图同时在根路径和 /api 路径下可用
    from app.api.routes import create_root_routes
    app.register_blueprint(create_root_routes())
    
    # 添加根路径处理
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    # 捕获所有未处理的路由，用于支持 SPA 前端路由
    @app.route('/<path:path>')
    def catch_all(path):
        # 先尝试作为静态文件提供
        static_path = os.path.join(app.static_folder, path)
        if os.path.exists(static_path) and os.path.isfile(static_path):
            return send_from_directory(app.static_folder, path)
        # 否则返回 index.html，让前端路由处理
        return send_from_directory(app.static_folder, 'index.html')
    
    return app
