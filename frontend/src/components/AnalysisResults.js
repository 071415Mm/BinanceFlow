/**
 * 分析结果组件
 * 用于显示分析结果
 */

class AnalysisResults {
    constructor(container) {
        this.container = container;
        this.results = null;
        this.isLoading = false;
        this.error = null;
        this.render();
    }

    /**
     * 设置加载状态
     * @param {boolean} isLoading - 是否正在加载
     */
    setLoading(isLoading) {
        this.isLoading = isLoading;
        this.error = null;
        this.render();
    }

    /**
     * 设置结果数据
     * @param {Object} results - 分析结果数据
     */
    setResults(results) {
        this.results = results;
        this.isLoading = false;
        this.error = null;
        this.render();
    }

    /**
     * 设置错误信息
     * @param {string} error - 错误信息
     */
    setError(error) {
        this.error = error;
        this.isLoading = false;
        this.render();
    }

    /**
     * 清除结果
     */
    clearResults() {
        this.results = null;
        this.isLoading = false;
        this.error = null;
        this.render();
    }

    /**
     * 渲染组件
     */
    render() {
        // 清空容器
        this.container.innerHTML = '';

        // 如果正在加载，显示加载动画
        if (this.isLoading) {
            const loadingContainer = document.createElement('div');
            loadingContainer.className = 'd-flex flex-column align-items-center justify-content-center my-5';
            
            const spinner = document.createElement('div');
            spinner.className = 'loading-spinner';
            
            const loadingText = document.createElement('p');
            loadingText.className = 'mt-3';
            loadingText.textContent = '正在分析，请稍候...';
            
            loadingContainer.appendChild(spinner);
            loadingContainer.appendChild(loadingText);
            
            this.container.appendChild(loadingContainer);
            return;
        }

        // 如果有错误，显示错误信息
        if (this.error) {
            const errorContainer = document.createElement('div');
            errorContainer.className = 'alert alert-danger mt-4';
            
            const errorTitle = document.createElement('h4');
            errorTitle.textContent = '分析过程中发生错误';
            
            const errorMessage = document.createElement('p');
            errorMessage.textContent = this.error;
            
            errorContainer.appendChild(errorTitle);
            errorContainer.appendChild(errorMessage);
            
            this.container.appendChild(errorContainer);
            return;
        }

        // 如果没有结果，显示欢迎信息
        if (!this.results) {
            const welcomeContainer = document.createElement('div');
            welcomeContainer.className = 'text-center my-5';
            
            const welcomeTitle = document.createElement('h2');
            welcomeTitle.textContent = '欢迎使用币安资金流向分析系统';
            
            const welcomeText = document.createElement('p');
            welcomeText.className = 'lead';
            welcomeText.textContent = '请在左侧添加交易对并点击"开始分析"按钮开始分析';
            
            welcomeContainer.appendChild(welcomeTitle);
            welcomeContainer.appendChild(welcomeText);
            
            // 添加系统介绍
            const introContainer = document.createElement('div');
            introContainer.className = 'card mt-4';
            
            const introTitle = document.createElement('h3');
            introTitle.className = 'card-header';
            introTitle.textContent = '系统功能';
            
            const introBody = document.createElement('div');
            introBody.className = 'card-body';
            
            const introList = document.createElement('ul');
            introList.innerHTML = `
                <li>资金流向趋势分析：分析现货和期货市场的资金流入流出趋势</li>
                <li>主力资金行为解读：识别主力资金的建仓、出货行为</li>
                <li>价格阶段判断：判断各交易对处于什么阶段（顶部、底部、上涨中、下跌中、整理中）</li>
                <li>短期趋势预判：预判未来可能的价格走势</li>
                <li>交易策略建议：针对每个交易对，给出具体的交易建议</li>
            `;
            
            introBody.appendChild(introList);
            introContainer.appendChild(introTitle);
            introContainer.appendChild(introBody);
            
            welcomeContainer.appendChild(introContainer);
            this.container.appendChild(welcomeContainer);
            return;
        }

        // 显示分析结果
        const resultsContainer = document.createElement('div');
        resultsContainer.className = 'analysis-container';

        // 添加标题和元数据
        const header = document.createElement('div');
        header.className = 'mb-4';

        const title = document.createElement('h2');
        title.textContent = '资金流向分析结果';
        
        const metadata = document.createElement('p');
        metadata.className = 'text-muted';
        metadata.textContent = `分析周期：${this.results.metadata.interval} | 分析时间：${this.results.metadata.analysis_time} | 耗时：${Math.round(this.results.metadata.duration)}秒`;
        
        header.appendChild(title);
        header.appendChild(metadata);
        resultsContainer.appendChild(header);

        // 添加分析结果内容
        const content = document.createElement('div');
        content.className = 'markdown-content';
        
        // 使用marked库渲染Markdown内容
        content.innerHTML = marked.parse(this.results.ai_interpretation);
        
        resultsContainer.appendChild(content);
        this.container.appendChild(resultsContainer);
    }
}

export default AnalysisResults; 