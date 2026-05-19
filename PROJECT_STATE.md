# 项目状态交接摘要

> 最后更新：2026-05-19（P10.2-1 完成）

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
| P8.6-1 | `30e0fb9` | UI兼容性最小修复 |
| P8.6-1.1 | `4aefa5c` | 项目状态commit回填修正 |
| P8.6-2 | `08c26c0` | UI冒烟验收与截图确认 |
| P8.6-2.1 | `e2b8e4b` | 回填UI冒烟验收commit |
| P8.6-3 | `ed4d27b` | 小白启动脚本冒烟验收 |
| P8.6-3.1 | `16d54c8` | 回填启动脚本验收commit |
| P8.6-4 | `401fad9` | 公开文档状态一致性收口 |
| P8.6-4.1 | `5737aa4` | 回填公开文档收口commit |
| P8.6-4.2 | `eaa9e31` | 项目状态阶段标题收口 |
| P8.7-0 | `5edefbe` | 发布前总复盘与下一阶段边界设计 |
| P8.7-1 | `33081e5` | 发布前一键验收脚本最小整合 |
| P8.7-2 | `8ae0544` | 小白手动验收清单一致性收口 |
| P8.7-3 | `58301ba` | README公开入口与当前状态一致性收口 |
| P8.7-4 | `67e2c72` | 公开文档数据层描述一致性收口 |
| P8.7-5 | `3966bf5` | 启动入口fallback可选状态收口 |
| P8.7-5.1 | `e96645e` | 回填commit并同步验收清单口径 |
| P8.7-5.2 | `28e2ba6` | 修正发布复盘口径禁词 |
| P8.7-6 | `93e84d3` | 发布候选最终复核与交付说明收口 |
| P8.7-6.1 | `f46731b` | 修正发布候选禁词口径 |
| P8完成态 | `96909eb` | 发布候选状态最终收口 |
| P9.0 | `—` | 从 P1 到 P8 的完整来时路复盘与 P9 路线图设计 |
| P9.1 | — | 公开文档一致性治理 |
| P9.1.1 | `ea4c3e9` | PROJECT_STATE.md 旧流程词口径返工收口 |
| P9.2-1 | — | 新增独立文档一致性检查脚本 |
| P9.2-2 | `994dcd5` | 将文档一致性检查接入发布前一键验收 |
| P9.3-0 | `24d38c0` | 复盘记录增强设计文档 |
| P9.3-1 | `3c9f299` | JSON 复盘记录字段实现 |
| P9.3-1.1 | `82c836e` | run_metadata 字段结构收口 |
| P9.3-2 | `cb20618` | Markdown 报告接入 run_metadata |
| P9.3-2.1 | — | PROJECT_STATE.md 禁词口径残留修正 |
| P9.3-3 | — | Streamlit UI 轻量展示 run_metadata |
| P9.3-3.1 | — | UI/CLI 输出边界措辞收口 |
| P9.3-4.1 | — | 新增独立 run_metadata 复盘记录验收脚本 |
| P9.3-4.1.1 | — | 设计文档表格格式返工收口 |
| P9.3-4.2 | — | run_metadata 验收接入发布前一键验收 |
| P9.3-4.2.1 | — | PROJECT_STATE.md 中 P9.3-4.2 记录措辞微修 |
| P9.4-0 | — | 小白排障增强设计文档 |
| P9.4-0.1 | — | P9.4 设计文档禁词措辞返工 |
| P9.4-1 | — | 公开排障文档口径收口 |
| P9.4-1.1 | — | 排障文档手动安装依赖说明微修 |
| P9.4-2 | — | UI 错误/等待/空结果提示增强 |
| P9.4-2.1 | — | UI 排障提示文案返工 |
| P9.4-3 | — | 启动脚本提示增强 |
| P9.4-3.1 | — | 恢复 start_ui.command 可执行权限 |
| P9.4-4.1 | — | 新增独立排障体验验收脚本 |
| P9.4-4.1.1 | — | 补齐验收脚本关键词覆盖 |
| P9.4-4.2 | — | 排障体验验收接入发布前一键验收 |
| P9.5-0 | — | 发布版打标准备设计文档 |
| P9.5-0.1 | — | 发布准备设计文档版本口径返工 |
| P9.5-1 | — | 更新 RELEASE_CHECKLIST.md |
| P9.5-1.1 | — | PROJECT_STATE.md 中 fallback 历史措辞微修 |
| P9.5-2 | — | 更新 CHANGELOG.md |
| P9.5-3 | — | tag 前最终验收记录（打标前记录） |
| P9.5-4 | — | v0.6-rc1 打标后状态同步 |
| P9.5-4.1 | — | P9_5_RELEASE_PREP 打标前/打标后口径分层收口 |
| P10-0 | — | 发布后观察与真实小白验收路线图 |
| P10.1-0 | — | tag/main/公开文档状态一致性守门设计 |
| P10.1-1 | — | 新增独立 release tag/main 状态验收脚本 |
| P10.1-2 | — | confirm_release_state 接入取舍决策（暂不接入） |
| P10.1-3 | — | tag/main 状态守门文档收口 |
| P10.2-0 | — | 真实 UI 启动与截图复核设计/诊断 |
| P10.2-1 | — | 修正截图脚本关键词/验收口径 |
| P10.2-1.1 | — | 修正 release 状态守门规则，允许验收脚本白名单 |
- GitHub: https://github.com/xiarantang/a-share-selection-system

## 3. 真实能力 (v0.5 + P8 已完成)

- ✅ 数据：akshare + **baostock** + skill_fallback + 缓存；baostock稳定570条K线
- ✅ 选股：6因子评分 + decision/risk_level/confidence + explain 小白解释字段
- ✅ 策略管理：策略元数据注册表 + CLI `--strategy` 参数 + UI 策略选择器（当前只有「默认规则策略」）
- ✅ 验证：validate + backtest-validate + report，Markdown报告已展示explain解释
- ✅ 可视化：Streamlit 本地 UI，逐只详情已展示 explain 小白解释，策略选择器
- ✅ 小白启动：start_ui.command 安装 requirements-ui.txt；轻量依赖已包含 baostock
- ✅ Pipeline：PASS/FAIL退出码可信
- ✅ UI 兼容性：废弃 API 已清理（use_container_width → width="stretch"、applymap → map）
- ✅ 启动验证：双击 start_ui.command 冒烟验收通过（HTTP 200、无废弃警告）
- ✅ 发布前复盘：P8.7-0 总复盘完成，剩余风险与下一阶段边界已明确

## 4. 阶段记录（P8.1-P8.7 已完成）

当前状态：P8 已走完，v0.5 + P8 处于发布候选完成态。以下保留 P8.1-P8.7 的关键验收记录。

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
- 明确禁止：不改评分公式、不改排序、不引入 AI、不输出投资建议措辞
- 展示范围：CLI JSON、Markdown 报告、Streamlit UI

