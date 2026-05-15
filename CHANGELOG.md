# 变更日志

## v0.5 (2026-05-16)

### 🎯 产品形态
- **可视化 UI**：Streamlit 本地界面，左侧参数 + 右侧结果，小白无需命令行
- **三步启动**：双击安装备用数据通道 → 双击启动 → 点击开始选股
- **产品首页**：README 顶部含截图预览、能力一览、已知限制、免责声明

### 🚀 小白体验
- 一键启动脚本 `start_ui.command`：分步检测 Python/虚拟环境/依赖/端口/启动，每步失败有中文下一步提示
- 备用数据通道安装脚本 `scripts/install_fallback.command`：Git/GitHub/权限问题的多方法解决 + 手动安装指引
- 环境自检页：首页展开即见 Python 版本/备用通道/本地缓存/最近选股，汇总判定就绪状态
- 四步引导：选参数 → 开始选股 → 看候选表格 → 看验证和报告
- 就绪状态：首页明确显示「✅ 可以开始选股」或具体缺失项

### 📊 数据
- akshare 主数据源 + skill_fallback（~120 条 K 线，6 个月）
- 本地缓存 `data/cache/*.parquet` 100+ 文件
- 股票池：static 55 只精选 A 股，含名称/行业元数据

### 🎯 选股
- 6 因子评分模型（data_quality / trend / momentum / volume / risk / pattern）
- 决策标签：strong_watch → watch → neutral → avoid
- 风险等级：low / medium / high
- 置信度：high / medium / low（覆盖不全时自动降权）

### ✅ 验证
- `validate`：选股结果质量评估（overall_quality / 覆盖不足率 / 置信度分布 / 决策分布 / 行业分布）
- `backtest-validate`：历史窗口 In-Sample 复盘（Forward 收益/最大回撤/波动率）
- `report`：Markdown 日报，含选股结果/数据来源/覆盖警告

### 📸 验收证据
- Playwright 自动截图脚本 `scripts/screenshot_home.py`
- 首页 + 结果页双截图持久化到 `docs/screenshots/`
- UI 验收报告 `docs/UI_ACCEPTANCE_RESULT.md`

### 📖 文档
- `docs/USER_GUIDE.md` — 小白使用指南（7 节：安装/启动/选股/看结果/常见问题/免责）
- `docs/TROUBLESHOOTING.md` — 10 个常见问题排障指南
- `docs/MANUAL_UI_CHECKLIST.md` — 手动验收清单
- `docs/MVP_ACCEPTANCE.md` — P7.2 MVP 验收记录
- `PROJECT_STATE.md` — 开发阶段/commit 记录/真实能力

### 🔧 CLI 验收入口
- `select` / `validate` / `backtest-validate` / `report` / `pipeline` / `selfcheck`

### ⚠️ 已知限制
- 数据覆盖：skill_fallback 约 120 条 K 线，请求较早日期触发「覆盖不全」
- akshare 不稳定：受网络影响经常失败，自动切换 fallback
- 选股等待：默认 10 只约 30-60 秒
- 非收益预测：评分为规则因子打分，不是 ML 预测
