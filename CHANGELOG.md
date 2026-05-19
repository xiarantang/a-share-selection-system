# 变更日志

> 以下为 v0.5 发布时的基线记录。v0.5 之后经历了 P8.1–P8.7 持续增强（数据层升级为 baostock、UI 体验优化、策略管理等），当前已进入发布候选完成态。详见 [PROJECT_STATE.md](PROJECT_STATE.md)。

## v0.6-rc1 (2026-05-19，已打 tag)

### 数据层
- **baostock 集成**：主数据源由 skill_fallback（~120 条 K 线）升级为 baostock（稳定 ~570 条日 K），覆盖不足率从 100% 降为 0%，整体质量从 `usable_with_caution` 提升为 `good`
- **三级降级链路**：akshare → baostock → skill_fallback + 本地缓存，akshare 网络波动时自动降级
- **覆盖提示修正**：570 条 baostock 数据不再误报覆盖不足

### 策略解释
- **explain 字段**：每只候选新增小白解释（summary / strengths / weaknesses / risk_note / confidence_note），从已有因子和规则生成，不改评分排序
- **三端展示**：CLI JSON + Markdown 报告 + Streamlit UI 均展示解释字段，老数据优雅降级

### UI 体验优化
- **Top3 速览卡片**：结果页首屏展示前 3 名候选，含排名、评分、中文决策/风险/置信度标签
- **中文标签映射**：决策（强观察/观察/中性/回避）、风险（低/中/高）、置信度（高/中/低），仅 UI 展示层，底层 JSON 保持英文
- **风险分级着色**：低风险绿色、中风险橙色、高风险红色，统一 Top3 卡片与逐只详情视觉风格
- **因子图标化**：6 因子添加中文标签和小图标（趋势/动量/量能/风控/数据质量/形态）
- **技术指标折叠**：MA/RSI/波动率等移入默认收起的 expander，首屏更清爽
- **数据概览紧凑化**：4 列紧凑展示替代 st.metric 大字号，长文本不再截断

### 策略管理
- **策略注册表**：元数据注册中心（id / name / description / suitable_scenario / risk_reminder），替代旧 Skill 脚本执行模式
- **CLI `--strategy` 参数**：select 子命令新增可选参数，无效策略不触发数据拉取
- **UI 策略选择器**：侧栏股票池下方选择策略，结果页展示策略名称/适用场景/风险提醒
- **AI 辅助解释边界评审**：结论为暂缓实现，明确硬性禁止项

### UI 兼容性
- **废弃 API 清理**：`use_container_width` → `width="stretch"`、`applymap` → `map`，消除 Streamlit/Pandas 废弃警告
- **版本约束升级**：streamlit ≥ 1.39.0、pandas ≥ 2.1.0

### 复盘记录增强（P9.3）
- **run_metadata 字段**：每次选股自动记录 9 字段（生成时间/入口/命令/参数/策略/数据摘要/结果摘要/路径），不重跑评分
- **Markdown 报告**：新增「本次运行复盘信息」小节
- **Streamlit UI**：数据概览下方新增默认收起的复盘信息折叠区
- **独立验收**：confirm_run_metadata.py 20 项自动检查

### 验收体系增强（P9.2-P9.4）
- **文档一致性检查**：confirm_docs_consistency.py 19 项自动检查（主路径表述/数据层/禁词/免责声明）
- **排障体验验收**：confirm_troubleshooting.py 13 项自动检查（权限/语法/关键词/禁词/fallback 可选）
- **发布前一键验收**：confirm_release_ready.py 聚合 12 项检查
- **UI 自动验收**：confirm_p83_ui.py 44 项检查（静态文案 + JSON 运行时 + 截图）

### 排障与体验增强（P9.4）
- **公开排障文档**：TROUBLESHOOTING.md 口径修正（数据源顺序/端口说明/安装失败路径/主路径表述）
- **FAQ 扩充**：USER_GUIDE.md 从 5 条扩充到 8 条（新增浏览器/安装失败/全部失败）
- **UI 提示增强**：选股 spinner/全部失败/error/warning 均增加白话说明和排障指引
- **启动脚本增强**：start_ui.command 提示加入主路径和排障文档引用

### 发布边界收口（P9.5）
- **RELEASE_CHECKLIST.md 更新**：对齐当前 12 项一键验收口径
- **fallback 可选**：三处文档统一为「可选第三级兜底」，不是启动前提
- **禁词红线**：公开文档零命中投资建议类措辞
- **免责声明**：全部公开文档保留「仅供研究学习，不构成投资建议」

### 已知限制
- akshare 受网络影响经常失败，自动切换 baostock 兜底
- 选股等待：默认 10 只约 30-60 秒
- 非未来表现预测：评分为规则因子打分（满分 100），不是机器学习预测

## v0.5 (2026-05-16)

### 🎯 产品形态
- **可视化 UI**：Streamlit 本地界面，左侧参数 + 右侧结果，小白无需命令行
- **启动方式**：双击 `start_ui.command` → 选参数 → 开始选股 → 看结果
- **产品首页**：README 顶部含截图预览、能力一览、已知限制、免责声明

### 🚀 小白体验
- 一键启动脚本 `start_ui.command`：分步检测 Python/虚拟环境/依赖/端口/启动，每步失败有中文下一步提示
- 备用数据通道安装脚本 `scripts/install_fallback.command`：Git/GitHub/权限问题的多方法解决 + 手动安装指引
- 环境自检页：首页展开即见 Python 版本/备用通道/本地缓存/最近选股，汇总判定就绪状态
- 首页引导：选参数 → 开始选股 → 看结果
- 就绪状态：首页明确显示「✅ 可以开始选股」或具体缺失项

### 📊 数据
- akshare 主数据源 + skill_fallback（~120 条 K 线，6 个月）（v0.5 基线，当前已由 baostock ~570 条替代）
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
- 数据覆盖：v0.5 基线为 skill_fallback 约 120 条 K 线；当前已由 baostock 稳定约 570 条替代
- akshare 不稳定：受网络影响经常失败，自动切换 fallback
- 选股等待：默认 10 只约 30-60 秒
- 非未来表现预测：评分为规则因子打分（满分 100），不是机器学习预测
