# 项目状态交接摘要

> 最后更新：2026-05-18

## 1. 项目总目标

打造长期可用、结果可信、可复盘的 A 股选股系统。最终形态：小白可用的可视化选股系统。
路线：P5→P6→P7→P8渐进增强。暂不碰实盘交易。
禁止事项：不碰 AI/qlib/实盘交易/复杂前后端分离/数据库/登录系统。

## 2. 当前完成阶段

| 阶段 | Commit | 内容 |
|------|--------|------|
| P7.10 | `81d9f4c` | v0.5发布前最终审查 |
| P7.10文档 | `83393f4` | 同步P7.10交付状态 |
| P8.0 | `46230b9` | 下一阶段规划初稿 |
| P8.0顾问审查 | `8706fa7` | 收紧P8路线图 |
| P8.1-0 | `9648b1b` | 数据源评估报告 |
| P8.1-1 | `eff452a` | baostock实验通过(10/10达570条) |
| P8.1-1文档 | `093576d` | 同步P8.1-1状态 |
| P8.1-2 | `5254f62` | baostock小步接入数据层，链路为 akshare → baostock → skill_fallback |
| P8.1-2文档 | `cd37496` | 记录P8.1-2顾问验收 |
| P8.1-3 | `12168f3` | 修正coverage_warning：baostock 570条不再误判 |
| P8.1-3.1 | `ce2b7ec` | 修正日期差方向+抽出_has_coverage_warning()+3反例验证 |
| P8.1-4 | `225ec0c` | 数据质量收口验收：CLI/报告/UI 三处一致，无矛盾 |
| P8.2-0 | `4415aa1` | 策略解释方案设计：explain字段/生成规则/CLI报告UI三处展示 |
| P8.2-1 | `4d50ae5` | 实现_build_explain()，JSON结果新增explain字段，Top5验证通过 |
| P8.2-2 | `63766d6` | Markdown报告接入explain，优雅降级，验证通过 |
| P8.2-2文档 | `c07eeae` | 同步P8.2-2报告解释状态 |
| P8.2-3 | `8379657` | UI接入explain：expander顶部展示解释/可靠性折叠 |
| P8.2-4 | `caac7b2` | 小白依赖收口：requirements-ui加入baostock/状态同步/全链路通过 |
| P8.4-0 | `9361433` | 策略管理设计文档 |
| P8.5-0 | `75209c7` | AI辅助解释边界评审决策文档 |
| P8.5-0.1 | `fdbab4f` | 修正 P8.5 决策文档中的旧候选字段名表述，统一为 selection_latest.json 顶层 top/all |
| P8.5-0.2 | `d8191a4` | 项目状态字段名零残留收口 |
| P8.6-0 | `468c240` | UI兼容性预检与修复方案（未修改产品代码） |
| P8.6-0.1 | `9d76805` | UI兼容性方案范围收口 |
| P8.6-1 | `2bc15aa` | UI兼容性最小修复 |
- GitHub: https://github.com/xiarantang/a-share-selection-system

## 3. 真实能力 (v0.5 + P8.4 已完成)

- ✅ 数据：akshare + **baostock** + skill_fallback + 缓存；baostock稳定570条K线
- ✅ 选股：6因子评分 + decision/risk_level/confidence + explain 小白解释字段
- ✅ 策略管理：策略元数据注册表 + CLI `--strategy` 参数 + UI 策略选择器（当前只有「默认规则策略」）
- ✅ 验证：validate + backtest-validate + report，Markdown报告已展示explain解释
- ✅ 可视化：Streamlit 本地 UI，逐只详情已展示 explain 小白解释，策略选择器
- ✅ 小白启动：start_ui.command 安装 requirements-ui.txt；轻量依赖已包含 baostock
- ✅ Pipeline：PASS/FAIL退出码可信

## 4. 阶段记录（P8.1-P8.4 已完成）

当前推进：P8.6-1 UI兼容性最小修复已完成。以下保留 P8.1-P8.6-1 的关键验收记录。

baostock 小步接入数据层：
1. baostock 加入 requirements.txt
2. data/fetcher.py 新增 `_fetch_baostock()`（~100行），插入 akshare 之后、skill_fallback 之前
3. 字段映射完整：date/open/high/low/close/volume/amount/pct_change/turnover/pre_close
4. 登录/登出管理，异常时 finally 释放连接
5. 函数签名不变，source 标记为 "baostock"
6. 修正 test_baostock.py：动态日期、达标率计算
7. CLI 全链路：语法8/8→select EXIT:0(10/10均为baostock)→backtest-validate EXIT:0→report EXIT:0
8. 数据来源已从 skill_fallback 为主切换为 baostock 为主