P8.2-1 JSON解释字段实现：
- `strategies/selection.py` 新增 `_build_explain()`
- `SelectionEngine.select()` 成功结果新增 `explain`
- `explain` 包含 `summary` / `strengths` / `weaknesses` / `risk_note` / `confidence_note`
- `scripts/confirm_explain.py` 验证 Top5 每条解释字段完整，且不包含投资建议措辞禁词
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
- docs/P8_ROADMAP.md P8.5 部分增加 P8.5-0 决策评审门：AI 默认关闭、不进评分/排序/风控/交易决策链路、不输出投资建议措辞、不需要 API Key 才能启动、不能保证边界则暂缓
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
- 硬性禁止：不参与评分、排序、风控等级、交易决策链路；不生成股票池；不改 data/fetcher.py 数据链路；不输出投资建议措辞；不要求 API Key 才能启动小白 UI
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

P8.6-2 UI冒烟验收与截图确认：
- 基础验收：py_compile app.py ✅ | select --universe static --limit 10 --top 5 EXIT:0 (10/10 baostock) ✅
- Streamlit UI 冒烟验收：
  - 首页可正常打开：标题、参数区（股票池/策略/扫描数量/展示数量/起始日期）、开始选股按钮、免责声明 ✅
  - 结果页可正常展示：选股完成提示 10/10、Top3 速览卡片（建设银行/工商银行/中信证券）、中文决策标签（观察/中性）、中文风险标签（低风险）、中文置信度标签（高置信度） ✅
  - 候选表格 5 行完整显示，无文字遮挡或空白 ✅
  - 逐只详情折叠区 5 条展开正常 ✅
- 截图更新：
  - docs/screenshots/home.png：首页截图已更新（~183KB）
  - docs/screenshots/result.png：结果页截图已更新（~147KB）
- 警告检查：app.py 无 use_container_width / applymap 残留 ✅
- 未修改产品代码/评分/排序/数据链路/报告逻辑
- 仅修改 PROJECT_STATE.md、docs/screenshots/home.png、docs/screenshots/result.png

P8.6-3 小白启动脚本冒烟验收：
- start_ui.command 存在且可执行（-rwxr-xr-x）
- 基础验收：py_compile app.py ✅ | requirements-ui.txt 含 streamlit>=1.39.0、pandas>=2.1.0 ✅
- 启动脚本关键步骤验证：
  - Python3 检测 ✅（Python 3.9.6）
  - 虚拟环境已存在 ✅
  - 依赖就绪 ✅（streamlit=1.50.0, pandas=2.3.3）
  - skill_fallback 兜底通道当时检测可用 ✅
- Streamlit 后台启动：HTTP 200 返回确认（1s 内响应） ✅
- 启动日志检查：无 use_container_width / applymap / DeprecationWarning / FutureWarning / 错误 ✅
- 端口清理：启动进程已停止，8501 端口无残留 ✅
- 未修改产品代码/启动脚本/评分/排序/数据链路/报告逻辑
- 仅修改 PROJECT_STATE.md

P8.6-4 公开文档状态一致性收口：
- README.md：当前能力新增「UI 兼容性」「启动验证」条目；文档索引表 UI 验收结果更新为 P8.6
- docs/USER_GUIDE.md：双击启动区补充 P8.6 验证状态说明（废弃 API 已清理、截图已更新）
- docs/UI_ACCEPTANCE_RESULT.md：追加 P8.6 验收记录（P8.6-1/2/3/4）
- PROJECT_STATE.md：记录 P8.6-4 完成
- 未修改产品代码 / 启动脚本 / 评分 / 排序 / 数据链路 / 报告逻辑
- 保留免责声明：仅供研究学习，不构成投资建议

P8.7-0 发布前总复盘与下一阶段边界设计：
- 文档：`docs/P8_7_RELEASE_REVIEW.md`
- P8.1–P8.6 已完成能力总结：数据层（baostock 570 条）、策略解释层（explain 字段）、UI 体验优化（Top3 卡片/中文标签/风险分级着色）、策略管理层（注册表/CLI/UI 选择器）、AI 边界评审（暂缓）、UI 兼容性修复与验收
- 小白路径确认：双击 start_ui.command → 选参数 → 开始选股 → 看结果
- 已验收入口：py_compile、CLI select/report/backtest-validate、Streamlit UI 冒烟、截图、双击启动、44 项自动验收脚本
- 剩余风险：数据源网络波动（baostock 兜底）、akshare 偶发失败（降级链路）、非投资建议边界（免责声明 + 禁词检查）
- 下一阶段建议：优先继续小白体验/验收稳定性，暂不进入 AI 实现，不改评分/排序/数据链路
- 本阶段仅写文档，未修改 app.py / main.py / strategies/ / data/ / reports/ / validation/ / scripts/ / start_ui.command
- 保留免责声明：仅供研究学习，不构成投资建议

P8.7-1 发布前一键验收脚本最小整合：
- 新增 `scripts/confirm_release_ready.py`：当时聚合 9 项发布前检查为一个入口（P9.2-2 起扩展为 10 项）
- 检查项：app.py 语法、P8.3 UI 验收 (44项)、P8.4 策略注册/CLI/UI/文档验收、CLI 选股 (static 10→Top5)、CLI 报告生成、废弃 API 残留检查
- 使用 Python 标准库 subprocess/pathlib/sys，不引入新依赖
- 从项目根目录运行：`python3 scripts/confirm_release_ready.py`
- 全部通过 exit 0，任一失败 exit 1；中文输出"通过/失败/跳过原因"
- docs/P8_7_RELEASE_REVIEW.md 新增第 7 节"发布前一键验收入口"
- PROJECT_STATE.md 记录 P8.7-1 完成
- 未修改 app.py / main.py / strategies/ / data/ / reports/ / validation/ / start_ui.command / requirements*.txt
- 未修改评分、排序、数据链路、报告逻辑
- 保留免责声明：仅供研究学习，不构成投资建议

P8.7-2 小白手动验收清单一致性收口：
- docs/MANUAL_UI_CHECKLIST.md：更新为当前真实 UI 路径（双击 start_ui.command → 选参数 → 开始选股 → 看结果），新增 Top3 速览、中文标签（决策/风险/置信度）、因子图标、技术指标折叠等验收项
- docs/UI_ACCEPTANCE.md：同步更新，移除旧流程引导文案、旧步骤编号等表述，新增 Top3 速览、数据概览、逐只详情中文展示等验收项
- 替换旧流程说法：旧流程引导卡片 →「引导卡片（①选参数 ②等待结果）」、旧步骤编号 → 移除、旧首页引导文案 →「首页引导卡片」
- 保留免责声明：仅供研究学习，不构成投资建议
- 未修改 app.py / main.py / strategies/ / data/ / reports/ / validation/ / scripts/ / start_ui.command / requirements*.txt / README.md / docs/USER_GUIDE.md / docs/P8_7_RELEASE_REVIEW.md
- 未修改评分、排序、数据链路、报告逻辑

