# 🏦 A 股智能选股系统 v0.4

> 七层架构实验版 · 真实可用的批量选股系统

基于 **akshare + skill fallback + backtrader** 的 A 股选股系统。

**当前真实能力**: 
- ✅ 数据层：akshare + 多源 fallback（腾讯/新浪/雪球/东财）+ 本地缓存
- ✅ 股票池：static(55只) / hs300 / top_amount / sample / manual，含名称行业元数据
- ✅ 批量选股：MA/MACD/RSI 五维评分，Top N 排序，CSV/JSON/Markdown 报告
- ✅ 回测层：backtrader A 股适配（佣金/印花税/T+1）
- ✅ 报告层：Markdown 日报，含选股结果+来源+覆盖警告
- ✅ Pipeline：PASS/FAIL 模块检查表，退出码可信
- 🧪 AI/Agent/qlib：experimental，未真实跑通

**⚠️ 已知限制**：当前 fallback 数据仅约 120 条 K 线（~6 个月），请求 2024-01-01 会触发 coverage_warning。数据覆盖不足时不构成选股建议。

---

## 🚀 快速开始

```bash
pip install -r requirements.txt
```

### Skill 安装（数据 fallback）

```bash
cd /tmp && git clone https://github.com/shouldnotappearcalm/a-share-skill.git
cp -R /tmp/a-share-skill/a-share-data ~/.agents/skills/
cp -R /tmp/a-share-skill/a-share-paper-trading ~/.agents/skills/
cp -R /tmp/a-share-skill/a-share-strategy-mainboard-multi-swing-defensive ~/.agents/skills/
cp -R /tmp/a-share-skill/macd-trend-resonance-stock-picker ~/.agents/skills/
cp -R /tmp/a-share-skill/macd-second-golden-cross ~/.agents/skills/
```

## 📖 命令

### 查看股票池

```bash
python3 main.py universe --universe static --limit 50
python3 main.py universe --universe hs300 --limit 50
python3 main.py universe --universe top_amount --limit 50
```

### 批量选股

```bash
python3 main.py select --universe static --limit 50 --top 10 --start 2024-01-01
python3 main.py select --universe hs300 --limit 50 --top 10 --start 2024-01-01
python3 main.py select --universe top_amount --limit 50 --top 10 --start 2024-01-01
python3 main.py select --symbols 600519,000001,300750 --top 3
```

### 生成报告

```bash
python3 main.py report
python3 main.py report --selection reports/output/selection_20260514.json
```

### 模块检查

```bash
python3 main.py pipeline
```

### 其他

```bash
python3 main.py selfcheck              # 数据源自检
python3 main.py fetch --type kline ... # 数据获取
python3 main.py backtest --symbol 000001  # 回测
python3 main.py paper-trading          # 模拟交易
```

## 🏗️ 架构

```
config/settings.py         # 全局配置
data/
  fetcher.py              # akshare + fallback + 缓存
  universe.py             # 股票池 (static/hs300/top_amount)
  static_universe.json    # 55只A股元数据
strategies/
  selection.py            # 选股引擎 (MA/MACD/RSI 评分)
  registry.py             # Skill 策略注册
backtest/engine.py        # backtrader 回测
reports/generator.py      # Markdown 报告
ai_models/qlib_runner.py  # 🧪 experimental
agent/bridge.py           # 🧪 experimental (需 API Key)
paper_trading/engine.py   # 模拟交易
```

## 🔗 集成项目

| 项目 | 状态 |
|------|------|
| [akshare](https://github.com/akfamily/akshare) | ✅ 已集成 |
| [a-share-skill](https://github.com/shouldnotappearcalm/a-share-skill) | ✅ fallback + 策略 |
| [backtrader](https://github.com/mementum/backtrader) | ✅ A股适配 |
| [qlib](https://github.com/microsoft/qlib) | 🧪 experimental |

## ⚠️ 免责声明

本系统由程序根据数据和规则自动生成选股结果，仅供研究学习，不构成投资建议。A 股市场风险较高，投资需谨慎。

## 📄 License

MIT
