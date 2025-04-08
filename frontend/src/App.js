/**
 * 应用入口文件
 * 负责初始化应用
 */

import Dashboard from './components/Dashboard.js';

// 在DOM加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    // 获取应用容器
    const appContainer = document.getElementById('app');
    
    // 如果找不到容器，记录错误并退出
    if (!appContainer) {
        console.error('找不到应用容器元素 #app');
        return;
    }
    
    // 初始化仪表盘
    const dashboard = new Dashboard(appContainer);
    
    // 在全局对象上存储仪表盘实例，便于调试
    window.dashboard = dashboard;
    
    console.log('币安资金流向分析系统已启动');
}); 