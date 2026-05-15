# 项目状态交接摘要

> 最后更新：2026-05-15

## 1. 项目总目标

打造长期可用、结果可信、可复盘的 A 股选股系统。

**最终形态：小白可用的可视化选股系统。** 当前 CLI 命令只是底层引擎和验收入口。
路线：P5 打磨引擎 → P6 可视化界面(Streamlit) → P7 产品化打磨 → P8 AI 辅助
暂不碰实盘交易。

**禁止事项**：不碰 AI/qlib/实盘交易/复杂前后端分离/数据库/登录系统。

## 2. 当前完成阶段

| 阶段 | Commit | 内容 |
|------|--------|------|
| P0 | `661acb5` | 骨架 fix |
| P1 | `a353019` | 退出码修正 |
| P2 | `b5469a0` | 多源fallback+缓存 |
| P2fix| `8337269` | fallback --json |
| P3 | `f9fec21` | 选股MVP |
| P3.1 | `9154ff5` | coverage_warning |
| P4 | `fbd4146` | 批量选股 |
| P4.1 | `5eaf1b2` | static universe |
| P4.2 | `ed9f8fb` | README/report |
| P4.3 | `4f69bd2` | 产物时间戳 |
| P5.1 | `cc61377` | 多因子评分 |
| P5.2 | `b197370` | coverage降权 |
| P5.3 | `973fe09` | selection validation |
| P5.3.1| `fab4dda` | 文档收口 |
| P5.4 | `9c6e156` | 历史窗口复盘 |
| docs | `21eece8` | 产品目标文档化 |
| P6.0 | `5983451` | Streamlit 本地 UI 第一版 |
| P6.0收尾 | `f8f8fb9` | README小白启动方式/.venv入口/架构更新 |
| P6.1 | `87a30f6` | 一键启动脚本/状态交接/README完善 |
| P6.1.1 | `72e0185` | 轻量依赖/状态同步/README入口优化 |
| P6.1.2 | `c1baabc` | 状态交接修正/P7准备 |
| P7.0 | `c8135d9` | 产品化打磨第一版：界面体验/错误提示/数据覆盖可视化 |
| P7.0.1 | `06cd143` | 同步P7.0状态并补充UI验收路径 |
| P7.1 | `e89b855` | 真实UI验收记录/点击流检查/状态同步 |
| P7.1.1 | `28e7061` | 真实浏览器验收/端口友好处理/验收结果修正 |
| P7.1.2 | `bd86585` | 最终结果页截图/状态同步/覆盖提示强化 |
| P7.1.3 | `609f7f3` | 收口P7.1.2状态与UI验收说明 |
| P7.2 | `7efd25c` | MVP点击流检查/使用阻塞记录/状态同步 |
| P7.3 | `307ac57` | 小白阻塞修复：数据通道和首次安装提示 |
| P7.4 | `6ea0414` | 小白流程打磨：四步引导/验证外置/首次检查区 |
| P7.4文档 | `6a8539b` | 同步P7.4交付状态 |
| P7.5 | `e6e01d0` | 小白首次体验：三步最快启动/就绪状态/友好提示 |

- 最新已记录交付 commit: `e6e01d0`
- 当前仓库最新提交请以 `git log -1 --oneline` 为准
- GitHub: https://github.com/xiarantang/a-share-selection-system
- 本地: `/Users/niuniu/projects/a-share-selection-system`

## 3. 真实能力

- ✅ 数据：akshare+skill_fallback+缓存；当前小白体验以 skill_fallback 为主要可用通道 | 股票池：static 55只
- ✅ 选股：6因子评分 + decision/risk_level/confidence
- ✅ 验证：validate + backtest-validate + report
- ✅ 可视化：Streamlit 本地 UI，四步引导/三步最快启动/就绪状态/错误提示友好化/数据覆盖可视化/验证摘要外置/首次使用检查
- ✅ Pipeline：PASS/FAIL退-出码可信
- 🧪 AI/qlib：experimental（未来 P8 阶段，不参与当前小白启动）

## 4. 当前阶段 P7.5

P7.5 小白首次体验：
1. 数据源说明：akshare 不稳定时说明系统仍会使用 skill_fallback
2. 等待体验：默认 static + 10 只，提示 30-60 秒
3. 覆盖解释：coverage_warning 用白话解释为数据较短、已自动降置信度
4. 首次安装：提供 `scripts/install_fallback.command`
5. 首页流程：四步引导，未安装备用数据通道时显示首次安装说明
6. 验证外置：选股完成后，关键质量指标直接显示在 Tab 外
7. 首次检查区：显示 Python、备用数据通道、本地缓存、最近选股结果
8. 最快启动：README 顶部提供安装备用数据通道 -> 双击启动 -> 点击开始选股三步路径
9. 就绪状态：首页明确显示“可以开始选股”或“需要先安装备用数据通道”
10. 启动友好提示：`start_ui.command` 分步显示检测、安装、启动、端口占用和下一步操作

见 NEXT_PROMPT.md、docs/UI_ACCEPTANCE.md、docs/MANUAL_UI_CHECKLIST.md。

## 5. 关键文件

app.py / main.py / data/fetcher.py / data/universe.py / strategies/selection.py / validation/selection_validator.py / validation/backtest_validator.py / backtest/engine.py / reports/generator.py / start_ui.command / requirements-ui.txt / docs/UI_ACCEPTANCE.md / docs/UI_ACCEPTANCE_RESULT.md / docs/MANUAL_UI_CHECKLIST.md
