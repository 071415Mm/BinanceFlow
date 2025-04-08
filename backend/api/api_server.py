"""
API服务器
用于启动API服务
"""

import os
from flask import Flask, jsonify, send_from_directory, redirect
from flask_cors import CORS
import logging

# 导入路由
from backend.api.routes import api_bp

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 获取项目根目录
    root_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    frontend_dir = os.path.join(root_dir, 'frontend')
    public_dir = os.path.join(frontend_dir, 'public')
    src_dir = os.path.join(frontend_dir, 'src')
    
    logger.info(f"前端目录: {frontend_dir}")
    logger.info(f"public目录: {public_dir}")
    
    # 配置CORS
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 添加根路由 - 重定向到前端首页
    @app.route('/')
    def index():
        return send_from_directory(public_dir, 'index.html')
    
    # 添加静态文件服务
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(public_dir, path)
        
    # 添加前端JS服务
    @app.route('/src/<path:path>')
    def serve_src(path):
        return send_from_directory(src_dir, path)
    
    # 配置500错误处理
    @app.errorhandler(500)
    def handle_500(error):
        logger.error(f"服务器错误: {str(error)}")
        return jsonify({
            "status": "error",
            "message": "服务器内部错误"
        }), 500
    
    # 配置404错误处理
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "status": "error",
            "message": "请求的资源不存在"
        }), 404
    
    return app


def run_server(host='0.0.0.0', port=5000, debug=False):
    """运行API服务器"""
    app = create_app()
    logger.info(f"API服务器启动在 http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    # 获取环境变量或使用默认值
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "5000"))
    debug = os.getenv("API_DEBUG", "False").lower() == "true"
    
    # 运行服务器
    run_server(host, port, debug) 