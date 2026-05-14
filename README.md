# 🏦 A 股智能选股系统

> 七层架构 · AI 驱动 · 全流程自动化

基于 **akshare + backtrader + qlib + a-share-skill + MCP** 的完整 A 股选股系统。

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────┐
│                    main.py (总调度)                   │
├─────────────────────────────────────────────────────┤
│  报告层 │ reports/         Markdown/JSON 报告生成     │
│  实盘层 │ paper_trading/   模拟盘 + 实盘接口预留       │
│  Agent层│ agent/           MCP桥接 + LLM 分析         │
│  AI层   │ ai_models/       微软 qlib 机器学习选股      │
│  回测层 │ backtest/        backtrader A股适配         │
│  策略层 │ strategies/      a-share-skill 策略调度     │
│  数据层 │ data/            akshare 全维度数据         │
├─────────────────────────────────────────────────────┤
│  配置层 │ config/          全局参数集中管理            │
└─────────────────────────────────────────────────────┘
```

## 📦 项目结构

```
a-share-selection-system/
├── main.py                  # 主入口，支持子命令
├── scripts/pipeline.py      # 一键运行脚本
├── config/                  # 配置层
│   └── settings.py          # 全局配置（dataclass）
├── data/                    # 数据层
│   └── fetcher.py           # akshare 封装（行情/财务/资金流/技术指标）
├── strategies/              # 策略层
│   └── registry.py          # a-share-skill 策略注册与调度
├── backtest/                # 回测层
│   └── engine.py            # backtrader A股回测引擎（T+1/手续费/印花税）
├── ai_models/               # AI/ML 层
│   └── qlib_runner.py       # 微软 qlib 集成（因子工程+LightGBM训练）
├── agent/                   # Agent 层
│   └── bridge.py            # MCP桥接 + DeepSeek LLM 分析
├── paper_trading/           # 模拟交易层
│   └── engine.py            # A股模拟盘引擎（100股/T+1/涨跌停）
└── reports/                 # 报告层
    └── generator.py         # Markdown/JSON 报告生成
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

核心依赖：`akshare` `backtrader` `pyqlib` `pandas` `numpy` `matplotlib` `requests` `loguru`

### 2. 安装 Skill

```bash
# 克隆 a-share-skill
cd /tmp && git clone https://github.com/shouldnotappearcalm/a-share-skill.git

# 安装到 Agent skills 目录
cp -R /tmp/a-share-skill/a-share-data ~/.agents/skills/
cp -R /tmp/a-share-skill/a-share-paper-trading ~/.agents/skills/
cp -R /tmp/a-share-skill/a-share-strategy-mainboard-multi-swing-defensive ~/.agents/skills/
cp -R /tmp/a-share-skill/macd-trend-resonance-stock-picker ~/.agents/skills/
cp -R /tmp/a-share-skill/macd-second-golden-cross ~/.agents/skills/
cp -R /tmp/a-share-skill/tuige-shortline-trading ~/.agents/skills/
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入 DeepSeek API Key
```

### 4. （可选）下载 qlib 数据

```bash
python -m qlib.cli.data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn
```

## 📖 使用

```bash
# 一键全流程检查
python main.py pipeline

# 查看实时行情
python main.py fetch --type quote --symbols 000001,600519

# 查看全市场概况
python main.py fetch --type market

# 列出已注册策略
python main.py strategy

# 执行全部策略
python main.py strategy --run

# 运行回测（000001 双均线策略）
python main.py backtest --symbol 000001

# AI 选股（需要 qlib 数据）
python main.py ai

# Agent 分析某只股票
python main.py agent --analyze 600519

# 查看模拟账户
python main.py paper-trading

# 生成报告
python main.py report
```

## 🔗 集成项目

| 层级 | 项目 | 作用 |
|------|------|------|
| 数据 | [akshare](https://github.com/akfamily/akshare) | A 股全维度数据接口 |
| 策略 | [a-share-skill](https://github.com/shouldnotappearcalm/a-share-skill) | 6 套选股策略 Skill |
| 回测 | [backtrader](https://github.com/mementum/backtrader) | Python 事件驱动回测 |
| AI | [qlib](https://github.com/microsoft/qlib) + [RD-Agent](https://github.com/microsoft/RD-Agent) | 微软 AI 量化平台 |
| Agent | [mcp-cn-a-stock](https://github.com/elsejj/mcp-cn-a-stock) | A 股 MCP 数据服务 |
| Agent | DeepSeek API | LLM 分析与报告生成 |

## ⚠️ 免责声明

本系统仅供研究学习使用，不构成投资建议。A 股市场风险较高，投资需谨慎。

## 📄 License

MIT