P8.1-3/P8.1-3.1 覆盖提示修正：
- `_has_coverage_warning()` 已从 `SelectionEngine.select()` 中抽出，便于验证
- 570 条 `baostock` 数据首个交易日晚 1 天时不再误报覆盖不足
- 570 条数据若实际起点晚 31 天，会正确提示覆盖不足
- 120 条 `skill_fallback` 仍会提示覆盖不足
- `scripts/confirm_coverage_fix.py` 已包含 3 个单元反例和 5 只真实集成验证

顾问验收补充：
- 复跑 `select --universe static --limit 10 --top 5`：10/10 数据源均为 `baostock`，每只 570 条日 K
- `backtest-validate` 和 `report` 均可运行
- P8.1-3.1 复核：3 个覆盖提示反例通过，5 只真实 `baostock` 数据均为 570 条且 `coverage_warning=False`

P8.1-4 收口验收：
- 文档：`docs/P8_1_ACCEPTANCE.md`
- CLI JSON：`source_dist={"baostock": 10}`，Top5 均为 570 条，`coverage_warning_count=0`
- Markdown 报告：数据源、K线条数、覆盖不足率、整体质量与 JSON 一致
- Streamlit UI：数据源摘要、K线区间、覆盖不足率、整体质量与 JSON/报告一致
- P8.1 对比 v0.5：主数据源由 `skill_fallback` 120 条提升为 `baostock` 570 条，覆盖不足率从 100% 降为 0%，整体质量从 `usable_with_caution` 提升为 `good`

P8.2-0 解释方案设计：
- 文档：`docs/P8_2_EXPLANATION_DESIGN.md`
- 设计新增 `explain` 字段：`summary` / `strengths` / `weaknesses` / `risk_note` / `confidence_note`
- 解释只从现有 `reasons` / `risks` / `factor_scores` / `factor_values` / `decision` / `risk_level` / `confidence` / `rows` 生成
- 明确禁止：不改评分公式、不改排序、不引入 AI、不输出买入/卖出/目标价/收益预测
- 展示范围：CLI JSON、Markdown 报告、Streamlit UI

P8.2-1 JSON解释字段实现：
- `strategies/selection.py` 新增 `_build_explain()`
- `SelectionEngine.select()` 成功结果新增 `explain`
- `explain` 包含 `summary` / `strengths` / `weaknesses` / `risk_note` / `confidence_note`
- `scripts/confirm_explain.py` 验证 Top5 每条解释字段完整，且不包含买入/卖出/目标价/收益预测等禁词
- 本阶段未修改报告和 UI 展示

P8.2-2 Markdown报告接入解释：
- `reports/generator.py` 在 Top 候选下展示 `explain`
- 报告包含：解释、加分、风险、可靠性、数据说明
- 老 JSON 没有 `explain` 时优雅降级，不报错
- `scripts/confirm_report_explain.py` 验证报告解释段落和禁词
- 本阶段未修改 UI

P8.2-3 Streamlit UI 接入解释：
- `app.py` 在逐只详情 expander 顶部展示 `explain.summary`
- UI 展示主要加分、主要风险、可靠性说明
- 老 JSON 没有 `explain` 时优雅降级，不报错
- 本阶段未修改评分、排序和报告生成逻辑

P8.2-4 小白依赖收口：
- `requirements-ui.txt` 已加入 `baostock>=0.8.8`
- `scripts/confirm_ui_dependencies.py` 验证轻量依赖包含 baostock，且当前环境可 import baostock/streamlit
- `select --universe static --limit 10 --top 5` 验证 10/10 数据源为 baostock
- `backtest-validate`、`report`、`confirm_explain.py`、`confirm_report_explain.py` 均通过

P8.3-0 UI体验增强设计：
- 文档：`docs/P8_3_UI_EXPERIENCE_DESIGN.md`
- 问题诊断：15 个具体问题（首页 H-1~H-4、结果页 R-1~R-4、逐只详情 D-1~D-4、工程风格 E-1~E-5）
- 总目标：小白打开后 完成 启动→选股→Top3→原因→风险→数据质量→报告 全流程
- 拆分计划：
  - P8.3-1：首页/启动区体验优化（合并就绪横幅、首次检查默认折叠、简化首页引导）
  - P8.3-2：结果首屏 Top3 + 总览卡片（Top3速览、合并信息层、决策中文化）
  - P8.3-3：风险视觉统一和小白解释优化（风险颜色、因子中文标签、技术术语折叠）
  - P8.3-4：UI 验收脚本和截图更新
