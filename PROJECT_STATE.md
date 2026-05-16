# 项目状态交接摘要

> 最后更新：2026-05-16

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
- GitHub: https://github.com/xiarantang/a-share-selection-system

## 3. 真实能力 (v0.5 + P8.2-0)

- ✅ 数据：akshare + **baostock** + skill_fallback + 缓存；baostock稳定570条K线
- ✅ 选股：6因子评分 + decision/risk_level/confidence
- ✅ 验证：validate + backtest-validate + report
- ✅ 可视化：Streamlit 本地 UI
- ✅ Pipeline：PASS/FAIL退出码可信

## 4. 当前阶段 P8.2（策略可解释增强）

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

下一步 P8.2-1：小步实现 `_build_explain()` 并把 `explain` 字段追加到 `SelectionEngine.select()` 返回结果。只改 `strategies/selection.py` 和必要验证脚本，不碰报告/UI 展示。

## 5. 关键文件

app.py / main.py / data/fetcher.py / data/universe.py / strategies/selection.py / requirements.txt / scripts/test_baostock.py / scripts/confirm_coverage_fix.py / docs/P8_1_ACCEPTANCE.md / docs/P8_2_EXPLANATION_DESIGN.md
