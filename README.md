# 🏦 A 股智能选股系统 v0.4

> 七层架构实验版 · 真实可用的批量选股系统

基于 **akshare + skill fallback + backtrader** 的 A 股选股系统。

**🎯 产品目标**：最终形态是小白也能用的可视化 A 股选股系统。CLI 命令是底层引擎和验收入口。当前已有 Streamlit 可视化界面（P6.0），后续将逐步产品化：一键选股 → 报告展示 → AI 辅助解释。暂不碰实盘交易。

> 继续开发请先阅读 PROJECT_STATE.md 和 NEXT_PROMPT.md

**当前真实能力**: 
- ✅ 数据层：akshare + 多源 fallback（腾讯/新浪/雪球/东财）+ 本地缓存
- ✅ 股票池：static(55只) / hs300 / top_amount / sample / manual，含名称行业元数据
- ✅ 批量选股：MA/MACD/RSI 五维评分，Top N 排序，CSV/JSON/Markdown 报告
- ✅ 回测层：backtrader A 股适配（佣金/印花税/T+1）
- ✅ 报告层：Markdown 日报，含选股结果+来源+覆盖警告
- ✅ 可视化：Streamlit 本地 UI（P6.0），小白一键选股/验证/复盘/报告
- ✅ Pipeline：PASS/FAIL 模块检查表，退出码可信
- 🧪 AI/Agent/qlib：experimental，未真实跑通（未来 P8 阶段，不参与当前小白启动）

**⚠️ 已知限制**：当前 fallback 数据仅约 120 条 K 线（~6 个月），请求 2024-01-01 会触发 coverage_warning。数据覆盖不足时不构成选股建议。

---

## 🚀 快速开始

### ⚡ 小白最快启动（三步）

1. **安装备用数据通道**（仅首次，约 1 分钟）  
   双击 `scripts/install_fallback.command`

2. **启动系统**  
   双击 `start_ui.command` → 浏览器自动打开 `http://localhost:8501`

3. **开始选股**  
   在页面左侧点击「🚀 开始选股」按钮 → 等待 30-60 秒 → 查看结果

> 💡 akshare 在部分网络环境下可能临时失败，系统会自动使用备用数据通道继续出结果；这不代表系统坏了。首次体验建议保持默认 **static + 10 只**。

### 🖥️ 小白一键启动（推荐）

**双击 `start_ui.command`** 即可自动完成以下步骤：
1. 检测 Python3 → 创建虚拟环境 → 安装轻量依赖 → 启动 Streamlit
2. 浏览器打开 **http://localhost:8501**

首次使用前建议先双击 **`scripts/install_fallback.command`** 安装 A 股备用数据通道。  
说明：`akshare` 在部分网络环境下可能临时失败，系统会自动使用备用数据通道继续出结果；这不代表系统坏了。

左侧栏选择股票池和参数，点击「🚀 开始选股」即可。首次体验建议保持默认 **static + 10 只**，通常需要 **30-60 秒**。选股完成后可切换 Tab 查看候选表格、验证摘要、历史复盘和完整报告。