- 设计原则：不做营销落地页、不换前端框架、不改评分/排序/数据链路、保持 CLI 验收和双击启动
- 本阶段仅写设计文档，未修改 app.py 和任何代码文件

P8.3-1 首页/启动区体验优化：
- 合并就绪横幅：`st.success` + `st.info` 两行合并为一行（"系统就绪 — 点击左侧开始选股"）
- 首次使用检查默认折叠：`expanded` 改为 `False`，不再占据首屏
- 简化首页引导：四步卡片改为两步（① 在左侧选参数 → ② 等待结果），更清晰
- 侧栏优化：去掉 `① 选择股票池` / `② 一键运行` / `③ 查看结果` 三段分割标题，改为参数区 + 按钮区 + 免责声明，更紧凑
- 未修改评分、排序、数据链路、报告逻辑
- 验收：py_compile ✅ | select EXIT:0 ✅ | backtest-validate EXIT:0 ✅ | report EXIT:0 ✅

P8.3-1.1 首页文案一致性收口：
- 副标题：旧文案`×步完成选股` → `选参数 → 开始选股 → 看结果`
- 文件头注释：旧文案`×步引导` → `选参数、开始选股、看结果`
- 函数注释/行内注释：旧文案步骤计数描述 → 移除步骤计数
- 全文件不再出现"四步/三步/两步"等不一致说法

P8.3-1.2 公开文档文案一致性收口：
- README.md：`三步完成选股` → `选参数 → 开始选股 → 看结果`
- README.md：`首页×步引导` → `首页引导`
- README.md：旧文案步骤计数 → `选参数→开始选股→看结果`
- docs/USER_GUIDE.md：确认无旧文案残留，无需修改
- 保留免责声明：仅供研究学习，不构成投资建议
- 未修改 app.py / strategies / data / reports / validation / main.py

P8.3-2 结果首屏 Top3 + 总览卡片：
- 新增 Top3 速览卡片：在 Tab 外、数据概览上方，用 `st.columns(3)` 展示前 3 名候选
- 每张卡片包含：排名奖牌（🥇🥈🥉）、代码名称、评分、中文决策标签、风险等级（带颜色）、一句话解释（explain.summary）
- 决策标签 UI 展示层中文化：strong_watch → 强观察、watch → 观察、neutral → 中性、avoid → 回避
- 风险等级 UI 展示层中文化：low → 🟢 低、medium → 🟡 中、high → 🔴 高
- 合并信息层：原 4 列信息条 + 5 列覆盖摘要 + 纯文本覆盖摘要 + 验证摘要 → 紧凑 4 列数据概览（股票池/数据区间/K线数据源/整体质量）+ 紧凑提示行
- 候选表格决策列同步中文化，着色函数适配中文标签
- 底层 JSON/CSV/策略字段不变（`DECISION_ZH` / `RISK_LABEL` 仅在 UI 展示层映射）
- 未修改评分、排序、数据链路、报告逻辑
- 验收：py_compile ✅ | select EXIT:0 (10/10 baostock) ✅ | backtest-validate EXIT:0 ✅ | report EXIT:0 ✅

P8.3-3 风险视觉统一和小白解释优化：
- 统一风险展示颜色：low → 低风险（绿色 #d4edda）、medium → 中风险（橙色 #fff3cd）、high → 高风险（红色 #f8d7da）
- Top3 速览卡片：决策和风险等级改用 HTML 彩色标签（`decision_badge` / `risk_badge`），视觉与逐只详情一致
- 候选表格：风险列中文化（低风险/中风险/高风险），决策列保持中文并着色
- 逐只详情标题：决策和风险改为中文展示（强观察/观察/中性/回避 · 低风险/中风险/高风险）
- 逐只详情正文：决策和风险使用 HTML 彩色标签，与 Top3 卡片风格统一
- 因子得分：添加小图标（📈趋势/🚀动量/📊量能/🛡️风控/📋数据质量/🔮形态），不改变分数
- 技术指标详情：MA5/MA20/MA60/RSI/波动率等移入默认收起的「📐 技术指标详情」expander，不堆在首层
- 风险提示分级着色：高风险 → `st.error`(红)、中风险 → `st.warning`(橙)、低风险 → `st.info`(绿灰)，不再一律红底
- 数据区间友好化：保留日期同时补充「约近 X 个月」提示
- 保留免责声明：仅供研究学习，不构成投资建议
- 新增 UI 展示 helper 函数：`risk_badge()` / `decision_badge()` / `friendly_date_range()` / `risk_alert()`，仅用于页面渲染
- 未修改评分、排序、数据链路、报告逻辑
- 验收：py_compile ✅ | select EXIT:0 (10/10 baostock) ✅ | backtest-validate EXIT:0 ✅ | report EXIT:0 ✅ | 禁词检查 ✅

