# 项目状态交接摘要

> 最后更新：2026-05-16

## 1. 项目总目标

打造长期可用、结果可信、可复盘的 A 股选股系统。

**最终形态：小白可用的可视化选股系统。** 当前 CLI 命令只是底层引擎和验收入口。
路线：P5 打磨引擎 → P6 可视化界面(Streamlit) → P7 产品化打磨 → P8 渐进增强
暂不碰实盘交易。

**禁止事项**：不碰实盘交易/复杂前后端分离/数据库/登录系统。AI/qlib 仍为远期实验方向，P8 阶段默认不进入评分、排序或买卖决策链路。

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
| P7.9 | `ec9f374` | 产品收口首页/v0.5发布准备/CHANGELOG/RELEASE_CHECKLIST |
| P7.9文档 | `7cdf0b2` | 同步P7.9交付状态 |
| P7.10 | `81d9f4c` | v0.5发布前最终审查/小修/文档矛盾修正 |
| P7.10文档 | `83393f4` | 同步P7.10交付状态 |
| P8.0 | `46230b9` | 下一阶段规划初稿：P8_ROADMAP/5阶段路线图 |
| P8.0顾问审查 | `8706fa7` | 收紧P8路线图：先数据、再解释、再UI，AI默认关闭 |
| P8.1-0 | `9648b1b` | 数据源评估报告：推荐先实验baostock，再评估efinance |
| P8.1-1 | `eff452a` | baostock最小实验通过：static前10只均达到570条日K |

- 🏷️ **v0.5 已发布**：tag `v0.5` → commit `81759aa`，annotated tag 已推送到 GitHub
- 最新已记录交付 commit: `eff452a`，当前进入 P8.1-2 baostock 小步接入
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

## 4. 当前阶段 P8.1（数据质量增强）

v0.5 已发布（tag `v0.5` → commit `81759aa`）。P8.0 规划审查已完成，P8.1 数据质量增强已启动。

P8.0 下一阶段规划已经建立，并已做顾问口径收紧：
- 新增 `docs/P8_ROADMAP.md` 规划 P8.1~P8.5 五个阶段
- P8.1 数据质量增强（高优先级）：先评估数据源，再做小步接入；目标是更长 K 线、更清楚来源、更低覆盖不足率
- P8.2 策略可解释增强（高优先级）：逐只白话解释/因子贡献说明，不改评分公式
- P8.3 UI 体验增强（中优先级）：真实阶段提示/首屏 Top3/风险颜色标记
- P8.4 策略管理（中优先级）：多策略框架/策略切换，但默认策略不变
- P8.5 AI 辅助解释（低优先级）：可选解释层/默认关闭/不参与评分、排序或交易决策

P8 执行顺序：先 P8.1 数据质量，再 P8.2 解释，再 P8.3 UI，最后才考虑 P8.4/P8.5。每阶段必须保留 v0.5 的双击启动、CLI 验收和截图证据。

详见 `docs/P8_ROADMAP.md`。

P8.1 已完成两步准备：
- 文档：`docs/P8_1_DATA_SOURCE_EVALUATION.md`
- 实验报告：`docs/P8_1_BAOSTOCK_EXPERIMENT.md`
- P8.1-0 数据源评估：首选 `baostock`，次选 `efinance`
- P8.1-1 baostock 最小实验：static 前 10 只股票 10/10 成功，均返回 570 条日 K，达成 250+ 条验收目标
- 次选实验：`efinance`
- 明确禁止：不改评分逻辑、不删除 `skill_fallback`、不修改 UI、不引入付费/API Key 作为唯一通道、不改 CLI 参数

下一步 P8.1-2：正式把 `baostock` 作为 akshare 之后、skill_fallback 之前的第二数据源小步接入 `data/fetcher.py`。只改数据层和必要依赖，不改评分、UI、CLI 参数。

## 5. 关键文件

app.py / main.py / data/fetcher.py / data/universe.py / strategies/selection.py / validation/selection_validator.py / validation/backtest_validator.py / backtest/engine.py / reports/generator.py / start_ui.command / scripts/install_fallback.command / scripts/screenshot_home.py / scripts/test_baostock.py / requirements-ui.txt / requirements-experimental.txt / README.md / CHANGELOG.md / RELEASE_CHECKLIST.md / docs/P8_ROADMAP.md / docs/P8_1_DATA_SOURCE_EVALUATION.md / docs/P8_1_BAOSTOCK_EXPERIMENT.md / docs/USER_GUIDE.md / docs/TROUBLESHOOTING.md / docs/UI_ACCEPTANCE_RESULT.md / docs/MANUAL_UI_CHECKLIST.md
