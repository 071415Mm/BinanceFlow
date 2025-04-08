#!/usr/bin/env python
"""
币安资金流向分析系统 - 启动脚本
提供一个方便的入口点来启动后端API服务器
"""

import os
import argparse
import webbrowser
import threading
import time
import logging
from dotenv import load_dotenv
from backend.api.api_server import run_server

# 加载.env文件
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def open_browser(host, port, delay=1.5):
    """
    在新线程中打开浏览器访问应用
    """
    def _open_browser():
        time.sleep(delay)  # 延迟一段时间确保服务器已启动
        url = f"http://{host}:{port}"
        logger.info(f"正在打开浏览器访问 {url}")
        webbrowser.open(url)

    threading.Thread(target=_open_browser).start()


def main():
    """
    主函数，解析命令行参数并启动服务器
    """
    parser = argparse.ArgumentParser(description='启动币安资金流向分析系统')
    parser.add_argument('-H', '--host', default='127.0.0.1', help='API服务器主机地址 (默认: 127.0.0.1)')
    parser.add_argument('-p', '--port', type=int, default=5000, help='API服务器端口 (默认: 5000)')
    parser.add_argument('-d', '--debug', action='store_true', help='启用调试模式')
    parser.add_argument('-n', '--no-browser', action='store_true', help='不自动打开浏览器')
    args = parser.parse_args()

    # 设置环境变量
    os.environ["API_HOST"] = args.host
    os.environ["API_PORT"] = str(args.port)
    os.environ["API_DEBUG"] = str(args.debug).lower()

    # 检查已加载的环境变量
    logger.info(f"DEEPSEEK_API_KEY 设置状态: {'已设置' if os.environ.get('DEEPSEEK_API_KEY') else '未设置'}")
    
    # 提示用户设置API密钥
    if not os.environ.get("DEEPSEEK_API_KEY"):
        logger.warning("警告: 未设置 DEEPSEEK_API_KEY 环境变量")
        print("\n请设置 DEEPSEEK_API_KEY 环境变量以启用AI分析功能。")
        print("您可以通过以下方式设置环境变量:")
        print("  Windows:  set DEEPSEEK_API_KEY=您的密钥")
        print("  Linux/Mac:  export DEEPSEEK_API_KEY=您的密钥\n")

    if not os.environ.get("BINANCE_API_KEY"):
        logger.warning("未设置 BINANCE_API_KEY 环境变量，将使用公共API访问限制")

    # 自动打开浏览器（除非指定了 --no-browser 选项）
    if not args.no_browser:
        open_browser(args.host, args.port)

    # 启动服务器
    logger.info(f"启动币安资金流向分析系统，API服务器运行在 {args.host}:{args.port}")
    run_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main() 