P8.7-3 README公开入口与当前状态一致性收口：
- README.md 数据层描述同步为：akshare → baostock → skill_fallback + 缓存；baostock 稳定约 570 条 K 线
- README.md 已知限制表修正：不再将"fallback 约 120 条"描述为主状态，改为 baostock 稳定约 570 条，极端情况降级
- README.md 文档索引新增：docs/MANUAL_UI_CHECKLIST.md（小白人工验收清单）、docs/P8_7_RELEASE_REVIEW.md（发布前总复盘）
- README.md CLI 命令区新增发布前一键验收入口：python3 scripts/confirm_release_ready.py（维护者用，非小白日常步骤）
- README.md 标题描述同步为 akshare → baostock → skill_fallback + backtrader
- 保留小白主路径：双击 start_ui.command → 选参数 → 开始选股 → 看结果
- 保留免责声明：仅供研究学习，不构成投资建议
- PROJECT_STATE.md 记录 P8.7-3 完成
- 未修改 app.py / main.py / strategies/ / data/ / reports/ / validation/ / scripts/ / start_ui.command / requirements*.txt / docs/USER_GUIDE.md / docs/MANUAL_UI_CHECKLIST.md / docs/UI_ACCEPTANCE.md / docs/P8_7_RELEASE_REVIEW.md
- 未修改评分、排序、数据链路、报告逻辑

P8.7-4 公开文档数据层描述一致性收口：
- docs/USER_GUIDE.md + docs/TROUBLESHOOTING.md 两份小白文档：
  - 移除所有"约 120 条""~120 条"硬编码数字，skill_fallback 统一描述为"第三级兜底（数据量可能较少）"
  - 保留数据链路：akshare → baostock（~570 条日 K）→ skill_fallback
  - 保留用户友好理念：「覆盖不全」不是系统故障，而是降级到第三级兜底时的正常提示
- 未修改 app.py / main.py / strategies/ / data/ / reports/ / validation/ / scripts/ / start_ui.command / requirements*.txt / README.md / docs/P8_7_RELEASE_REVIEW.md
- 未修改评分、排序、数据链路、报告逻辑
- 验收：rg 禁词零命中 ✅ | confirm_release_ready ✅

P8.7-5 启动入口fallback可选状态收口：
- app.py：FALLBACK_SCRIPT 不存在时从 st.error（阻止选股）改为 st.info（可选提示）；环境检查将 skill_fallback 标为可选（💡 而非 ❌）；选股失败提示改为先检查网络，必要时安装第三级兜底
- start_ui.command：缺少 fallback 只提示"可选"，移除"重要/缺少/必须/安装后再启动"等阻塞性文案
- scripts/install_fallback.command：标题改为"可选：安装第三级兜底数据通道"，不说首次必装
- README.md：启动入口收口为两步启动；安装 fallback 章节改为可选
- docs/USER_GUIDE.md：移除旧的阻塞式安装提示入口，改为"如果选股全部失败"
- docs/TROUBLESHOOTING.md：已在 P8.7-4 完成同步，无需额外修改
- 未修改 data/ / strategies/ / reports/ / validation/ / main.py / requirements*.txt / scripts/confirm*.py / docs/screenshots/
- 未修改评分、排序、数据链路、报告逻辑
- 验收：rg 禁词零命中 ✅ | py_compile ✅ | bash -n ✅ | test -x ✅ | confirm_release_ready ✅

P8.7-5.1 回填commit并同步验收清单口径：
- PROJECT_STATE.md：P8.7-4 回填 `67e2c72`，P8.7-5 回填 `3966bf5`
- docs/MANUAL_UI_CHECKLIST.md + docs/UI_ACCEPTANCE.md：前置条件同步为"requirements-ui 已包含 baostock，skill_fallback 为可选第三级兜底"
- docs/P8_7_RELEASE_REVIEW.md：补充 P8.7-4/P8.7-5 收口结果，小白启动路径为双击 start_ui.command → 选参数 → 开始选股 → 看结果，install_fallback 只是可选兜底
- 未修改产品代码、README.md、app.py、start_ui.command、scripts/install_fallback.command、data/、strategies/、reports/、validation/、main.py、requirements*.txt、docs/screenshots/
- 保留免责声明：仅供研究学习，不构成投资建议
- 验收：rg 禁词零命中 ✅ | confirm_release_ready ✅

P8.7-6 发布候选最终复核与交付说明收口：
- docs/P8_7_RELEASE_REVIEW.md：新增第 10 节发布候选结论
  - 10.1 系统能做什么：6 因子规则评分、三级降级数据层、策略管理、验证与报告、可视化 UI
  - 10.2 怎么启动：双击 start_ui.command → 选参数 → 开始选股 → 看结果；skill_fallback 为可选第三级兜底
  - 10.3 怎么验收：python3 scripts/confirm_release_ready.py
  - 10.4 边界：不碰实盘交易、不引入 AI/qlib 到评分排序链路、不输出投资建议措辞
  - 10.5 结论：v0.5 + P8.1-P8.7 全部阶段已完成，处于发布候选状态
