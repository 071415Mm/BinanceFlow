#!/bin/bash

# 安装依赖
pip install -r requirements.txt

# 安装 gunicorn
pip install gunicorn

# 加载环境变量
export $(cat .env | xargs)

# 启动应用
gunicorn -c gunicorn.conf.py wsgi:app 