P8.3-3.1 置信度展示中文化收口：
- 新增 `CONFIDENCE_ZH` 映射：high → 高置信度、medium → 中置信度、low → 低置信度（仅 UI 展示层）
- 候选表格"置信度"列：raw high/medium/low → 高置信度/中置信度/低置信度
- 逐只详情正文"置信度: high" → "置信度: 高置信度"
- 底层 JSON/CSV/策略字段不变，CLI 输出仍保持 high/medium/low
- 未修改评分、排序、数据链路、报告逻辑
- 验收：py_compile ✅ | select EXIT:0 ✅ | report EXIT:0 ✅ | 置信度英文残留检查 ✅ | 禁词检查 ✅

P8.3-3.2 置信度验收正则小尾巴收口：
- `CONFIDENCE_ZH` 字典改为多行写法，避免同一行出现"置信度"后跟 high/medium/low 导致验收正则误命中
- 无业务逻辑变化，纯格式收口
- 验收：py_compile ✅ | 正则零命中 ✅ | 禁词检查 ✅

P8.3-4 UI 验收脚本和截图更新：
- 新增 `scripts/confirm_p83_ui.py`：44 项自动检查，覆盖 app.py 静态文本 + JSON 运行时数据 + 截图文件
  - 首页引导文案（选参数 → 开始选股 → 看结果）
  - Top 3 候选速览标题
  - 技术指标详情折叠入口
  - 免责声明
  - 决策标签中文：强观察/观察/中性/回避
  - 风险标签中文：低风险/中风险/高风险
  - 置信度标签中文：高置信度/中置信度/低置信度
  - 因子标签中文：趋势/动量/量能/风控/数据质量/形态
  - 逐只详情标题已用中文（不再显示 raw 英文字段）
  - 风险分级着色 risk_alert
  - 友好日期区间 friendly_date_range
  - 禁词不在 UI 正向文案
  - JSON 底层字段仍为英文（映射仅在 UI 展示层）
  - explain 字段完整、因子得分齐全
  - JSON explain 无禁词
  - 截图文件存在且非空
- 截图更新：通过 agent-browser 从真实 Streamlit 页面截取
  - `docs/screenshots/home.png`（~197KB）：首页引导 + 系统就绪状态
  - `docs/screenshots/result.png`（~174KB）：Top3 速览卡片 + 中文决策/风险标签
- 未修改 app.py、评分、排序、数据链路、报告逻辑
- 验收：confirm_p83_ui 44/44 ✅ | py_compile ✅ | select EXIT:0 ✅ | backtest-validate EXIT:0 ✅ | report EXIT:0 ✅ | 禁词检查 ✅

P8.3-4.1 结果页数据概览可读性收口：
- 问题：结果页数据概览区域使用 `st.metric` 大字号展示，长文本（数据区间、K线/数据源）被截断
- 修复：将 4 列 `st.metric`（股票池/数据区间/K线数据源/整体质量）替换为 `st.caption` + `st.markdown` 紧凑文本展示
- 改动仅限 `app.py` 第 564-571 行（数据概览区域），从 `ov_cols[N].metric(label, value)` 改为 `with ov_cols[N]: st.caption(label); st.markdown(value)`
- 以下信息完整显示无截断：股票池/扫描数量、完整数据区间（含"约近 X 个月"）、平均K线条数/数据源、整体质量
- 未修改 Top3 卡片、逐只详情、候选表格、评分、排序、数据链路、报告逻辑
- 截图更新：`docs/screenshots/result.png`（~243KB）从真实 Streamlit 页面截取，数据概览文字无截断
- 验收：py_compile ✅ | confirm_p83_ui 44/44 ✅ | select EXIT:0 (10/10 baostock) ✅ | report EXIT:0 ✅

