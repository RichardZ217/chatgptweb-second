#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file: check_structure.py
@describe: 检查项目结构并复制必要文件
"""
import os
import shutil
import sys

def check_and_create_structure():
    # 定义项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # 检查静态文件夹是否存在
    static_dir = os.path.join(project_root, 'static')
    if not os.path.exists(static_dir):
        print(f"创建静态文件目录: {static_dir}")
        os.makedirs(static_dir)
    
    # 检查 index.html 是否存在
    index_file = os.path.join(static_dir, 'index.html')
    if not os.path.exists(index_file):
        # 尝试从 app/static 目录复制
        app_static_index = os.path.join(project_root, 'app', 'static', 'index.html')
        if os.path.exists(app_static_index):
            print(f"从 {app_static_index} 复制 index.html 到 {index_file}")
            shutil.copy2(app_static_index, index_file)
        else:
            # 如果找不到源文件，创建一个简单的 index.html
            print(f"创建简单的 index.html 文件: {index_file}")
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ChatGPT Web</title>
</head>
<body>
    <h1>ChatGPT Web</h1>
    <p>服务器已成功启动！</p>
</body>
</html>
""")
    
    # 检查 assets 目录是否存在
    assets_dir = os.path.join(static_dir, 'assets')
    if not os.path.exists(assets_dir):
        print(f"创建资源目录: {assets_dir}")
        os.makedirs(assets_dir)
        
        # 尝试从 app/static/assets 复制文件
        app_assets_dir = os.path.join(project_root, 'app', 'static', 'assets')
        if os.path.exists(app_assets_dir):
            print(f"从 {app_assets_dir} 复制资源文件")
            for item in os.listdir(app_assets_dir):
                s = os.path.join(app_assets_dir, item)
                d = os.path.join(assets_dir, item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)
                else:
                    shutil.copytree(s, d)
    
    print("项目结构检查完成!")

if __name__ == "__main__":
    check_and_create_structure()
