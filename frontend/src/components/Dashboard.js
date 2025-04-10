/**
 * 仪表盘组件
 * 作为前端的主容器，协调其他组件
 */

import SymbolList from './SymbolList.js';
import ControlPanel from './ControlPanel.js';
import AnalysisResults from './AnalysisResults.js';
import * as api from '../utils/api.js';

class Dashboard {
    constructor(container) {
        this.container = container;
        this.init();
    }

    /**
     * 初始化仪表盘
     */
    async init() {
        this.render();
        
        // 加载默认交易对
        try {
            const response = await api.getDefaultSymbols();
            if (response.status === 'success') {
                this.symbolList.symbols = response.data;
                this.symbolList.render();
            }
        } catch (error) {
            console.error('加载默认交易对失败:', error);
        }
        
        // 加载可用时间间隔
        try {
            const response = await api.getIntervals();
            if (response.status === 'success') {
                this.controlPanel.setIntervals(response.data);
            }
        } catch (error) {
            console.error('加载时间间隔失败:', error);
        }
    }

    /**
     * 渲染仪表盘
     */
    render() {
        // 清空容器
        this.container.innerHTML = '';
        
        // 创建导航栏
        const navbar = document.createElement('nav');
        navbar.className = 'navbar navbar-dark bg-dark';
        
        const navbarContainer = document.createElement('div');
        navbarContainer.className = 'container-fluid';
        
        const brand = document.createElement('span');
        brand.className = 'navbar-brand mb-0 h1';
        brand.innerHTML = '<i class="bi bi-currency-bitcoin me-2"></i>币安资金流向分析系统';
        
        navbarContainer.appendChild(brand);
        navbar.appendChild(navbarContainer);
        this.container.appendChild(navbar);
        
        // 创建主体内容
        const main = document.createElement('div');
        main.className = 'container-fluid';
        
        const row = document.createElement('div');
        row.className = 'row';
        
        // 创建侧边栏
        const sidebar = document.createElement('div');
        sidebar.className = 'col-md-3 col-lg-2 sidebar p-0';
        
        const sidebarContent = document.createElement('div');
        sidebarContent.className = 'p-3';
        
        // 控制面板容器
        const controlPanelContainer = document.createElement('div');
        sidebar.appendChild(sidebarContent);
        sidebarContent.appendChild(controlPanelContainer);
        
        // 交易对列表容器
        const symbolListContainer = document.createElement('div');
        symbolListContainer.className = 'mt-4';
        sidebarContent.appendChild(symbolListContainer);
        
        row.appendChild(sidebar);
        
        // 创建主内容区域
        const content = document.createElement('div');
        content.className = 'col-md-9 col-lg-10 ms-sm-auto px-md-4 py-4';
        
        // 分析结果容器
        const resultsContainer = document.createElement('div');
        content.appendChild(resultsContainer);
        
        row.appendChild(content);
        main.appendChild(row);
        this.container.appendChild(main);
        
        // 初始化组件
        this.controlPanel = new ControlPanel(controlPanelContainer);
        this.symbolList = new SymbolList(symbolListContainer);
        this.analysisResults = new AnalysisResults(resultsContainer);
        
        // 设置事件处理
        this.controlPanel.onAddSymbol = (symbol) => {
            this.symbolList.addSymbol(symbol);
        };
        
        this.symbolList.onSymbolsChanged = (symbols) => {
            // 可以在这里处理交易对变更事件
            console.log('交易对列表已更新:', symbols);
        };
        
        this.controlPanel.onAnalysisStart = (interval) => {
            this.startAnalysis(interval);
        };
    }
    
    /**
     * 开始分析
     * @param {string} interval - 时间间隔
     */
    async startAnalysis(interval) {
        const symbols = this.symbolList.getSymbols();
        
        // 检查是否有交易对
        if (symbols.length === 0) {
            this.analysisResults.setError('请至少添加一个交易对');
            this.controlPanel.setAnalyzing(false);
            return;
        }
        
        // 显示加载状态
        this.analysisResults.setLoading(true);
        
        try {
            // 发送分析请求
            const response = await api.analyzeSymbols(symbols, interval);
            
            // 处理响应
            if (response.status === 'success') {
                this.analysisResults.setResults(response.data);
            } else {
                this.analysisResults.setError(response.message || '分析请求失败');
            }
        } catch (error) {
            this.analysisResults.setError(error.message || '分析过程中发生错误');
        } finally {
            // 无论成功还是失败，都重置分析状态
            this.controlPanel.setAnalyzing(false);
        }
    }
}

export default Dashboard; 