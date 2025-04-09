"""
AI服务
处理与DeepSeek API的交互，获取AI分析结果
"""

import requests
import json
import logging
import os
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API端点URL
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


def send_to_deepseek(data, interval="1h"):
    """将数据发送给DeepSeek API并获取解读"""
    # 在函数内部获取环境变量，确保每次调用都能获取到最新值
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
    
    if not DEEPSEEK_API_KEY:
        logger.error("DeepSeek API密钥未设置")
        raise Exception("DeepSeek API密钥未设置，请在环境变量中设置DEEPSEEK_API_KEY")
    
    logger.info(f"使用API密钥：{DEEPSEEK_API_KEY[:8]}...（部分隐藏）")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    # 根据不同时间间隔设置相应的分析参数
    interval_settings = {
        "5m": {
            "forecast_period": "未来2-6小时",
            "trade_horizon": "短线（数小时内）",
            "stop_loss_range": "较小（0.5%-1.5%）",
            "analysis_depth": "微观市场结构和短期波动",
            "position_sizing": "建议小仓位（5%-15%）"
        },
        "15m": {
            "forecast_period": "未来6-12小时",
            "trade_horizon": "短线至中短线（半天至1天）",
            "stop_loss_range": "中小（1%-2%）",
            "analysis_depth": "短期趋势和支撑阻力位",
            "position_sizing": "建议小至中等仓位（10%-20%）"
        },
        "30m": {
            "forecast_period": "未来12-24小时",
            "trade_horizon": "中短线（1-2天）",
            "stop_loss_range": "中等（1.5%-3%）",
            "analysis_depth": "日内趋势和关键价格区间",
            "position_sizing": "建议中等仓位（15%-25%）"
        },
        "1h": {
            "forecast_period": "未来1-3天",
            "trade_horizon": "中线（2-5天）",
            "stop_loss_range": "中等（2%-4%）",
            "analysis_depth": "中期趋势和市场结构转换",
            "position_sizing": "建议中等仓位（20%-30%）"
        },
        "4h": {
            "forecast_period": "未来3-7天",
            "trade_horizon": "中长线（1-2周）",
            "stop_loss_range": "中大（3%-6%）",
            "analysis_depth": "中长期趋势和市场周期",
            "position_sizing": "建议中至大仓位（25%-40%）"
        },
        "1d": {
            "forecast_period": "未来1-4周",
            "trade_horizon": "长线（2周-1个月）",
            "stop_loss_range": "较大（5%-10%）",
            "analysis_depth": "长期趋势、市场周期和宏观因素影响",
            "position_sizing": "建议大仓位或分批建仓（30%-50%）"
        }
    }

    # 获取当前时间间隔的设置
    interval_key = interval.lower()
    if interval_key not in interval_settings:
        interval_key = "1h"  # 默认使用1小时设置

    settings = interval_settings[interval_key]

    prompt = (
            f"## Binance资金流向专业分析任务 (K线周期: {interval})\n\n"
            f"我已收集了Binance现货和期货市场过去50根{interval}K线的资金流向数据（已剔除最新未完成的一根），包括：\n"
            "- 各交易对的资金流向趋势分析\n"
            "- 价格所处阶段预测（顶部、底部、上涨中、下跌中、整理中）\n"
            "- 订单簿数据（买卖盘不平衡度）\n"
            "- 资金压力分析\n"
            "- 异常交易检测\n\n"

            f"请从专业交易员和机构投资者角度，针对{interval}周期特点进行深度分析：\n\n"

            "1. **主力资金行为解读**：\n"
            "   - 通过资金流向趋势变化，识别主力资金的建仓、出货行为\n"
            "   - 结合订单簿数据，分析主力资金的意图（吸筹、出货、洗盘等）\n"
            "   - 特别关注资金流向与价格变化不匹配的异常情况\n"
            f"   - 重点分析{settings['analysis_depth']}\n\n"

            "2. **价格阶段判断**：\n"
            "   - 根据资金流向趋势和价格关系，判断各交易对处于什么阶段（顶部、底部、上涨中、下跌中、整理中）\n"
            "   - 提供判断的置信度和依据\n"
            "   - 对比不同交易对的阶段差异，分析可能的轮动关系\n"
            f"   - 结合{interval}周期特有的市场结构特征\n\n"

            "3. **趋势预判**：\n"
            f"   - 基于资金流向和资金压力分析，预判{settings['forecast_period']}可能的价格走势\n"
            "   - 识别可能的反转信号或趋势延续信号\n"
            "   - 关注异常交易数据可能暗示的行情变化\n"
            f"   - 给出具体的价格目标区间和时间预期\n\n"

            "4. **交易策略建议**：\n"
            "   - 针对每个交易对，给出具体的交易建议（观望、做多、做空、减仓等）\n"
            f"   - 提供适合{settings['trade_horizon']}的入场点位和止损位\n"
            f"   - 建议止损范围：{settings['stop_loss_range']}\n"
            f"   - {settings['position_sizing']}\n"
            "   - 评估风险和回报比\n\n"

            "请使用专业术语，保持分析简洁但深入，避免泛泛而谈。数据如下：\n\n" +
            json.dumps(data, indent=2, ensure_ascii=False) +
            "\n\n回复格式要求：中文，使用markdown格式，重点突出，适当使用表格对比分析。"
    )

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.7
    }

    try:
        logger.info("正在发送数据到DeepSeek API...")
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # 检查响应内容类型
        content_type = response.headers.get('content-type', '')
        if 'application/json' not in content_type:
            logger.error(f"意外的响应类型: {content_type}")
            logger.error(f"响应内容: {response.text[:500]}...")  # 只记录前500个字符
            raise Exception("DeepSeek API返回了非JSON响应")
            
        try:
            result = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
            logger.error(f"响应内容: {response.text[:500]}...")
            raise Exception("无法解析DeepSeek API的响应")
            
        if 'choices' not in result or not result['choices']:
            logger.error(f"API响应格式错误: {result}")
            raise Exception("DeepSeek API响应格式不正确")
            
        logger.info("成功获取DeepSeek API响应")
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        logger.error(f"DeepSeek API请求错误: {e}")
        raise Exception(f"AI分析失败: 网络请求错误 - {str(e)}")
    except Exception as e:
        logger.error(f"DeepSeek API error: {e}")
        raise Exception(f"AI分析失败: {str(e)}") 