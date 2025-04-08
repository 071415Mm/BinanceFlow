"""
辅助工具
提供一些通用的辅助函数
"""

from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_current_time_str():
    """获取当前时间字符串"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_analysis_metadata(interval, symbols, klines_count=50):
    """创建分析元数据"""
    return {
        "analysis_time": get_current_time_str(),
        "interval": interval,
        "symbols_analyzed": symbols,
        "klines_count": klines_count
    }


def log_progress(message):
    """记录进度日志"""
    logger.info(message)
    return message 