P8.4-0 策略管理设计文档：
- 文档：`docs/P8_4_STRATEGY_MANAGEMENT_DESIGN.md`
- 结论先行：P8.4 从最小策略管理层起步，不是评分重写
- 目标：策略注册骨架 → CLI 可选参数 → Streamlit 选择器 → 文档验收
- 策略元数据设计：id/name/description/suitable_scenario/risk_reminder/enabled/entry_function
- 安全边界：不改评分/排序/数据链路，不引入 AI/qlib，不做交易执行
- 分步计划：P8.4-1 注册骨架、P8.4-2 CLI 参数、P8.4-3 UI 选择器、P8.4-4 文档验收
- 本阶段仅写设计文档，未修改任何代码文件或策略逻辑
- 未修改 app.py / main.py / strategies/selection.py / data/ / reports/ / validation/

P8.4-1 策略注册骨架：
- `strategies/registry.py` 从旧 Skill/脚本执行注册中心替换为元数据注册中心
- 移除：PRIORITY_SCRIPTS / skills_dir / subprocess.run / SKILL.md 扫描
- 模块级 API：DEFAULT_STRATEGY_ID / STRATEGY_REGISTRY / REQUIRED_FIELDS / register_strategy / get_strategy / list_strategies / get_default_strategy
- 默认策略：id=default / name=默认规则策略 / entry_function=strategies.selection:SelectionEngine
- StrategyRegistry 兼容类保留：list_strategies() / execute_strategy() / run_all_strategies() 不执行外部脚本
- 兼容字段：available=True / executable=False / type="builtin"，main.py strategy 和 scripts/pipeline.py 无需改动
- 验收脚本：scripts/confirm_p84_registry.py
- 未修改 app.py / main.py / strategies/selection.py / data/ / reports/ / validation/
- 未修改评分、排序、数据链路、报告逻辑、Streamlit UI

P8.4-1.1 策略注册兼容签名收口：
- `StrategyRegistry.execute_strategy` 签名恢复为接受旧式 script/args 参数：(strategy_name, script=None, args=None, **_kwargs)
- script/args 参数被安全忽略，不执行外部脚本，行为不变
- 现有调用方（main.py strategy / scripts/pipeline.py）无需改动
- 验收脚本新增 3 项旧签名检查：execute_strategy("default", "dummy.py") / execute_strategy("default", "dummy.py", ["--x"]) / execute_strategy("missing", "dummy.py")
- 未修改 app.py / main.py / strategies/selection.py / data/ / reports/ / validation/
- 未修改评分、排序、数据链路、报告逻辑、Streamlit UI

P8.4-2 CLI策略参数接入：
- `main.py` select 子命令新增 `--strategy` 可选参数，默认 `DEFAULT_STRATEGY_ID`（即 "default"）
- `cmd_select(args)` 在运行 SelectionEngine 前验证 strategy_id：无效或已禁用时 log error 并返回 exit 1
- 无效策略不触发数据拉取、不覆盖 selection_latest.json
- JSON payload 新增顶层字段：`strategy_id`（字符串）和 `strategy`（含 id/name/description/suitable_scenario/risk_reminder 的小字典）
- `--strategy default` 等同于省略 `--strategy`
- 省略 `--strategy` 时行为与之前完全一致（仅多了顶层策略元数据）
- 不调用 entry_function，不动态导入，不改变评分/排序/数据/报告/UI
- 验收脚本：`scripts/confirm_p84_cli.py`
- 未修改 app.py / strategies/selection.py / strategies/registry.py / data/ / reports/ / validation/

下一步建议：P8.4-4 文档验收。 → **已完成**

P8.4-4.1 路线图状态一致性收口：
- docs/P8_ROADMAP.md P8.4 部分修正为真实完成状态：默认策略 ID 是 `default`（非 `multi-factor-v1`），当前只有一套默认策略，Markdown 报告逻辑未改，策略管理只是入口壳
- docs/P8_ROADMAP.md P8.5 部分增加 P8.5-0 决策评审门：AI 默认关闭、不进评分/排序/风控/买卖决策链路、不输出买入/卖出/目标价/收益预测、不需要 API Key 才能启动、不能保证边界则暂缓
- docs/P8_ROADMAP.md 阶段总览表和执行顺序更新为已完成状态
- PROJECT_STATE.md 更新：P8.4 已完成，下一步建议为 P8.5-0 可选 AI 辅助解释边界评审/暂缓决策
- scripts/confirm_p84_docs.py 新增路线图一致性检查
- 未修改 app.py / main.py / strategies/ / data/ / reports/generator.py / validation/ / 评分/排序/数据链路
- 验收：py_compile ✅ | confirm_p84_docs ✅ | confirm_p84_registry ✅ | confirm_p84_cli ✅ | confirm_p84_ui ✅

