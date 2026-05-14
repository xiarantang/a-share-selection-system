# 🏦 A 股智能选股系统 v0.1

> 七层架构实验版 · 项目骨架已建立

基于 **akshare + backtrader + a-share-skill** 的 A 股选股系统实验版。

**当前状态**: v0.1 — 数据层/策略层/回测层/报告层已接入（需通过 pipeline 验证数据源可用性）；AI 层和 Agent 层为实验模块。

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────┐
│                    main.py (总调度)                   │
├─────────────────────────────────────────────────────┤
│  报告层 │ reports/         ✅ Markdown/JSON 报告生成   │
│  实盘层 │ paper_trading/   ✅ 模拟盘引擎 (v0.1)       │
│  Agent层│ agent/           ⚠️  桥接器可用,需 API Key   │
│  AI层   │ ai_models/       🧪 qlib experimental      │
│  回测层 │ backtest/        ✅ backtrader A股适配      │
│  策略层 │ strategies/      ✅ Skill 注册+自动扫描     │
│  数据层 │ data/            ✅ akshare 全维度数据       │
├─────────────────────────────────────────────────────┤
│  配置层 │ config/          全局参数集中管理            │
└─────────────────────────────────────────────────────┘
```

## 📦 项目结构

```
a-share-selection-system/
├── main.py                  # 主入口（支持子命令）
├── scripts/pipeline.py      # 一键运行脚本
├── config/settings.py       # 全局配置
├── data/fetcher.py          # akshare 封装
├── strategies/registry.py   # Skill 注册调度
├── backtest/engine.py       # backtrader 回测引擎
├── ai_models/qlib_runner.py # qlib (experimental)
├── agent/bridge.py          # MCP + LLM 桥接
├── paper_trading/engine.py  # 模拟盘引擎
└── reports/generator.py     # 报告生成
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 安装 Skill
```bash
cd /tmp && git clone https://github.com/shouldnotappearcalm/a-share-skill.git
cp -R /tmp/a-share-skill/a-share-data ~/.agents/skills/
cp -R /tmp/a-share-skill/a-share-paper-trading ~/.agents/skills/
cp -R /tmp/a-share-skill/a-share-strategy-mainboard-multi-swing-defensive ~/.agents/skills/
cp -R /tmp/a-share-skill/macd-trend-resonance-stock-picker ~/.agents/skills/
cp -R /tmp/a-share-skill/macd-second-golden-cross ~/.agents/skills/
```

### 3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 填入 DeepSeek API Key（Agent 层需要）
```

## 📖 使用

```bash
# 模块检查（PASS/FAIL 表）
python main.py pipeline

# 数据获取
python main.py fetch --type kline --symbols 600519,000001,300750 --start 2024-01-01

# 策略管理
python main.py strategy
python main.py strategy --run

# 回测
python main.py backtest --symbol 000001

# 模拟交易
python main.py paper-trading

# 生成报告
python main.py report
```

## 🔗 集成项目

| 层级 | 项目 | 状态 |
|------|------|------|
| 数据 | [akshare](https://github.com/akfamily/akshare) | ✅ 已集成 |
| 策略 | [a-share-skill](https://github.com/shouldnotappearcalm/a-share-skill) | ✅ 3 个 Skill 已注册 |
| 回测 | [backtrader](https://github.com/mementum/backtrader) | ✅ A 股适配完成 |
| AI | [qlib](https://github.com/microsoft/qlib) | 🧪 experimental |
| Agent | [mcp-cn-a-stock](https://github.com/elsejj/mcp-cn-a-stock) | ⚠️  需 API Key |
| 报告 | 内置 | ✅ 可用 |

## 🧪 实验模块

以下模块代码已写但未真实跑通，标记为 experimental：
- `ai_models/qlib_runner.py` — 需先下载 qlib 数据
- `agent/bridge.py` — 需配置 DeepSeek API Key 和 MCP 服务地址

## ⚠️ 免责声明

本系统仅供研究学习使用，不构成投资建议。A 股市场风险较高，投资需谨慎。

## 📄 License

MIT
