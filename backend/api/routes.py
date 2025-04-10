"""
API路由
定义REST API的端点
"""

from flask import Blueprint, request, jsonify
import logging
from datetime import datetime

# 导入服务模块
from backend.services import binance_service, analysis_service, ai_service
from backend.utils import helpers

# 创建蓝图
api_bp = Blueprint('api', __name__)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 在routes.py中添加全局变量来跟踪分析状态
_analysis_in_progress = False


@api_bp.route('/symbols', methods=['GET'])
def get_default_symbols():
    """获取默认交易对列表"""
    return jsonify({
        "status": "success",
        "data": ["BTCUSDT", "ETHUSDT"]
    })


@api_bp.route('/intervals', methods=['GET'])
def get_intervals():
    """获取可用的K线时间间隔"""
    return jsonify({
        "status": "success",
        "data": ["5m", "15m", "30m", "1h", "4h", "1d"]
    })


@api_bp.route('/analyze', methods=['POST'])
def analyze_symbols():
    """分析交易对的资金流向"""
    global _analysis_in_progress
    
    # 检查是否有正在进行的分析
    if _analysis_in_progress:
        return jsonify({
            "status": "error",
            "message": "已有分析正在进行中，请等待完成后再试"
        }), 429  # 使用429状态码表示请求过多
    
    try:
        _analysis_in_progress = True
        data = request.json
        if not data:
            return jsonify({
                "status": "error",
                "message": "请求数据为空"
            }), 400

        symbols = data.get('symbols', [])
        interval = data.get('interval', '1h')

        if not symbols:
            return jsonify({
                "status": "error",
                "message": "未提供交易对"
            }), 400

        # 记录开始时间
        start_time = datetime.now()
        logger.info(f"开始分析 {', '.join(symbols)}, 时间间隔: {interval}")

        # 获取现货和期货的K线数据
        spot_klines_data = {}
        futures_klines_data = {}

        for symbol in symbols:
            helpers.log_progress(f"正在获取 {symbol} 现货{interval}K线数据...")
            spot_klines_data[symbol] = binance_service.get_klines_data(
                symbol, interval=interval, limit=50, is_futures=False
            )

            helpers.log_progress(f"正在获取 {symbol} 期货{interval}K线数据...")
            futures_klines_data[symbol] = binance_service.get_klines_data(
                symbol, interval=interval, limit=50, is_futures=True
            )

        # 获取订单簿数据
        spot_order_books = {}
        futures_order_books = {}

        for symbol in symbols:
            helpers.log_progress(f"正在获取 {symbol} 订单簿数据...")
            spot_order_books[symbol] = binance_service.get_orderbook_stats(symbol, is_futures=False)
            futures_order_books[symbol] = binance_service.get_orderbook_stats(symbol, is_futures=True)

        # 分析资金流向趋势
        spot_trend_analysis = {}
        futures_trend_analysis = {}

        for symbol in symbols:
            helpers.log_progress(f"正在分析 {symbol} 资金流向趋势...")
            spot_trend_analysis[symbol] = analysis_service.analyze_funding_flow_trend(spot_klines_data[symbol])
            futures_trend_analysis[symbol] = analysis_service.analyze_funding_flow_trend(futures_klines_data[symbol])

        # 检测异常交易
        spot_anomalies = {}
        futures_anomalies = {}

        for symbol in symbols:
            helpers.log_progress(f"正在检测 {symbol} 异常交易...")
            spot_anomalies[symbol] = analysis_service.detect_anomalies(spot_klines_data[symbol])
            futures_anomalies[symbol] = analysis_service.detect_anomalies(futures_klines_data[symbol])

        # 分析资金压力
        spot_pressure_analysis = {}
        futures_pressure_analysis = {}

        for symbol in symbols:
            helpers.log_progress(f"正在分析 {symbol} 资金压力...")
            spot_pressure_analysis[symbol] = analysis_service.analyze_funding_pressure(
                spot_klines_data[symbol], spot_order_books[symbol]
            )
            futures_pressure_analysis[symbol] = analysis_service.analyze_funding_pressure(
                futures_klines_data[symbol], futures_order_books[symbol]
            )

        # 整合数据
        analysis_data = {}

        for symbol in symbols:
            analysis_data[symbol] = {
                "spot": {
                    "klines_summary": {
                        "first_time": spot_klines_data[symbol][0]["open_time"] if spot_klines_data[symbol] else None,
                        "last_time": spot_klines_data[symbol][-1]["close_time"] if spot_klines_data[symbol] else None,
                        "price_change": (spot_klines_data[symbol][-1]["close"] - spot_klines_data[symbol][0]["open"]) /
                                        spot_klines_data[symbol][0]["open"] * 100 if spot_klines_data[symbol] else 0,
                        "current_price": spot_klines_data[symbol][-1]["close"] if spot_klines_data[symbol] else 0,
                        "total_volume": sum(k["volume"] for k in spot_klines_data[symbol]) if spot_klines_data[
                            symbol] else 0,
                        "total_quote_volume": sum(k["quote_volume"] for k in spot_klines_data[symbol]) if
                        spot_klines_data[symbol] else 0
                    },
                    "funding_trend": spot_trend_analysis[symbol],
                    "anomalies": spot_anomalies[symbol],
                    "order_book": spot_order_books[symbol],
                    "funding_pressure": spot_pressure_analysis[symbol]
                },
                "futures": {
                    "klines_summary": {
                        "first_time": futures_klines_data[symbol][0]["open_time"] if futures_klines_data[
                            symbol] else None,
                        "last_time": futures_klines_data[symbol][-1]["close_time"] if futures_klines_data[
                            symbol] else None,
                        "price_change": (futures_klines_data[symbol][-1]["close"] - futures_klines_data[symbol][0][
                            "open"]) / futures_klines_data[symbol][0]["open"] * 100 if futures_klines_data[
                            symbol] else 0,
                        "current_price": futures_klines_data[symbol][-1]["close"] if futures_klines_data[symbol] else 0,
                        "total_volume": sum(k["volume"] for k in futures_klines_data[symbol]) if futures_klines_data[
                            symbol] else 0,
                        "total_quote_volume": sum(k["quote_volume"] for k in futures_klines_data[symbol]) if
                        futures_klines_data[symbol] else 0
                    },
                    "funding_trend": futures_trend_analysis[symbol],
                    "anomalies": futures_anomalies[symbol],
                    "order_book": futures_order_books[symbol],
                    "funding_pressure": futures_pressure_analysis[symbol]
                },
                "comparison": {
                    "spot_vs_futures_price_diff": (spot_klines_data[symbol][-1]["close"] -
                                                   futures_klines_data[symbol][-1]["close"]) /
                                                  spot_klines_data[symbol][-1]["close"] * 100 if spot_klines_data[
                                                      symbol] and futures_klines_data[symbol] else 0,
                    "spot_vs_futures_volume_ratio": sum(k["volume"] for k in spot_klines_data[symbol]) / sum(
                        k["volume"] for k in futures_klines_data[symbol]) if spot_klines_data[symbol] and
                                                   futures_klines_data[symbol] and sum(
                        k["volume"] for k in futures_klines_data[symbol]) > 0 else 0,
                    "spot_vs_futures_net_inflow_diff": spot_trend_analysis[symbol]["net_inflow_total"] -
                                                       futures_trend_analysis[symbol]["net_inflow_total"] if
                    spot_trend_analysis[symbol] and futures_trend_analysis[symbol] else 0
                }
            }

        # 添加分析时间和参数信息
        analysis_metadata = helpers.create_analysis_metadata(interval, symbols)

        # 整合所有数据
        deepseek_data = {
            "metadata": analysis_metadata,
            "analysis": analysis_data
        }

        # 发送到DeepSeek进行解读
        helpers.log_progress("正在通过AI解读分析结果...")
        deepseek_result = ai_service.send_to_deepseek(deepseek_data, interval)

        # 计算总耗时
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # 返回结果
        return jsonify({
            "status": "success",
            "data": {
                "raw_analysis": deepseek_data,
                "ai_interpretation": deepseek_result,
                "metadata": {
                    **analysis_metadata,
                    "duration": duration
                }
            }
        })

    except Exception as e:
        logger.error(f"分析过程中发生错误: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": f"分析过程中发生错误: {str(e)}"
        }), 500
    finally:
        _analysis_in_progress = False


@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "success",
        "message": "API服务正常运行",
        "timestamp": helpers.get_current_time_str()
    }) 