P8.4-3 UI 策略选择器接入：
- `app.py` 从 `strategies.registry` 导入 `DEFAULT_STRATEGY_ID` / `get_strategy` / `list_strategies`
- `run_selection` 新增可选 `strategy_id` 参数（默认 `DEFAULT_STRATEGY_ID`），函数开头用 `get_strategy(strategy_id)` 校验：无效或 disabled 抛出 ValueError
- `run_selection` 仍然使用 `SelectionEngine()` 和 `engine.select(...)`，不调用 registry 的 `execute_strategy`，不动态 import，不调用 `entry_function`
- `run_selection` 返回数据顶层新增 `strategy_id`（字符串）和 `strategy`（含 id/name/description/suitable_scenario/risk_reminder 的字典）
- 侧栏股票池下方增加策略选择器：使用 `list_strategies(enabled_only=True)` 渲染，显示 `name`（如"默认规则策略"），help 提示"当前为规则策略选择，不改变评分公式；仅供研究学习，不构成投资建议"
- 点击"开始选股"时将选中的 `strategy_id` 传给 `run_selection`，写入 `session_state.last_strategy`
- 结果页数据概览下方用 `st.caption` 克制展示当前策略名称、适用场景、风险提醒，不影响 Top3 第一眼可读性
- session_state 新增 `last_strategy`，不破坏已有状态
- 验收脚本：`scripts/confirm_p84_ui.py`（36 项检查）
- 未修改 main.py / strategies/selection.py / strategies/registry.py / data/ / reports/ / validation/
- 未修改评分、排序、数据链路、报告逻辑
- 验收：py_compile ✅ | confirm_p84_registry 35/35 ✅ | confirm_p84_cli 17/17 ✅ | confirm_p84_ui 36/36 ✅ | select EXIT:0 (10/10 baostock) ✅ | report EXIT:0 ✅

P8.4-4 策略管理文档与验收收口：
- README.md：当前能力新增「策略管理」条目，快速开始侧栏描述更新为「选择股票池、策略和参数」，CLI 示例增加 `--strategy default`
- docs/USER_GUIDE.md：参数表新增「选股策略」行（默认值：默认规则策略，说明：当前为规则策略选择，不改变评分公式）；结果区新增策略/适用场景/风险提醒说明
- docs/P8_4_STRATEGY_MANAGEMENT_DESIGN.md：P8.4-1/2/3/4 全部标注 ✅；修正误导表述「调用对应入口函数」→「当前只校验并传递策略 ID，仍运行默认 SelectionEngine」
- PROJECT_STATE.md：记录 P8.4-4 完成 + P8.4 策略管理阶段完成
- 新增 scripts/confirm_p84_docs.py：文档验收脚本
- 未修改 app.py / main.py / strategies/ / data/ / reports/generator.py / validation/
- 未修改评分、排序、数据链路、报告逻辑
- 验收：py_compile ✅ | confirm_p84_registry ✅ | confirm_p84_cli ✅ | confirm_p84_ui ✅ | confirm_p84_docs ✅ | select EXIT:0 ✅ | report EXIT:0 ✅

**P8.4 策略管理阶段已完成**（P8.4-1 注册骨架 → P8.4-2 CLI 参数 → P8.4-3 UI 选择器 → P8.4-4 文档验收 → P8.4-4.1 路线图一致性收口）。