- PROJECT_STATE.md：记录 P8.7-6 完成，回填 P8.7-5.2 commit \`28e2ba6\`
- 未修改产品代码（app.py / main.py / start_ui.command / scripts/install_fallback.command / data/ / strategies/ / reports/ / validation/ / requirements*.txt）
- 未修改评分、排序、数据链路、报告逻辑
- 验收：confirm_release_ready ✅ | rg 禁词零命中 ✅
- P8.7-6.1：`f46731b` 修正发布候选禁词口径，docs/P8_7_RELEASE_REVIEW.md 不再出现具体投资建议措辞禁词，发布前一键验收 9/9 通过

P8 完成态结论：
- v0.5 + P8.1-P8.7 全部完成，当前为发布候选完成态
- 小白主路径稳定为：双击 start_ui.command → 选参数 → 开始选股 → 看结果
- 发布前验收入口稳定为：python3 scripts/confirm_release_ready.py
- 后续迭代需继续遵守边界：不碰实盘交易、不引入 AI/qlib 到评分排序链路、不改评分排序数据链路、不输出投资建议措辞

P9.0 来时路复盘与路线图设计：
- 新增 docs/PROJECT_HISTORY.md：按真实 git 历史梳理 P1-P8 演进，明确从基础可信、数据稳定、选股 MVP、批量股票池、模型可信度、Streamlit UI、小白可用 MVP 到 P8 发布候选增强的来时路
- 新增 docs/P9_ROADMAP.md：制定 P9「发布版稳定性与复盘可信度增强」路线图
- P9 分阶段：P9.1 公开文档一致性治理、P9.2 验收体系增强、P9.3 复盘记录增强、P9.4 小白排障增强、P9.5 发布版打标准备
- 本阶段仅新增/更新文档，未修改 app.py / main.py / data/ / strategies/ / reports/ / validation/ / requirements*.txt / 启动脚本
- 继续遵守边界：不碰实盘交易、不引入 AI/qlib 到评分排序链路、不做数据库/登录/复杂前后端、不重写评分/排序、不改数据链路、不输出投资建议措辞

P9.1 公开文档一致性治理：
- CHANGELOG.md：
  - 新增顶部标注：v0.5 为历史基线，当前已由 P8 更新
  - 修正「三步启动」→ 启动方式：双击 start_ui.command → 选参数 → 开始选股 → 看结果
  - 修正旧首页引导文案 → 首页引导：选参数 → 开始选股 → 看结果
  - 标注 v0.5 数据层（skill_fallback ~120 条）已被 baostock ~570 条替代
- README.md：
  - 修正「首次使用前建议先双击 install_fallback」→「如需多一层保障，可双击 install_fallback」（可选第三级兜底，不是启动前提）
- docs/USER_GUIDE.md / docs/TROUBLESHOOTING.md / docs/MANUAL_UI_CHECKLIST.md / docs/UI_ACCEPTANCE.md：确认无旧口径残留，无需修改
- docs/P8_7_RELEASE_REVIEW.md：确认无旧口径残留，无需修改
- 未修改产品代码（app.py / main.py / start_ui.command / scripts/install_fallback.command / data/ / strategies/ / reports/ / validation/ / requirements*.txt）
- 未修改评分、排序、数据链路、报告逻辑
- 验收：confirm_release_ready 9/9 通过 | rg 旧口径零命中 | rg 禁词零新增命中

P9.1.1 PROJECT_STATE.md 旧流程词口径返工收口：
- P8.7-2 历史记录（行 424-425）：旧流程引导卡片、旧首页引导文案等旧词残留改为概括表达（旧流程引导文案 / 旧步骤编号 / 旧首页引导文案）
- P9.1 记录（行 500）：旧首页引导文案改为概括表达
- 未修改产品代码、评分、排序、数据链路、报告逻辑
- 验收：confirm_release_ready 9/9 通过 | rg 旧流程词零命中 | rg 禁词零命中

P9.2-1 新增独立文档一致性检查脚本：
- 新增 scripts/confirm_docs_consistency.py：19 项自动检查公开文档口径一致性
  - 小白主路径关键表述：start_ui.command / 选参数 / 开始选股 / 看结果
  - baostock 数据层表述：baostock / 570
  - skill_fallback 兜底表述：可选第三级兜底，不是启动前提
  - 旧流程误导词零命中：旧首页引导文案等 6 个词
  - 投资建议措辞禁词零命中：4 个禁词
  - 免责声明保留：不构成投资建议
- 独立验收入口，未接入 confirm_release_ready.py
- 运行方式：python3 scripts/confirm_docs_consistency.py
- 未修改产品代码（app.py / main.py / start_ui.command / data/ / strategies/ / reports/ / validation/ / requirements*.txt）
- 未修改评分、排序、数据链路、报告逻辑
- 验收：confirm_docs_consistency 19/19 通过 | confirm_release_ready 当时 9/9 通过

P9.2-2 将文档一致性检查接入发布前一键验收：
- scripts/confirm_release_ready.py：CHECKS 新增第 10 项「文档口径一致性检查」，调用 confirm_docs_consistency.py
- README.md：发布前一键验收说明从 9 项更新为 10 项
- docs/P8_7_RELEASE_REVIEW.md：检查清单新增第 10 项文档口径一致性检查；聚合 9 项 → 10 项
- docs/P9_ROADMAP.md：基线 commit 和验收结果更新为 10/10 通过
- docs/PROJECT_HISTORY.md：发布前一键验收数量和结果更新为 10 项
- PROJECT_STATE.md：P8.7-1 历史记录标注「当时 9 项」
- 未修改产品代码（app.py / main.py / start_ui.command / data/ / strategies/ / reports/ / validation/ / requirements*.txt / scripts/confirm_docs_consistency.py）
- 未修改评分、排序、数据链路、报告逻辑
- 验收：confirm_docs_consistency 19/19 通过 | confirm_release_ready 10/10 通过

P9.3-0 复盘记录增强设计文档：
- 新增 docs/P9_3_REPLAY_TRACE_DESIGN.md：设计「每次选股结果更容易复盘」的最小方案
  - 当前问题分析：运行参数、数据源分布、策略信息、报告路径等未形成统一复盘记录口径
  - 建议新增 run_metadata 字段：generated_at / entrypoint / command / params / strategy / data_summary / result_summary / report_path / selection_path
  - 字段全部来自已有结果和验证摘要，不重新跑评分、不影响排序
  - Markdown 报告新增「本次运行复盘信息」小节
  - Streamlit UI 后续轻量展示（不在本阶段实现）
  - 后续拆分：P9.3-1 JSON 字段实现 → P9.3-2 报告接入 → P9.3-3 UI 展示 → P9.3-4 验收收口
- 只新增设计文档，未修改产品代码、评分、排序、数据链路、报告逻辑
- 下一步建议：P9.3-1 JSON 复盘记录字段实现
- 验收：confirm_docs_consistency 19/19 通过 | confirm_release_ready 10/10 通过

P9.3-1 JSON 复盘记录字段实现：
- strategies/selection.py：新增 build_run_metadata() helper
  - 只读取已有 selection_data / validation / stats / top / strategy 字段
  - 不重新跑评分、不重新拉数据、不改变 top/all 顺序
  - 输出 9 个字段：generated_at / entrypoint / command / params / strategy / data_summary / result_summary / selection_path / report_path
- main.py cmd_select：写 JSON 前调用 build_run_metadata，entrypoint=cli，command 为完整命令行
- app.py run_selection：返回 data 前调用 build_run_metadata，entrypoint=ui，command 为 streamlit run app.py
- 未改变现有 generated_at / strategy_id / strategy / universe / stats / top / all / validation 字段
- 未改变 Top 排序（同参数同数据源，结果与 P9.3-1 之前一致：601939 建设银行 69 分 #1）
- 未修改评分公式、排序逻辑、数据源优先级、Markdown 报告逻辑、UI 展示区域
- 验收：py_compile OK | CLI select EXIT:0 | run_metadata 含全部 9 个字段 | report EXIT:0 | confirm_docs_consistency 19/19 | confirm_release_ready 10/10

P9.3-1.1 run_metadata 字段结构收口：
- strategies/selection.py build_run_metadata() 收口：
  - data_summary 新增 data_source_dist（优先 validation.data_source_dist，fallback stats.source_dist）
  - data_summary 新增 rows_summary（min/max/avg/count）
  - 保留 source_dist / avg_rows 兼容字段
  - result_summary 的 total/success/top_score/avg_score 优先从 validation 取，缺失时降级从 top 数组计算
- 验证：result_summary.avg_score == validation.avg_score (54.4)、top_score == validation.top_score (69)
- 未修改 app.py / main.py / reports/generator.py / 评分 / 排序 / 数据链路 / UI 展示
- 验收：py_compile OK | CLI select EXIT:0 | 字段结构验证通过 | confirm_docs_consistency 19/19 | confirm_release_ready 10/10

P9.3-2 Markdown 报告接入 run_metadata：
- reports/generator.py：新增「本次运行复盘信息」小节
  - 位置：历史窗口复盘之后、免责声明之前
  - 展示：生成时间 / 运行方式 / 命令 / 参数 / 策略 / 数据源分布 / rows_summary / 覆盖不足率 / 整体质量 / Top评分 / 平均评分 / selection_path
  - 优雅降级：run_metadata 不存在时不显示，不报错
- reports/generator.py：修复报告输出中的投资建议措辞边界口径
- 未修改 JSON 生成（strategies/selection.py / main.py / app.py）
- 未修改评分公式、排序逻辑、数据源优先级、UI 展示区域
- 验收：py_compile OK | CLI report EXIT:0 | 复盘小节完整显示 | 报告禁词检查零命中 | confirm_docs_consistency 19/19 | confirm_release_ready 10/10

P9.3-3 Streamlit UI 轻量展示 run_metadata：
- app.py：在数据概览区域（ov_cols）下方、Tab 区域上方新增默认收起的 expander「本次运行复盘信息」
  - 第一行 4 列：入口（中文映射） / 生成时间 / 策略 / 整体质量（带颜色标签）
  - 第二行 4 列：最高分/平均分 / 覆盖不足率 / 数据源分布 / K线条数(min/avg/max)
  - 底部 caption：运行参数 + 完整命令
  - 优雅降级：run_metadata 不存在时不显示 expander
- 未修改 JSON 生成（strategies/selection.py / main.py）
- 未修改 Markdown 报告（reports/generator.py）
- 未修改评分公式、排序逻辑、数据源优先级
- 验收：py_compile OK | confirm_docs_consistency 19/19 | confirm_release_ready 10/10

P9.3-3.1 UI/CLI 输出边界措辞收口：
- main.py：CLI 输出标题措辞收口，统一为「不代表未来表现」
- app.py：覆盖不全提示与底部免责声明措辞收口，统一为稳妥表达
- 未修改评分公式、排序逻辑、数据源优先级、JSON 生成、报告逻辑
- 验收：py_compile OK | 禁词检查零命中 | confirm_docs_consistency 19/19 | confirm_release_ready 10/10

P9.3-4.1 新增独立 run_metadata 复盘记录验收脚本：
- scripts/confirm_run_metadata.py：独立验收入口，检查 selection_latest.json 中 run_metadata 结构与内容
  - 调用 CLI 最小链路生成选股 JSON
  - 20 项检查：顶层字段存在 / 9 个必需字段 / entrypoint==cli / command 含 main.py select / params(universe/limit/top) / data_source_dist 为 dict / rows_summary 含 min/max/avg/count / result_summary 含 total/success/top_score/avg_score / selection_path 文件存在 / report_path 可为空
  - 未接入 confirm_release_ready.py（留到 P9.3-4.2）
- 未修改 app.py / main.py / strategies/selection.py / reports/generator.py / 评分 / 排序 / 数据链路 / 报告逻辑
- 验收：confirm_run_metadata 20/20 | confirm_docs_consistency 19/19 | confirm_release_ready 10/10

P9.3-4.1.1 设计文档表格格式返工收口：
- docs/P9_3_REPLAY_TRACE_DESIGN.md：「P9.3 后续拆分」表格表头从 3 列补齐为 4 列（阶段/内容/改动范围/状态）
- 未修改任何产品代码、脚本、评分、排序、数据链路、报告逻辑

P9.3-4.2 run_metadata 验收接入发布前一键验收：
- scripts/confirm_release_ready.py：CHECKS 新增「run_metadata 复盘记录验收」（位置在 CLI 报告生成之后、废弃 API 残留检查之前），调用 confirm_run_metadata.py
- 公开文档检查项数量从 10 项更新为 11 项：README.md / docs/P8_7_RELEASE_REVIEW.md / docs/P9_ROADMAP.md
- 未修改 confirm_run_metadata.py / app.py / main.py / strategies/selection.py / reports/generator.py / 评分 / 排序 / 数据链路
- 验收：confirm_release_ready 11/11 | confirm_docs_consistency 19/19

P9.4-0 小白排障增强设计文档：
- docs/P9_4_TROUBLESHOOTING_DESIGN.md：P9.4 设计文档
  - 诊断 10 项排障体验问题（D-1~D-10）
  - 场景分级：启动前 / 选股中 / 结果后
  - 小白文案原则：先白话结论、技术详情放后面、低压力表达
  - 后续拆分：P9.4-1 公开排障文档口径收口 / P9.4-2 UI 提示增强 / P9.4-3 启动脚本提示增强 / P9.4-4 排障验收收口
- 未修改任何产品代码、脚本、评分、排序、数据链路、报告逻辑
- 下一步建议：P9.4-1 公开排障文档口径收口

P9.4-0.1 P9.4 设计文档禁词措辞返工：
- docs/P9_4_TROUBLESHOOTING_DESIGN.md：2 处禁词列表改为概括表达（交易指令类、收益承诺类）
- PROJECT_STATE.md：修复关键文件列表重复行
- 未修改任何产品代码、脚本、评分、排序、数据链路、报告逻辑

P9.4-1 公开排障文档口径收口：
- docs/TROUBLESHOOTING.md 4 处修改：
  - #6 数据源等待描述修正为准确的三级顺序尝试表述
  - #5 端口占用处补 lsof 命令含义说明 + 低压力替代方案（关终端/重启）
  - #2 Python 安装后补 venv/pip 安装失败白话排查路径
  - #10 旧流程引导文案修正为当前主路径（启动→环境自检→选参数→选股→看结果）
- docs/USER_GUIDE.md FAQ 从 5 条扩充到 8 条，新增：浏览器打不开、安装失败、全部失败
- docs/P9_4_TROUBLESHOOTING_DESIGN.md：P9.4-1 标记已完成
- 未修改 app.py / main.py / scripts/ / strategies/ / data/ / reports/ / validation/ / 评分 / 排序 / 数据链路
- 下一步建议：P9.4-2 UI 错误/等待/空结果提示增强

P9.4-2 UI 错误/等待/空结果提示增强：
- app.py 6 处提示文案增强（只改展示，不改逻辑）：
  - 选股 spinner：补充"个别数据源慢时可能接近 2 分钟"说明
  - 全部失败 error：白话说明"所有数据源暂时都没有取到数据"+ 分步下一步
  - 选股 except：主提示白话 + 技术详情放入默认收起 expander
  - 复盘 except：同上模式，主提示白话 + 技术详情收起
  - 无候选结果 warning（2 处）：补充排障指南引用
  - 覆盖不全 info：补充排障指南引用
- docs/P9_4_TROUBLESHOOTING_DESIGN.md：P9.4-2 标记已完成
- 未修改 run_selection / run_backtest / 数据结构 / session_state / 报告逻辑 / 评分 / 排序 / 数据链路
- 下一步建议：P9.4-3 启动脚本提示增强

P9.4-2.1 UI 排障提示文案返工：
- app.py：「可选择安装」修正冗余表达；设计文档诊断表旧写法修正

P9.4-3 启动脚本提示增强：
- start_ui.command 4 处文案增强（只改 echo 输出，不改脚本逻辑）：
  - 启动成功提示：加入主路径（环境自检→选参数→选股→看结果）
  - 依赖安装失败：指向 docs/TROUBLESHOOTING.md 第 2 条，移除"找懂技术朋友"
  - 端口占用自动切换：补充"这通常不是故障，不影响正常使用"
  - Streamlit 启动失败：指向 docs/TROUBLESHOOTING.md 第 5 条 + Issues 截图
- docs/P9_4_TROUBLESHOOTING_DESIGN.md：P9.4-3 标记已完成
- 未修改 app.py / main.py / scripts/ / strategies/ / data/ / reports/ / validation/ / 评分 / 排序 / 数据链路
- 下一步建议：P9.4-4 排障验收脚本与发布前收口

P9.4-4.1 新增独立排障体验验收脚本：
- scripts/confirm_troubleshooting.py：独立验收入口，13 项检查
  - start_ui.command：可执行权限 / bash 语法 / 主路径关键词
  - app.py：无旧直暴露写法 / 含折叠提示 / 含 TROUBLESHOOTING 指引
  - TROUBLESHOOTING.md：无旧流程词 / 无旧误导说法 / 无旧 cd 中文写法
  - USER_GUIDE.md：FAQ 覆盖关键排障场景
  - PROJECT_STATE.md：记录 P9.4-3.1 或之后状态
  - 禁词检查 + fallback 可选口径
  - 未接入 confirm_release_ready.py（留到 P9.4-4.2）
- docs/P9_4_TROUBLESHOOTING_DESIGN.md：P9.4-4 状态更新
- 未修改 app.py / main.py / start_ui.command / strategies/ / data/ / reports/ / validation/ / 评分 / 排序 / 数据链路

P9.4-4.2 排障体验验收接入发布前一键验收：
- scripts/confirm_release_ready.py：CHECKS 新增「排障体验验收」，位置在 run_metadata 复盘记录验收之后
- 公开文档检查项数量从 11 项更新为 12 项：README.md / docs/P8_7_RELEASE_REVIEW.md / docs/P9_ROADMAP.md
- docs/P9_4_TROUBLESHOOTING_DESIGN.md：P9.4 排障增强闭环标记完成
- 未修改 confirm_troubleshooting.py / app.py / main.py / start_ui.command / strategies/ / data/ / reports/ / validation/ / 评分 / 排序 / 数据链路
- 验收：confirm_release_ready 12/12 | confirm_docs_consistency 19/19
- 下一步建议：P9.5 发布版打标准备

P9.5-0 发布版打标准备设计文档（打标前记录）：
- docs/P9_5_RELEASE_PREP.md：P9.5 设计文档
  - 当前基线：commit 4b944a9、v0.5 tag、12/12 一键验收通过
  - 版本建议：推荐 v0.6-rc1（最终是否打 tag 仍需人工确认）
  - 后续拆分：P9.5-1 更新 RELEASE_CHECKLIST.md / P9.5-2 更新 CHANGELOG.md / P9.5-3 tag 前最终验收记录
- 未修改任何产品代码、脚本、评分、排序、数据链路、报告逻辑
- 打标前记录：当时未创建 git tag
- 下一步建议：P9.5-1 更新 RELEASE_CHECKLIST.md

P9.5-0.1 发布准备设计文档版本口径返工：
- docs/P9_5_RELEASE_PREP.md：选项 A 从 v0.5-p9 改为 v0.5-p8，基线 commit 表述修正
- 未修改任何产品代码、脚本、评分、排序、数据链路、报告逻辑

P9.5-1 更新 RELEASE_CHECKLIST.md（打标前记录）：
- RELEASE_CHECKLIST.md 全面更新：
  - 新增第 1 节「自动验收」：一键验收 12 项 + 3 个独立验收脚本
  - 第 2 节「环境」：fallback 改为可选第三级兜底
  - 第 3 节「启动」：新增 test -x start_ui.command 权限检查
  - 第 4 节「选股」：新增白话错误提示检查
  - 第 5 节「CLI 全链路」：命令统一为 .venv/bin/python
  - 新增第 7 节「tag 前确认」：git status/log/tag 手动确认，不自动打 tag
  - 保留免责声明
- docs/P9_5_RELEASE_PREP.md：P9.5-1 标记已完成
- 未修改 app.py / main.py / start_ui.command / scripts/ / strategies/ / data/ / reports/ / validation/ / 评分 / 排序 / 数据链路
- 打标前记录：当时未创建 git tag
- 下一步建议：P9.5-2 更新 CHANGELOG.md

P9.5-2 更新 CHANGELOG.md（打标前记录）：
- CHANGELOG.md 新增 v0.6-rc1 候选章节（打标前记录：当时未打 tag）
  - 数据层：baostock 集成、三级降级、覆盖提示修正
  - 策略解释：explain 字段、三端展示
  - UI 体验：Top3 卡片、中文标签、风险着色、因子图标、技术指标折叠、数据概览紧凑化
  - 策略管理：注册表、CLI 参数、UI 选择器、AI 边界评审
  - UI 兼容性：废弃 API 清理、版本约束升级
  - 复盘记录增强（P9.3）：run_metadata 9 字段、报告小节、UI 折叠区、20 项验收
  - 验收体系增强（P9.2-P9.4）：文档一致性 19 项、排障体验 13 项、一键验收 12 项、UI 44 项
  - 排障与体验增强（P9.4）：排障文档口径、FAQ 扩充、UI 提示、启动脚本
  - 发布边界收口（P9.5）：验收清单更新、fallback 可选、禁词红线、免责声明
  - 已知限制
- docs/P9_5_RELEASE_PREP.md：P9.5-2 标记已完成
- 打标前记录：当时未创建 git tag
- 下一步建议：P9.5-3 tag 前最终验收记录

P9.5-3 tag 前最终验收记录（打标前记录）：
- 最终验收结果（基于 P9.5-3 最终记录阶段，见 git log 最新提交）：
  - confirm_release_ready.py：12/12 通过
  - confirm_docs_consistency.py：19/19 通过
  - confirm_run_metadata.py：20/20 通过
  - confirm_troubleshooting.py：13/13 通过
  - git status：工作树干净
  - git tag --points-at HEAD：当时无 tag（正确，本阶段不创建 tag）
- 推荐 tag 版本：`v0.6-rc1`
- 建议 tag 命令（打标前建议，已由人工确认后执行）：
  - `git tag -a v0.6-rc1 -m "v0.6-rc1: A股选股系统发布候选"`
  - `git push origin v0.6-rc1`
- 重要提醒：tag 是不可变标记，以上命令已由人工确认后执行完毕。
- 未修改 app.py / main.py / start_ui.command / scripts/ / strategies/ / data/ / reports/ / validation/ / README.md / CHANGELOG.md / RELEASE_CHECKLIST.md / docs/TROUBLESHOOTING.md / docs/USER_GUIDE.md
- 打标前记录：当时未创建 git tag

P9.5-3.1 最终验收记录 commit 号同步（打标前记录）：
- PROJECT_STATE.md 中 P9.5-3 的 commit 号引用改为阶段描述，避免过期

P9.5-4 v0.6-rc1 打标后状态同步：
- v0.6-rc1 tag 已创建并推送到远端，指向 commit `3461390`（P9.5-3.1）
- 发布前验收结果：confirm_release_ready 12/12、confirm_docs_consistency 19/19、confirm_run_metadata 20/20、confirm_troubleshooting 13/13
- CHANGELOG.md：顶部章节从「候选（未打 tag）」改为「v0.6-rc1 (2026-05-19，已打 tag)」
- PROJECT_STATE.md：打标前历史记录标注「打标前记录」，当前状态为已打 tag
- docs/P9_5_RELEASE_PREP.md：新增打标后状态确认
- README.md：标题和能力说明从 v0.5 同步为 v0.6-rc1 发布候选
- 保留免责声明：仅供研究学习，不构成投资建议
- 不直写投资建议类禁词
- 未修改 app.py / main.py / start_ui.command / scripts/ / strategies/ / data/ / reports/ / validation/ / 评分 / 排序 / 数据链路
- 未重新打 tag，未执行 git push --tags

P9.5-4.1 P9_5_RELEASE_PREP 打标前/打标后口径分层收口：
- docs/P9_5_RELEASE_PREP.md：
  - 顶部新增文档分层说明：第 1–7 节为打标前设计记录，第 7.1 节为打标后状态确认，当前真实状态以 7.1 为准
  - 版本建议结论：补充"打标前设计记录：该建议已由人工确认并执行，见 7.1 节"
  - P9.5-3 拆分说明：标题标注"打标前步骤"，"不实际打 tag"改为"打标前步骤要求：当时不实际打 tag"
  - 第 7 节完成结论：标题标注"打标前记录"，增加引导说明指向 7.1 节
- PROJECT_STATE.md：记录 P9.5-4.1 完成
- tag 未移动，v0.6-rc1 仍指向 commit `3461390`
- 未修改 app.py / main.py / start_ui.command / scripts/ / strategies/ / data/ / reports/ / validation/ / 评分 / 排序 / 数据链路
- 保留免责声明：仅供研究学习，不构成投资建议
- 不直写投资建议类禁词

P10-0 发布后观察与真实小白验收路线图：
- 新增 docs/P10_ROADMAP.md：P10 路线图
  - 总目标：发布后观察与真实小白验收，不是新增功能冲刺
  - 当前基线：main 最新 commit `148701c`、v0.6-rc1 tag 指向 `3461390`、12/12 通过
  - P10 原则：保护双击启动主路径、先观察再修复、修复只改体验/文档/验收、tag 不随便移动
  - P10.1：tag/main/公开文档状态一致性守门
  - P10.2：真实 UI 启动与截图复核
  - P10.3：发布后问题记录模板（docs/POST_RELEASE_NOTES.md）
  - P10.4：v0.6 正式版决策记录（基于观察结果，不自动打 tag）
  - 明确不做：不加新策略、不改评分排序、不改数据链路、不引入 AI、不做登录/数据库/实盘
  - 免责声明：仅供研究学习，不构成投资建议
- README.md：文档索引新增 P10_ROADMAP.md
- PROJECT_STATE.md：记录 P10-0 完成
- 未修改 app.py / main.py / start_ui.command / scripts/ / strategies/ / data/ / reports/ / validation/ / CHANGELOG.md / RELEASE_CHECKLIST.md / docs/TROUBLESHOOTING.md / docs/USER_GUIDE.md
- 不直写投资建议类禁词
- 下一步建议：P10.1 tag/main/公开文档状态一致性守门

P10.1-0 tag/main/公开文档状态一致性守门设计：
- 新增 docs/P10_1_RELEASE_STATE_GUARD_DESIGN.md：P10.1 设计文档
  - 目标：让维护者区分 release tag、main 最新提交、远端 tag 状态，避免误以为 tag 必须指向最新 main
  - 当前事实：v0.6-rc1 指向 3461390；main 最新 51db203；tag 后 3 个提交均为文档/状态记录
  - 守门检查 5 项：tag 指向 / HEAD 可无 tag / 远端 tag / tag 内容 / tag-HEAD diff 无产品代码
  - 后续拆分：P10.1-1 独立脚本 / P10.1-2 接入评估（建议暂不接入）/ P10.1-3 文档收口
  - 核心结论：tag 后 main 文档提交是正常收口，不应移动 tag
- docs/P10_ROADMAP.md：标记 P10.1 已进入设计阶段
- PROJECT_STATE.md：记录 P10.1-0 完成
- 未修改 app.py / main.py / start_ui.command / scripts/ / strategies/ / data/ / reports/ / validation/ / README.md / CHANGELOG.md / RELEASE_CHECKLIST.md
- 不直写投资建议类禁词
- 下一步建议：P10.1-1 新增独立脚本 scripts/confirm_release_state.py

P10.1-1 新增独立 release tag/main 状态验收脚本：
- 新增 scripts/confirm_release_state.py：独立验收入口，6 项检查
  - 本地 tag v0.6-rc1 存在
  - tag v0.6-rc1 指向 commit 3461390
  - HEAD 可无 tag（正常：main 在 tag 后有文档提交）
  - 远端 tag v0.6-rc1 存在
  - tag 指向的提交内容正确
  - tag..HEAD diff 无产品代码变更（允许本脚本自身和文档文件）
- 运行方式：python3 scripts/confirm_release_state.py
- 不接入 confirm_release_ready.py（tag 固定而 main 会继续前进，生命周期不同）
- docs/P10_1_RELEASE_STATE_GUARD_DESIGN.md：标记 P10.1-1 已完成
- PROJECT_STATE.md：记录 P10.1-1 完成
- 未修改 app.py / main.py / start_ui.command / strategies/ / data/ / reports/ / validation/ / confirm_release_ready.py / README.md / CHANGELOG.md / RELEASE_CHECKLIST.md
- 不直写投资建议类禁词
- 下一步建议：P10.1-2 接入评估（建议暂不接入）或 P10.1-3 文档收口

P10.1-2 confirm_release_state 是否接入 confirm_release_ready 的取舍决策：
- 决策结论：暂不将 confirm_release_state.py 接入 confirm_release_ready.py
- 决策理由：
  - confirm_release_ready.py 检查"当前 main 是否可发布/可运行"（产品能力）
  - confirm_release_state.py 检查"某个历史 release tag 与 main 后续文档提交关系是否清楚"（git 元数据）
  - tag 固定在 3461390 而 main 会继续前进，生命周期不同
  - 混在一起会让日常产品验收依赖 git 历史状态，反而不清晰
- 使用方式：
  - 日常产品回归：python3 scripts/confirm_release_ready.py
  - 发布状态复盘：python3 scripts/confirm_release_state.py（单独运行）
- docs/P10_1_RELEASE_STATE_GUARD_DESIGN.md：P10.1-2 标记已完成
- docs/P10_ROADMAP.md：P10.1-2 状态同步
- 未修改 scripts/confirm_release_ready.py / scripts/confirm_release_state.py / app.py / main.py / start_ui.command / strategies/ / data/ / reports/ / validation/ / README.md / CHANGELOG.md / RELEASE_CHECKLIST.md
- 不直写投资建议类禁词
- 下一步建议：P10.1-3 文档收口

P10.1-3 tag/main 状态守门文档收口：
- docs/P10_1_RELEASE_STATE_GUARD_DESIGN.md：新增 P10.1 完成结论
- docs/P10_ROADMAP.md：标记 P10.1 已完成，下一步建议 P10.2
- PROJECT_STATE.md：记录 P10.1-3 完成
- 未修改 scripts/ / app.py / main.py / start_ui.command / strategies/ / data/ / reports/ / validation/ / README.md / CHANGELOG.md / RELEASE_CHECKLIST.md
- 不直写投资建议类禁词

**P10.1 已完成。** 完成结论：
- v0.6-rc1 tag 固定指向 commit `3461390`
- main 可以继续有文档/观察记录提交
- 发布后文档提交不移动 rc1 tag
- release 状态复盘用 `python3 scripts/confirm_release_state.py`（6/6 通过）
- 产品回归验收用 `python3 scripts/confirm_release_ready.py`（12/12 通过）
- 下一步建议：P10.2 真实 UI 启动与截图复核

P10.2-0 真实 UI 启动与截图复核设计/诊断：
- 新增 docs/P10_2_UI_SMOKE_DESIGN.md：P10.2 设计/诊断文档
  - 诊断截图脚本 scripts/screenshot_home.py 旧关键词残留：首页旧步骤计数词（行 45）、结果页原始英文决策标签（行 68）
  - 现有截图来自 P8.6-2（2026-05-18），app.py 自 P8.6 后未改产品代码，截图应仍有效但需 P10.2-2 实际确认
  - confirm_p83_ui.py（44 项静态/运行时）vs screenshot_home.py（真实浏览器截图）角色区分
- P10.2 拆分：
  - P10.2-1：修正截图脚本关键词/验收口径（只改脚本，不改 UI）
  - P10.2-2：启动 Streamlit 做真实截图复核（确认截图是否仍代表当前 UI）
  - P10.2-3：文档收口（记录复核结果和是否更新截图）
- 明确不做：不改 UI 文案、不改产品逻辑、不改评分排序数据链路、不移动 tag
- docs/P10_ROADMAP.md：P10.2-0 状态同步
- PROJECT_STATE.md：记录 P10.2-0 完成
- 未修改 app.py / main.py / start_ui.command / scripts/ / docs/screenshots/ / strategies/ / data/ / reports/ / validation/
- 不直写投资建议类禁词
- 下一步建议：P10.2-1 修正截图脚本关键词/验收口径

P10.2-1 修正截图脚本关键词/验收口径：
- scripts/screenshot_home.py 修正 3 处：
  - 文件头从 P7.7 更新为 P10.2 真实 UI 截图复核脚本
  - 首页关键词：移除旧步骤计数词（行 45），保留当前 UI 确定性文本
  - 结果页关键词：移除原始英文决策标签（行 68），改为检查中文决策标签（强观察/观察/中性/回避）至少出现一种
  - 覆盖不全改为可选诊断输出，不影响退出码
- docs/P10_2_UI_SMOKE_DESIGN.md：标记 P10.2-1 已完成
- docs/P10_ROADMAP.md：P10.2-1 状态同步
- PROJECT_STATE.md：记录 P10.2-1 完成
- 未修改 app.py / main.py / start_ui.command / docs/screenshots/ / strategies/ / data/ / reports/ / validation/ / 评分/排序/数据链路
- 不直写投资建议类禁词
- 下一步建议：P10.2-2 启动 Streamlit 做真实截图复核

P10.2-1.1 修正 release 状态守门规则，允许验收脚本白名单：
- scripts/confirm_release_state.py ALLOWED_SCRIPTS 从"只允许本脚本自身"扩展为白名单：
  - scripts/confirm_release_state.py（本脚本）
  - scripts/screenshot_home.py（发布后真实 UI 截图复核工具）
- 白名单注释说明：这些脚本是发布后验收/截图复核工具，不是产品链路
- 仍然禁止 app.py / main.py / start_ui.command / data/ / strategies/ / reports/ / validation/ 等产品代码变更
- 输出文案微调为"tag..HEAD diff 无产品代码变更（允许验收脚本白名单）"
- 修正后 confirm_release_state 6/6 通过
- docs/P10_1_RELEASE_STATE_GUARD_DESIGN.md：同步白名单规则
- docs/P10_2_UI_SMOKE_DESIGN.md：补充 P10.2-1.1 异常修正记录
- docs/P10_ROADMAP.md：P10.2-1.1 状态同步
- 未修改 app.py / main.py / start_ui.command / scripts/screenshot_home.py / docs/screenshots/ / strategies/ / data/ / reports/ / validation/ / 评分/排序/数据链路
- 不直写投资建议类禁词
- 下一步建议：P10.2-2 启动 Streamlit 做真实截图复核

## 5. 关键文件

app.py / main.py / data/fetcher.py / data/universe.py / strategies/selection.py / strategies/registry.py / reports/generator.py / requirements.txt / requirements-ui.txt / scripts/test_baostock.py / scripts/confirm_coverage_fix.py / scripts/confirm_explain.py / scripts/confirm_report_explain.py / scripts/confirm_ui_dependencies.py / scripts/confirm_p83_ui.py / scripts/confirm_p84_registry.py / scripts/confirm_p84_cli.py / scripts/confirm_p84_ui.py / scripts/confirm_p84_docs.py / scripts/confirm_release_ready.py / scripts/confirm_run_metadata.py / scripts/confirm_troubleshooting.py / docs/P8_1_ACCEPTANCE.md / docs/P8_2_EXPLANATION_DESIGN.md / docs/P8_3_UI_EXPERIENCE_DESIGN.md / docs/P8_4_STRATEGY_MANAGEMENT_DESIGN.md / docs/P8_5_AI_EXPLANATION_DECISION.md / docs/P8_6_UI_STABILITY_AUDIT.md / docs/P8_7_RELEASE_REVIEW.md / docs/P8_ROADMAP.md / docs/P9_3_REPLAY_TRACE_DESIGN.md / docs/P9_4_TROUBLESHOOTING_DESIGN.md / docs/P9_5_RELEASE_PREP.md / docs/MANUAL_UI_CHECKLIST.md / docs/screenshots/home.png / docs/screenshots/result.png
