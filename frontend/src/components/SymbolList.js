/**
 * 交易对列表组件
 * 用于显示和管理分析的交易对
 */

class SymbolList {
    constructor(container, initialSymbols = []) {
        this.container = container;
        this.symbols = initialSymbols;
        this.onSymbolsChanged = null;
        this.render();
    }

    /**
     * 添加交易对
     * @param {string} symbol - 待添加的交易对
     */
    addSymbol(symbol) {
        if (!symbol) return;
        
        // 转换为大写并去除空格
        const formattedSymbol = symbol.trim().toUpperCase();
        
        // 检查是否已存在
        if (!this.symbols.includes(formattedSymbol)) {
            this.symbols.push(formattedSymbol);
            this.render();
            
            // 触发变更回调
            if (this.onSymbolsChanged) {
                this.onSymbolsChanged(this.symbols);
            }
        }
    }

    /**
     * 移除交易对
     * @param {string} symbol - 待移除的交易对
     */
    removeSymbol(symbol) {
        const index = this.symbols.indexOf(symbol);
        if (index > -1) {
            this.symbols.splice(index, 1);
            this.render();
            
            // 触发变更回调
            if (this.onSymbolsChanged) {
                this.onSymbolsChanged(this.symbols);
            }
        }
    }

    /**
     * 获取当前的交易对列表
     * @returns {Array} - 交易对列表
     */
    getSymbols() {
        return [...this.symbols];
    }

    /**
     * 渲染组件
     */
    render() {
        // 清空容器
        this.container.innerHTML = '';
        
        // 创建标题
        const title = document.createElement('h4');
        title.textContent = '已添加的交易对';
        this.container.appendChild(title);
        
        // 如果没有交易对，显示提示
        if (this.symbols.length === 0) {
            const emptyMessage = document.createElement('p');
            emptyMessage.className = 'text-muted';
            emptyMessage.textContent = '未添加任何交易对，请在上方输入并添加';
            this.container.appendChild(emptyMessage);
            return;
        }
        
        // 创建交易对列表
        const list = document.createElement('div');
        list.className = 'symbol-list';
        
        this.symbols.forEach(symbol => {
            const symbolItem = document.createElement('div');
            symbolItem.className = 'symbol-item d-flex justify-content-between align-items-center mb-2';
            
            const symbolTag = document.createElement('span');
            symbolTag.className = 'symbol-tag';
            symbolTag.textContent = symbol;
            
            const removeButton = document.createElement('button');
            removeButton.className = 'btn btn-sm btn-danger';
            removeButton.innerHTML = '<i class="bi bi-x"></i>';
            removeButton.title = '删除';
            removeButton.onclick = () => this.removeSymbol(symbol);
            
            symbolItem.appendChild(symbolTag);
            symbolItem.appendChild(removeButton);
            list.appendChild(symbolItem);
        });
        
        this.container.appendChild(list);
    }
}

export default SymbolList; 