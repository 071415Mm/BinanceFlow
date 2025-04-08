# 币安资金流向分析系统

## 项目简介

这是一个专业的加密货币资金流向分析工具，采用前后端分离的架构设计，主要通过分析Binance交易所的现货和期货市场数据，提供深度的市场洞察和交易策略建议。该工具结合K线数据、订单簿深度和DeepSeek AI模型，为交易者提供全面的市场分析。

## 项目架构

项目采用前后端分离的架构：

### 后端
- 基于Flask框架构建的REST API
- 模块化设计，功能清晰分离
- 支持跨域资源共享(CORS)
- 提供数据获取、分析和AI解读功能

### 前端
- 纯JavaScript实现，无需额外构建工具
- 组件化架构，每个组件负责特定功能
- 响应式设计，适配各种屏幕尺寸
- 使用Bootstrap进行样式设计

## 主要功能

1. **资金流向分析**
   - 分析现货和期货市场的资金流入/流出趋势
   - 识别主力资金的建仓、出货行为
   - 对比不同交易对的资金流向差异

2. **市场阶段判断**
   - 自动判断市场所处阶段（顶部、底部、上涨中、下跌中、整理中）
   - 提供判断的置信度和具体依据
   - 分析不同交易对之间可能存在的轮动关系

3. **订单簿深度分析**
   - 计算买卖盘不平衡度
   - 分析关键价格区间内的买卖盘压力
   - 结合资金流向评估市场压力方向和强度

4. **异常交易检测**
   - 识别成交量异常但价格变化不大的情况
   - 检测价格异常波动但成交量不高的情况
   - 发现极端资金净流入/流出的异常交易

5. **AI驱动的专业分析**
   - 通过DeepSeek API提供专业交易员视角的市场解读
   - 生成短期趋势预判和交易策略建议
   - 输出结构化的markdown格式分析报告

## 安装与运行

### 环境要求
- Python 3.8+
- 现代浏览器（Chrome、Firefox、Edge等）

### 安装步骤

1. 克隆项目到本地
   ```
   git clone <repository-url>
   cd FlowTrack-Crypto
   ```

2. 安装依赖
   ```
   pip install -r requirements.txt
   ```

3. 设置环境变量
   - Windows:
     ```
     set DEEPSEEK_API_KEY=您的DeepSeek API密钥
     set BINANCE_API_KEY=您的Binance API密钥(可选)
     set BINANCE_API_SECRET=您的Binance API密钥(可选)
     ```
   - Linux/Mac:
     ```
     export DEEPSEEK_API_KEY=您的DeepSeek API密钥
     export BINANCE_API_KEY=您的Binance API密钥(可选)
     export BINANCE_API_SECRET=您的Binance API密钥(可选)
     ```

4. 运行应用
   ```
   python run.py
   ```
   
   应用将在 http://localhost:5000 上运行，并自动打开浏览器。

### 命令行选项

```
usage: run.py [-h] [-H HOST] [-p PORT] [-d] [-n]

启动币安资金流向分析系统

optional arguments:
  -h, --help            显示帮助信息并退出
  -H HOST, --host HOST  API服务器主机地址 (默认: 127.0.0.1)
  -p PORT, --port PORT  API服务器端口 (默认: 5000)
  -d, --debug           启用调试模式
  -n, --no-browser      不自动打开浏览器
```

## 使用方法

1. 在左侧面板添加要分析的交易对（例如：BTCUSDT、ETHUSDT等）
2. 选择K线时间间隔（5分钟、15分钟、30分钟、1小时、4小时，日线）
3. 点击"开始分析"按钮，等待分析完成
4. 分析完成后，查看右侧的详细分析结果

## 项目结构

```
FlowTrack-Crypto/
├── backend/
│   ├── api/
│   │   ├── routes.py      # API端点定义
│   │   └── api_server.py  # API服务器
│   ├── services/
│   │   ├── binance_service.py  # 币安数据服务
│   │   ├── analysis_service.py # 分析服务
│   │   └── ai_service.py       # AI服务
│   └── utils/
│       └── helpers.py     # 辅助函数
├── frontend/
│   ├── src/
│   │   ├── App.js                   # 应用入口
│   │   ├── components/
│   │   │   ├── Dashboard.js         # 主仪表盘
│   │   │   ├── SymbolList.js        # 交易对列表
│   │   │   ├── AnalysisResults.js   # 分析结果
│   │   │   └── ControlPanel.js      # 控制面板
│   │   ├── styles/
│   │   │   └── main.css             # 样式文件
│   │   └── utils/
│   │       └── api.js               # API调用
│   └── public/
│       └── index.html               # HTML入口
├── run.py                # 主运行脚本
└── requirements.txt      # 依赖列表
```

## 注意事项

1. DeepSeek API密钥必须设置才能使用AI分析功能
2. Binance API密钥是可选的，但设置后可以提高API调用限制
3. 分析结果仅供参考，不构成投资建议
4. 请遵守Binance API使用条款，避免过于频繁的请求

## 许可证

MIT

## 贡献

欢迎提交问题和贡献代码，请遵循以下步骤：
1. Fork 该仓库
2. 创建您的特性分支 (git checkout -b feature/amazing-feature)
3. 提交您的更改 (git commit -m 'Add some amazing feature')
4. 推送到分支 (git push origin feature/amazing-feature)
5. 创建一个 Pull Request


