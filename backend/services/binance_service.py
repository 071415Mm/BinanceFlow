"""
币安数据服务
处理与币安API的交互，获取K线数据和订单簿数据
"""

import requests
import logging
from datetime import datetime
import os

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 设置API密钥和URL
BINANCE_API_URL = "https://api.binance.com"
BINANCE_FUTURES_API_URL = "https://fapi.binance.com"
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")


def get_klines_data(symbol, interval="5m", limit=50, is_futures=False):
    """获取K线数据"""
    try:
        base_url = BINANCE_FUTURES_API_URL if is_futures else BINANCE_API_URL
        endpoint = "/fapi/v1/klines" if is_futures else "/api/v3/klines"

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit + 1  # 多获取一根，用于计算最后一根的变化
        }

        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()

        klines = response.json()

        # 移除最后一根未完成的K线
        klines = klines[:-1]

        # 处理K线数据
        processed_klines = []
        for i, kline in enumerate(klines):
            open_time = datetime.fromtimestamp(kline[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            close_time = datetime.fromtimestamp(kline[6] / 1000).strftime('%Y-%m-%d %H:%M:%S')

            open_price = float(kline[1])
            high_price = float(kline[2])
            low_price = float(kline[3])
            close_price = float(kline[4])
            volume = float(kline[5])
            quote_asset_volume = float(kline[7])

            # 计算买入和卖出量（简化估算）
            if close_price >= open_price:
                # 上涨K线，假设60%的成交量是买入
                buy_volume = volume * 0.6
                sell_volume = volume * 0.4
            else:
                # 下跌K线，假设40%的成交量是买入
                buy_volume = volume * 0.4
                sell_volume = volume * 0.6

            # 计算净流入资金
            net_inflow = (buy_volume - sell_volume) * close_price

            # 计算价格变化百分比
            price_change_pct = ((close_price - open_price) / open_price) * 100

            processed_kline = {
                "open_time": open_time,
                "close_time": close_time,
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": volume,
                "quote_volume": quote_asset_volume,
                "buy_volume": buy_volume,
                "sell_volume": sell_volume,
                "net_inflow": net_inflow,
                "price_change_pct": price_change_pct
            }

            processed_klines.append(processed_kline)

        return processed_klines

    except Exception as e:
        logger.error(f"获取K线数据出错: {e}")
        raise Exception(f"获取{symbol} {interval}K线数据失败: {str(e)}")


def get_orderbook_stats(symbol, is_futures=False, limit=1000):
    """获取订单簿数据并计算统计信息"""
    try:
        base_url = BINANCE_FUTURES_API_URL if is_futures else BINANCE_API_URL
        endpoint = "/fapi/v1/depth" if is_futures else "/api/v3/depth"

        params = {
            "symbol": symbol,
            "limit": limit
        }

        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()

        orderbook = response.json()

        # 处理订单簿数据
        bids = [[float(price), float(qty)] for price, qty in orderbook["bids"]]
        asks = [[float(price), float(qty)] for price, qty in orderbook["asks"]]

        # 计算买卖盘总量
        total_bid_qty = sum(bid[1] for bid in bids)
        total_ask_qty = sum(ask[1] for ask in asks)

        # 计算买卖盘不平衡度
        imbalance = (total_bid_qty - total_ask_qty) / (total_bid_qty + total_ask_qty) if (
                total_bid_qty + total_ask_qty) > 0 else 0

        # 计算买卖盘压力
        bid_pressure = sum(bid[0] * bid[1] for bid in bids)
        ask_pressure = sum(ask[0] * ask[1] for ask in asks)

        # 计算买卖盘压力比
        pressure_ratio = bid_pressure / ask_pressure if ask_pressure > 0 else float('inf')

        # 计算价格范围
        bid_prices = [bid[0] for bid in bids]
        ask_prices = [ask[0] for ask in asks]

        price_range = {
            "highest_bid": max(bid_prices) if bid_prices else 0,
            "lowest_ask": min(ask_prices) if ask_prices else 0,
            "spread": min(ask_prices) - max(bid_prices) if bid_prices and ask_prices else 0,
            "spread_pct": ((min(ask_prices) - max(bid_prices)) / max(bid_prices) * 100) if bid_prices and ask_prices else 0
        }

        return {
            "total_bid_qty": total_bid_qty,
            "total_ask_qty": total_ask_qty,
            "imbalance": imbalance,
            "bid_pressure": bid_pressure,
            "ask_pressure": ask_pressure,
            "pressure_ratio": pressure_ratio,
            "price_range": price_range
        }

    except Exception as e:
        logger.error(f"获取订单簿数据出错: {e}")
        raise Exception(f"获取{symbol}订单簿数据失败: {str(e)}") 