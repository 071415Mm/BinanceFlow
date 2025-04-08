#!/bin/bash

# 安装依赖
pip install -r requirements.txt

# 安装 gunicorn
pip install gunicorn

# 启动应用
gunicorn -c gunicorn.conf.py "backend.api.api_server:create_app()" 