### 🔧 开发者启动（命令行）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt        # 完整依赖（含回测/AI）
# 或：pip install -r requirements-ui.txt  # 轻量依赖（仅可视化）
.venv/bin/streamlit run app.py
```

### 小白首次安装数据通道（推荐）

双击：

```bash
scripts/install_fallback.command
```

它会自动安装 A 股备用数据通道。安装完成后，再双击 `start_ui.command` 启动系统。

### Skill 手动安装（数据 fallback）

```bash
cd /tmp && git clone https://github.com/shouldnotappearcalm/a-share-skill.git
cp -R /tmp/a-share-skill/a-share-data ~/.agents/skills/
cp -R /tmp/a-share-skill/a-share-paper-trading ~/.agents/skills/
cp -R /tmp/a-share-skill/a-share-strategy-mainboard-multi-swing-defensive ~/.agents/skills/
cp -R /tmp/a-share-skill/macd-trend-resonance-stock-picker ~/.agents/skills/
cp -R /tmp/a-share-skill/macd-second-golden-cross ~/.agents/skills/
```

## 📖 CLI 命令（开发者/验收入口）

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

### 验证结果

```bash
python3 main.py validate
python3 main.py validate --selection reports/output/selection_latest.json
```

### 历史复盘

```bash
python3 main.py backtest-validate
python3 main.py backtest-validate --selection reports/output/selection_latest.json --top 10
```
> 历史窗口复盘：对已有K线做 in-sample 验证，不代表未来收益。

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

## ❓ 常见问题

**Q: 启动后选股没有数据怎么办？**
A: 首次使用需要安装 A 股备用数据通道。优先双击 `scripts/install_fallback.command`，安装后重新点击「开始选股」即可。

**Q: akshare 失败是不是系统坏了？**
A: 不是。`akshare` 受网络和接口状态影响，失败很常见。当前系统会自动使用 A 股备用数据通道 `skill_fallback`，只要能看到候选表格，就是正常运行。

**Q: 开始选股后要等多久？**
A: 默认扫描 10 只股票通常需要 30-60 秒。数量越多等待越久。首次体验建议保持默认 static + 10 只。

**Q: 选股结果都带"⚠️ 覆盖不全"标志？**
A: 正常现象。当前备用数据通道约 120 条 K 线（约 6 个月），请求 2024-01-01 会触发 coverage_warning。模型已自动下调 data_quality 评分和 confidence 置信度；这不是报错，只表示结果更适合做研究观察。

**Q: 如何更新数据？**
A: 在界面左侧设置数据起始日期，重新点击「开始选股」即可。数据会自动缓存到 `data/cache/`。

**Q: 端口 8501 被占用怎么办？**
A: `start_ui.command` 会自动检测端口占用：
- 如果 8501 已被其他程序占用，自动尝试 8502
- 如果 8501 已有 Streamlit 在运行，会提示直接打开浏览器
- 手动指定端口：`.venv/bin/streamlit run app.py --server.port 8502`

**Q: 选股结果质量如何判断？**
A: 切换「验证摘要」Tab 查看 `overall_quality`。`good` 表示数据充足、风险可控；`usable_with_caution` 表示覆盖不足或置信度偏低。

**Q: 双击 start_ui.command 没反应？**
A: macOS 安全策略可能阻止。右键 → 打开，或在「系统设置 → 隐私与安全性」中允许。

---

## 📊 评分模型

当前为**规则因子评分模型**（非机器学习预测）。满分 100，分 6 组：

| 因子组 | 满分 | 说明 |
|--------|------|------|
| data_quality | 10 | 数据条数、覆盖完整性 |
| trend | 25 | MA5/MA20/MA60 多头排列 |
| momentum | 20 | 20日/60日涨跌幅、回撤 |
| volume | 15 | 量能放大倍数 |
| risk | 20 | RSI、追高风险、波动率（越高越好） |
| pattern | 10 | MACD、回踩形态 |

**决策标签**：strong_watch（强观察）→ watch（观察）→ neutral（中性）→ avoid（回避）
**风险等级**：low / medium / high
**置信度**：high / medium / low。coverage_warning 或 rows<120 时会降低 data_quality 和 confidence；若 confidence=low 或 data_quality 过低，decision 会被下调；若仍为 strong_watch，报告必须提示覆盖不足风险。

## 📋 验证摘要说明

`validate` 命令评估本次选股结果质量，不预测收益。`selection_latest.json` 自动包含 validation 字段。

**overall_quality**：
- `good` — 数据充足、风险可控
- `usable_with_caution` — 覆盖不足或置信度偏低
- `poor` — 无可用结果

**关键指标**：coverage_warning_ratio（覆盖不足比例）、confidence_dist（置信度分布）、decision_dist（决策分布）、risk_level_dist（风险分布）、sector_dist（行业分布）

## 🏗️ 架构

```
app.py                     # Streamlit 可视化界面 (P6.0)
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

## 📦 产物说明

`reports/output/` 下的文件：

| 文件 | 说明 |
|------|------|
| `selection_YYYYMMDD_HHMMSS.json` | 每次选股结果（时间戳命名） |
| `selection_YYYYMMDD_HHMMSS.csv` | 选股CSV |
| `selection_latest.json` | 最近一次选股（覆盖更新） |
| `selection_latest.csv` | 最近一次选股CSV |
| `report_YYYYMMDD_HHMMSS.md` | 每次报告（时间戳命名） |
| `report_latest.md` | 最近一次报告（覆盖更新） |

`data/cache/`：K线缓存文件，不提交 Git。

## 📄 License

MIT
