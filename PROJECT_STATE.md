# 项目状态交接摘要

> 最后更新：2026-05-14

## 1. 项目总目标

打造长期可用、结果可信、可复盘的 A 股选股系统。

当前阶段（P0-P5）：先把规则选股基础盘做好。不碰 AI、qlib、UI、实盘。

## 2. 当前完成阶段

| 阶段 | Commit | 内容 |
|------|--------|------|
| P0 | `661acb5` | 骨架 fix：数据失败标记/策略扫描/回测拒绝/AI降级/README去夸大 |
| P1 | `a353019` | 退出码修正/策略统计分离 |
| P2 | `b5469a0` | 多源fallback+缓存+selfcheck |
| P2fix| `8337269` | fallback --json/字段映射/JSON提取/timeout |
| P3 | `f9fec21` | 选股MVP：引擎/select命令/report接入 |
| P3.1 | `9154ff5` | coverage_warning/select--start/全失败EXIT=1 |
| P4 | `fbd4146` | 批量选股：universe模块/select--universe |
| P4.1 | `5eaf1b2` | static 55只/metadata/universe命令 |
| P4.2 | `ed9f8fb` | README/report统计/selection参数化/版本统一 |
| P4.3 | `4f69bd2` | report失败退出/产物时间戳/latest文件/v0.4 |
| P5.1 | `cc61377` | 多因子评分(6组100分)/decision/risk_level |
| P5.2 | *(current)* | coverage降权/confidence/决策联动 |

- 最新 commit: *(P5.2 in progress)*
- GitHub: https://github.com/xiarantang/a-share-selection-system
- 本地: `/Users/niuniu/projects/a-share-selection-system`

## 3. 当前真实能力

- ✅ 数据层：akshare + 多源fallback(腾讯/新浪/雪球/东财) + 本地缓存
- ✅ 股票池：static(55只)/hs300/top_amount/sample/manual + 名称行业
- ✅ 批量选股：6组因子评分(100分) + decision(strong_watch/watch/neutral/avoid) + risk_level(low/medium/high)
- ✅ 回测：backtrader A股适配(佣金/印花税/T+1)，空数据拒绝
- ✅ 报告：Markdown日报 + JSON/CSV，含因子拆分/来源说明/覆盖警告
- ✅ Pipeline：PASS/FAIL/WARN/SKIP检查表，退出码可信
- 🧪 AI/qlib：experimental
- ⚠️ 限制：fallback仅~120条K线，coverage_warning；akshare经常失败

## 4. 工程规则

1. 不允许假成功 — 失败必须 exit 1
2. 生成物必须时间戳 + latest: `selection_YYYYMMDD_HHMMSS.*` + `report_YYYYMMDD_HHMMSS.md` + `*_latest.*`
3. reports/output 和 data/cache 不提交 Git
4. 验收：py_compile → select → report → pipeline → git status
5. 完成后 commit + push

## 5. 下一阶段

- P5.x 选股模型持续收口（调优因子权重/阈值、与回测联动）
- 不碰 AI/qlib/UI/实盘

## 6. 关键文件

| 文件 | 用途 |
|------|------|
| `main.py` | 主入口 |
| `config/settings.py` | 全局配置 |
| `data/fetcher.py` | akshare + fallback + 缓存 |
| `data/universe.py` | 股票池 |
| `data/static_universe.json` | 55只A股元数据 |
| `strategies/selection.py` | 选股引擎 v2 |
| `strategies/registry.py` | Skill策略注册 |
| `backtest/engine.py` | 回测引擎 |
| `reports/generator.py` | 报告生成器 |
| `ai_models/qlib_runner.py` | 🧪 experimental |
| `agent/bridge.py` | 🧪 experimental |
| `paper_trading/engine.py` | 模拟交易 |
