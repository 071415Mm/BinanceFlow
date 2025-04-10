/**
 * 控制面板组件
 * 用于设置分析参数和触发分析
 */

class ControlPanel {
    constructor(container) {
        this.container = container;
        this.intervals = ["5m", "15m", "30m", "1h", "4h", "1d"];
        this.selectedInterval = "1h";
        this.onAnalysisStart = null;
        this.symbolInput = '';
        this.onAddSymbol = null;
        this.isAnalyzing = false;
        this.render();
    }

    /**
     * 设置可用的K线时间间隔
     * @param {Array} intervals - 时间间隔列表
     */
    setIntervals(intervals) {
        if (Array.isArray(intervals) && intervals.length > 0) {
            this.intervals = intervals;
            this.render();
        }
    }

    /**
     * 获取选中的时间间隔
     * @returns {string} - 选中的时间间隔
     */
    getSelectedInterval() {
        return this.selectedInterval;
    }

    /**
     * 设置分析状态
     * @param {boolean} analyzing - 是否正在分析
     */
    setAnalyzing(analyzing) {
        this.isAnalyzing = analyzing;
        this.render();
    }

    /**
     * 渲染组件
     */
    render() {
        // 清空容器
        this.container.innerHTML = '';

        // 创建面板卡片
        const card = document.createElement('div');
        card.className = 'card';

        // 创建标题
        const title = document.createElement('h4');
        title.textContent = '分析设置';
        card.appendChild(title);

        // 创建交易对输入区域
        const symbolGroup = document.createElement('div');
        symbolGroup.className = 'mb-3';

        const symbolLabel = document.createElement('label');
        symbolLabel.textContent = '添加交易对';
        symbolLabel.className = 'form-label';
        symbolGroup.appendChild(symbolLabel);

        const symbolInputGroup = document.createElement('div');
        symbolInputGroup.className = 'input-group mb-3';

        const symbolInput = document.createElement('input');
        symbolInput.type = 'text';
        symbolInput.className = 'form-control';
        symbolInput.placeholder = '例如: BTCUSDT';
        symbolInput.value = this.symbolInput;
        symbolInput.disabled = this.isAnalyzing;
        symbolInput.oninput = (e) => {
            this.symbolInput = e.target.value;
        };
        symbolInput.onkeypress = (e) => {
            if (e.key === 'Enter' && this.onAddSymbol && !this.isAnalyzing) {
                this.onAddSymbol(this.symbolInput);
                this.symbolInput = '';
                symbolInput.value = '';
            }
        };
        symbolInputGroup.appendChild(symbolInput);

        const addButton = document.createElement('button');
        addButton.className = 'btn btn-primary';
        addButton.textContent = '添加';
        addButton.disabled = this.isAnalyzing;
        addButton.onclick = () => {
            if (this.onAddSymbol && !this.isAnalyzing) {
                this.onAddSymbol(this.symbolInput);
                this.symbolInput = '';
                symbolInput.value = '';
            }
        };
        symbolInputGroup.appendChild(addButton);

        symbolGroup.appendChild(symbolInputGroup);
        card.appendChild(symbolGroup);

        // 创建时间间隔选择区域
        const intervalGroup = document.createElement('div');
        intervalGroup.className = 'mb-3';

        const intervalLabel = document.createElement('label');
        intervalLabel.textContent = 'K线时间间隔';
        intervalLabel.className = 'form-label';
        intervalGroup.appendChild(intervalLabel);

        const intervalSelect = document.createElement('select');
        intervalSelect.className = 'form-select';
        intervalSelect.disabled = this.isAnalyzing;
        
        this.intervals.forEach(interval => {
            const option = document.createElement('option');
            option.value = interval;
            option.textContent = this.formatIntervalLabel(interval);
            option.selected = interval === this.selectedInterval;
            intervalSelect.appendChild(option);
        });
        
        intervalSelect.onchange = (e) => {
            this.selectedInterval = e.target.value;
        };
        
        intervalGroup.appendChild(intervalSelect);
        card.appendChild(intervalGroup);

        // 创建分析按钮
        const analyzeButton = document.createElement('button');
        analyzeButton.className = `btn w-100 ${this.isAnalyzing ? 'btn-danger' : 'btn-primary'}`;
        analyzeButton.textContent = this.isAnalyzing ? '正在分析...' : '开始分析';
        analyzeButton.disabled = this.isAnalyzing;
        analyzeButton.onclick = () => {
            if (this.onAnalysisStart && !this.isAnalyzing) {
                this.isAnalyzing = true;
                this.render();
                this.onAnalysisStart(this.selectedInterval);
            }
        };
        card.appendChild(analyzeButton);

        this.container.appendChild(card);
    }

    /**
     * 格式化时间间隔标签
     * @param {string} interval - 时间间隔代码
     * @returns {string} - 格式化后的标签
     */
    formatIntervalLabel(interval) {
        const labels = {
            '5m': '5分钟',
            '15m': '15分钟',
            '30m': '30分钟',
            '1h': '1小时',
            '4h': '4小时',
            '1d': '日线'
        };
        
        return labels[interval] || interval;
    }
}

export default ControlPanel; 