P8.5-0 AI 辅助解释边界评审：
- 文档：`docs/P8_5_AI_EXPLANATION_DECISION.md`
- 结论：**暂缓实现 P8.5 AI 辅助解释**；只有在边界全部可自动验收时，才进入下一步最小设计
- 硬性禁止：不参与评分、排序、风控等级、买卖决策链路；不生成股票池；不改 data/fetcher.py 数据链路；不输出买入/卖出/目标价/收益预测等投资建议措辞；不要求 API Key 才能启动小白 UI
- 默认关闭：UI 默认不启用 AI；CLI 默认不启用 AI；没有 API Key 时系统完全可用
- 可接受最小方案（仅设计）：UI 折叠区"AI 辅助阅读说明"，输入只允许已有 JSON 的 Top 候选和规则 explain，输出只能是通俗解释/术语解释/风险提醒复述，必须带免责声明
- 进入 P8.5-1 的硬门槛：禁词检查验收脚本、默认关闭验收、无 API Key 可启动验收、默认路径不调用 AI 验收、输出隔离验收
- 本阶段仅写决策文档，未修改任何代码文件
- 未修改 app.py / main.py / strategies/ / data/ / reports/ / validation/

下一步建议：**暂不进入 AI 实现**。可选择：① 如确需推进，先做 P8.5-1 设计文档（含可自动验收的边界守卫方案）；② 转向其他验收稳定性小优化。

P8.5-0.1 文档字段名一致性收口：
- `docs/P8_5_AI_EXPLANATION_DECISION.md` 中旧候选字段名表述修正，统一为 `selection_latest.json` 真实顶层字段名 `top`（候选列表）和 `all`（全集列表）
- PROJECT_STATE.md P8.5-0 commit 从 `—` 更新为 `75209c7`
- 无代码改动，未修改 app.py / main.py / strategies/ / data/ / reports/ / validation/ / 评分/排序/数据链路

P8.6-0 UI兼容性预检与修复方案：
- 文档：`docs/P8_6_UI_STABILITY_AUDIT.md`
- 发现 2 类兼容性风险：
  1. Streamlit `use_container_width` 已废弃，app.py 共 4 处（行 358/492/494/660），需替换为 `width="stretch"`
  2. Pandas `Styler.applymap` 已废弃，app.py 共 1 处（行 657），需替换为 `Styler.map`
- 修复方案：P8.6-1 共 9 处机械替换（app.py 5 处 + requirements*.txt 4 处），不新增验收脚本，无逻辑变化
- 版本约束建议：`streamlit>=1.28.0` → `>=1.39.0`，`pandas>=2.0.0` → `>=2.1.0`
- 本阶段仅写预检文档，未修改 app.py / main.py / strategies/ / data/ / reports/ / validation/ / 评分/排序/数据链路

	P8.6-0.1 UI兼容性方案范围收口：
	- `docs/P8_6_UI_STABILITY_AUDIT.md` 补充范围收口说明，明确只做 9 处机械替换
	- 本阶段仅更新文档，未修改 app.py / requirements.txt / requirements-ui.txt

	P8.6-1 UI兼容性最小修复：
	- app.py 4 处 `use_container_width=True` → `width="stretch"`：逐只复盘详情表格、侧栏"开始选股"按钮、侧栏"历史复盘"按钮、结果页候选表格
	- app.py 1 处 `df.style.applymap(...)` → `df.style.map(...)`
	- requirements.txt 2 处：`streamlit>=1.28.0` → `>=1.39.0`，`pandas>=2.0.0` → `>=2.1.0`
	- requirements-ui.txt 2 处：同上
	- PROJECT_STATE.md 记录 P8.6-1 完成
	- 未修改评分、排序、数据链路、报告逻辑
	- 未新增任何脚本，未改 docs/P8_6_UI_STABILITY_AUDIT.md

## 5. 关键文件

app.py / main.py / data/fetcher.py / data/universe.py / strategies/selection.py / strategies/registry.py / reports/generator.py / requirements.txt / requirements-ui.txt / scripts/test_baostock.py / scripts/confirm_coverage_fix.py / scripts/confirm_explain.py / scripts/confirm_report_explain.py / scripts/confirm_ui_dependencies.py / scripts/confirm_p83_ui.py / scripts/confirm_p84_registry.py / scripts/confirm_p84_cli.py / scripts/confirm_p84_ui.py / scripts/confirm_p84_docs.py / docs/P8_1_ACCEPTANCE.md / docs/P8_2_EXPLANATION_DESIGN.md / docs/P8_3_UI_EXPERIENCE_DESIGN.md / docs/P8_4_STRATEGY_MANAGEMENT_DESIGN.md / docs/P8_5_AI_EXPLANATION_DECISION.md / docs/P8_6_UI_STABILITY_AUDIT.md / docs/P8_ROADMAP.md / docs/screenshots/home.png / docs/screenshots/result.png
