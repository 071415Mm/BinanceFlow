"""
Gunicorn 配置文件
用于生产环境的 WSGI 服务器配置
"""

# 工作进程数
workers = 4

# 每个工作进程的线程数
threads = 2

# 监听地址和端口
bind = "0.0.0.0:10000"

# 超时设置
timeout = 120

# 访问日志格式
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 错误日志
errorlog = "-"

# 预加载应用
preload_app = True 