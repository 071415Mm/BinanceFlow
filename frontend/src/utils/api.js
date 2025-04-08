/**
 * API工具模块
 * 用于处理前端与后端API的交互
 */

// API基础URL，基于当前窗口域名构建
const API_BASE_URL = (window.location.origin || 'http://localhost:5000') + '/api';

/**
 * 发送HTTP请求
 * @param {string} endpoint - API端点
 * @param {string} method - HTTP方法
 * @param {Object} data - 请求数据
 * @returns {Promise} - HTTP响应
 */
async function fetchAPI(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || '请求失败');
        }
        
        return await response.json();
    } catch (error) {
        console.error(`API请求失败: ${error.message}`);
        throw error;
    }
}

/**
 * 获取默认交易对列表
 * @returns {Promise} - 包含默认交易对的响应
 */
export async function getDefaultSymbols() {
    return fetchAPI('/symbols');
}

/**
 * 获取可用的K线时间间隔
 * @returns {Promise} - 包含可用时间间隔的响应
 */
export async function getIntervals() {
    return fetchAPI('/intervals');
}

/**
 * 分析交易对资金流向
 * @param {Array} symbols - 交易对列表
 * @param {string} interval - K线时间间隔
 * @returns {Promise} - 分析结果
 */
export async function analyzeSymbols(symbols, interval) {
    return fetchAPI('/analyze', 'POST', { symbols, interval });
}

/**
 * 检查API服务健康状态
 * @returns {Promise} - 健康状态响应
 */
export async function checkHealth() {
    return fetchAPI('/health');
}

export default {
    getDefaultSymbols,
    getIntervals,
    analyzeSymbols,
    checkHealth
}; 