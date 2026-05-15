# 项目状态交接摘要

> 最后更新：2026-05-16

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
| P7.5文档 | `1662739` | 同步P7.5交付状态 |
| P7.6 | `b60b1a1` | 真实浏览器验收：截图留证/首页结果页双截图 |
| P7.6 final | `7359a4a` | 最终验收截图/UI文案修正/CLI全链路/状态同步 |
| P7.6文档 | `d23f56d` | 修正P7.6验收状态记录 |
| P7.7 | `ab10af7` | 验收证据持久化/小白交付包/截图脚本/USER_GUIDE/状态同步 |
| P7.7文档 | `fbf2615` | 同步P7.7交付状态 |
| P7.8 | `2d6f662` | 小白安装失败兜底/环境自检页/TROUBLESHOOTING/启动脚本强化 |
| P7.8文档 | `7920621` | 同步P7.8交付状态 |
| P7.9 | _待commit_ | 产品收口首页/v0.5发布准备/CHANGELOG/RELEASE_CHECKLIST |

- 最新已记录交付 commit: `7920621`，当前待 commit P7.9 (v0.5发布准备)
- 当前仓库最新提交请以 `git log -1 --oneline` 为准
- GitHub: https://github.com/xiarantang/a-share-selection-system
- 本地: `/Users/niuniu/projects/a-share-selection-system`

## 3. 真实能力 (v0.5)

- ✅ 数据：akshare+skill_fallback+缓存；当前小白体验以 skill_fallback 为主要可用通道 | 股票池：static 55只
- ✅ 选股：6因子评分 + decision/risk_level/confidence
- ✅ 验证：validate + backtest-validate + report
- ✅ 可视化：Streamlit 本地 UI，四步引导/三步最快启动/就绪状态/错误提示友好化/数据覆盖可视化/验证摘要外置/首次使用检查/环境自检/就绪判定
- ✅ Pipeline：PASS/FAIL退出码可信
- ✅ 排障：docs/TROUBLESHOOTING.md 覆盖常见 10 个小白问题
- ✅ 发布：CHANGELOG.md / RELEASE_CHECKLIST.md / 产品首页含截图预览
- 🧪 AI/qlib：experimental（未来 P8 阶段，不参与当前小白启动）

## 4. 当前阶段 P7.9（已完成）

P7.9 产品收口首页 + v0.5 发布准备：
1. README 重写为正式项目首页：版本号 v0.5 / 一句话说明 / 截图预览 / 三步启动 / 能力一览 / 已知限制 / 免责声明 / 文档索引
2. README 嵌入 `docs/screenshots/home.png` + `result.png` 截图展示
3. 新增 CHANGELOG.md：记录 v0.5 已完成能力（产品形态/小白体验/数据/选股/验证/验收/文档/CLI/限制）
4. 新增 RELEASE_CHECKLIST.md：发布前检查清单（环境/启动/选股/CLI/文档/Git/截图脚本）
5. 不改核心选股逻辑，仅 README/发布文档/少量必要文案
6. CLI 全链路：语法 8/8 → select EXIT:0 → backtest-validate EXIT:0 → report EXIT:0

见 README.md、CHANGELOG.md、RELEASE_CHECKLIST.md。

## 5. 关键文件

app.py / main.py / data/fetcher.py / data/universe.py / strategies/selection.py / validation/selection_validator.py / validation/backtest_validator.py / backtest/engine.py / reports/generator.py / start_ui.command / scripts/install_fallback.command / scripts/screenshot_home.py / requirements-ui.txt / README.md / CHANGELOG.md / RELEASE_CHECKLIST.md / docs/USER_GUIDE.md / docs/TROUBLESHOOTING.md / docs/UI_ACCEPTANCE_RESULT.md / docs/MANUAL_UI_CHECKLIST.md