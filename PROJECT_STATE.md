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
| P8.1-2 | _待commit_ | baostock小步接入数据层 |

- 🏷️ v0.5 已发布 tag `v0.5` → `81759aa`
- GitHub: https://github.com/xiarantang/a-share-selection-system

## 3. 真实能力 (v0.5 + P8.1-2)

- ✅ 数据：akshare + **baostock** + skill_fallback + 缓存；baostock稳定570条K线
- ✅ 选股：6因子评分 + decision/risk_level/confidence
- ✅ 验证：validate + backtest-validate + report
- ✅ 可视化：Streamlit 本地 UI
- ✅ Pipeline：PASS/FAIL退出码可信

## 4. 当前阶段 P8.1-2（已完成）

baostock 小步接入数据层：
1. baostock 加入 requirements.txt
2. data/fetcher.py 新增 `_fetch_baostock()`（~100行），插入 akshare 之后、skill_fallback 之前
3. 字段映射完整：date/open/high/low/close/volume/amount/pct_change/turnover/pre_close
4. 登录/登出管理，异常时 finally 释放连接
5. 函数签名不变，source 标记为 "baostock"
6. 修正 test_baostock.py：动态日期、达标率计算
7. CLI 全链路：语法8/8→select EXIT:0(10/10均为baostock)→backtest-validate EXIT:0→report EXIT:0
8. 覆盖不全从100%降至接近0

## 5. 关键文件

app.py / main.py / data/fetcher.py / data/universe.py / strategies/selection.py / requirements.txt / scripts/test_baostock.py
