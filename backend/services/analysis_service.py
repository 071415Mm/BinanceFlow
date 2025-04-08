"""
分析服务
处理数据分析逻辑，包括资金流向趋势分析、异常检测和资金压力分析
"""

import numpy as np
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def analyze_funding_flow_trend(klines_data, window_size=10):
    """分析资金流向趋势"""
    if not klines_data or len(klines_data) < window_size:
        return {
            "trend": "unknown",
            "confidence": 0,
            "net_inflow_total": 0,
            "net_inflow_recent": 0,
            "price_stage": "unknown"
        }

    # 计算总净流入
    net_inflow_total = sum(k["net_inflow"] for k in klines_data)

    # 计算最近窗口的净流入
    net_inflow_recent = sum(k["net_inflow"] for k in klines_data[-window_size:])

    # 计算净流入的移动平均
    window_inflows = []
    for i in range(len(klines_data) - window_size + 1):
        window_inflow = sum(k["net_inflow"] for k in klines_data[i:i + window_size])
        window_inflows.append(window_inflow)

    # 确定趋势
    trend = "neutral"
    if len(window_inflows) >= 3:
        recent_inflows = window_inflows[-3:]
        if all(x > 0 for x in recent_inflows) and recent_inflows[-1] > recent_inflows[-2]:
            trend = "increasing"
        elif all(x < 0 for x in recent_inflows) and recent_inflows[-1] < recent_inflows[-2]:
            trend = "decreasing"
        elif sum(1 for x in recent_inflows if x > 0) >= 2:
            trend = "slightly_increasing"
        elif sum(1 for x in recent_inflows if x < 0) >= 2:
            trend = "slightly_decreasing"

    # 计算趋势置信度
    if trend in ["increasing", "decreasing"]:
        confidence = 0.8
    elif trend in ["slightly_increasing", "slightly_decreasing"]:
        confidence = 0.6
    else:
        confidence = 0.4

    # 判断价格所处阶段
    price_stage = "unknown"
    if len(klines_data) >= 20:
        recent_prices = [k["close"] for k in klines_data[-20:]]
        price_changes = [recent_prices[i] - recent_prices[i - 1] for i in range(1, len(recent_prices))]

        # 计算价格变化的移动平均
        price_ma = sum(recent_prices) / len(recent_prices)
        latest_price = recent_prices[-1]

        # 计算价格波动率
        price_volatility = np.std(price_changes) / price_ma if price_ma > 0 else 0

        # 判断价格阶段
        if latest_price > price_ma * 1.05 and trend in ["increasing", "slightly_increasing"]:
            price_stage = "上涨中"
        elif latest_price < price_ma * 0.95 and trend in ["decreasing", "slightly_decreasing"]:
            price_stage = "下跌中"
        elif price_volatility < 0.01 and abs(latest_price - price_ma) / price_ma < 0.02:
            price_stage = "整理中"
        elif latest_price > price_ma * 1.08 and trend in ["decreasing", "slightly_decreasing"]:
            price_stage = "可能顶部"
        elif latest_price < price_ma * 0.92 and trend in ["increasing", "slightly_increasing"]:
            price_stage = "可能底部"
        else:
            price_stage = "波动中"

    return {
        "trend": trend,
        "confidence": confidence,
        "net_inflow_total": net_inflow_total,
        "net_inflow_recent": net_inflow_recent,
        "price_stage": price_stage
    }


def detect_anomalies(klines_data, window_size=10, threshold=2.0):
    """检测异常交易"""
    if not klines_data or len(klines_data) < window_size * 2:
        return {
            "has_anomalies": False,
            "anomalies": []
        }

    anomalies = []

    # 计算成交量和净流入的均值和标准差
    volumes = [k["volume"] for k in klines_data]
    inflows = [k["net_inflow"] for k in klines_data]

    volume_mean = np.mean(volumes)
    volume_std = np.std(volumes)
    inflow_mean = np.mean(inflows)
    inflow_std = np.std(inflows)

    # 检测异常成交量和净流入
    for i, kline in enumerate(klines_data):
        anomaly = {}

        # 检测异常成交量
        volume_z_score = (kline["volume"] - volume_mean) / volume_std if volume_std > 0 else 0
        if abs(volume_z_score) > threshold:
            anomaly["volume"] = {
                "value": kline["volume"],
                "z_score": volume_z_score,
                "direction": "high" if volume_z_score > 0 else "low"
            }

        # 检测异常净流入
        inflow_z_score = (kline["net_inflow"] - inflow_mean) / inflow_std if inflow_std > 0 else 0
        if abs(inflow_z_score) > threshold:
            anomaly["net_inflow"] = {
                "value": kline["net_inflow"],
                "z_score": inflow_z_score,
                "direction": "high" if inflow_z_score > 0 else "low"
            }

        # 检测价格和成交量不匹配的情况
        price_change = kline["price_change_pct"]
        if abs(price_change) > 1.0 and volume_z_score < 0:
            anomaly["price_volume_mismatch"] = {
                "price_change": price_change,
                "volume_z_score": volume_z_score
            }

        # 如果存在异常，添加到列表
        if anomaly:
            anomaly["time"] = kline["close_time"]
            anomalies.append(anomaly)

    return {
        "has_anomalies": len(anomalies) > 0,
        "anomalies": anomalies[-5:] if anomalies else []  # 只返回最近的5个异常
    }


def analyze_funding_pressure(klines_data, orderbook_stats):
    """分析资金压力"""
    if not klines_data or not orderbook_stats:
        return {
            "pressure_direction": "unknown",
            "confidence": 0,
            "imbalance": 0
        }

    # 获取订单簿不平衡度
    imbalance = orderbook_stats["imbalance"]

    # 获取最近的价格变化
    recent_klines = klines_data[-5:] if len(klines_data) >= 5 else klines_data
    recent_price_changes = [k["price_change_pct"] for k in recent_klines]
    avg_price_change = sum(recent_price_changes) / len(recent_price_changes) if recent_price_changes else 0

    # 判断资金压力方向
    pressure_direction = "neutral"
    if imbalance > 0.2 and avg_price_change > 0:
        pressure_direction = "upward_strong"
    elif imbalance > 0.1 and avg_price_change > 0:
        pressure_direction = "upward"
    elif imbalance < -0.2 and avg_price_change < 0:
        pressure_direction = "downward_strong"
    elif imbalance < -0.1 and avg_price_change < 0:
        pressure_direction = "downward"
    elif imbalance > 0.1 and avg_price_change < 0:
        pressure_direction = "potential_reversal_up"
    elif imbalance < -0.1 and avg_price_change > 0:
        pressure_direction = "potential_reversal_down"

    # 计算置信度
    confidence = abs(imbalance) * 2 if abs(imbalance) < 0.5 else 1.0

    return {
        "pressure_direction": pressure_direction,
        "confidence": confidence,
        "imbalance": imbalance,
        "bid_ask_ratio": orderbook_stats["pressure_ratio"]
    }


def format_number(num):
    """格式化数字，保留适当的小数位数"""
    if isinstance(num, (int, float)):
        if abs(num) >= 1000:
            return f"{num:.2f}"
        elif abs(num) >= 1:
            return f"{num:.4f}"
        else:
            return f"{num:.8f}"
    return num 