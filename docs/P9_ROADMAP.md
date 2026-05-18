# P9 路线图：发布版稳定性与复盘可信度增强

> 规划日期：2026-05-18
> 前置基线：v0.5 + P8 发布候选完成态
> 最新基线 commit：`84bec90`
> 发布前一键验收：`python3 scripts/confirm_release_ready.py`，当前 11/11 通过（含文档口径一致性检查 + run_metadata 复盘记录验收）

## 1. 总目标

P9 的目标不是把系统做复杂，而是把已经完成的 v0.5 + P8 发布候选，打磨成更长期可用、更容易复盘、更适合小白持续使用的版本。

P9 继续坚持产品目标：

> 小白双击启动 Streamlit UI，通过按钮、表格、解释和风险提示完成选股查看。

P9 继续坚持工程目标：

> 每次改动都能被验收、能追溯、能回滚，不靠口头说“应该没问题”。

## 2. 当前基线

当前已完成：

- P1-P5：命令行、数据层、选股 MVP、批量股票池、模型可信度与验证复盘。
- P6-P7：Streamlit UI、小白启动脚本、真实浏览器验收、v0.5 tag。
- P8：baostock 数据增强、规则解释、UI 体验增强、策略管理入口、AI 边界评审、UI 稳定性、发布候选收口。

当前主路径：

> 双击 `start_ui.command` → 选参数 → 开始选股 → 看结果

当前发布前验收入口：

```bash
python3 scripts/confirm_release_ready.py
```

## 3. P9 总原则

必须坚持：

- 不碰实盘交易。
- 不引入 AI/qlib 到评分排序链路。
- 不做数据库、登录系统、复杂前后端分离。
- 不重写评分和排序。
- 不随意改数据链路。
- 不输出投资建议措辞。
- 不牺牲小白双击启动路径。
- 每个阶段都要更新 `PROJECT_STATE.md` 并保留验收结果。

## 4. 阶段总览

| 阶段 | 主题 | 优先级 | 核心产出 |
|------|------|--------|----------|
| P9.0 | 来时路复盘与路线图 | 高 | `PROJECT_HISTORY.md` + `P9_ROADMAP.md` |
| P9.1 | 公开文档一致性治理 | 高 | README/CHANGELOG/指南/状态文件口径一致 |
| P9.2 | 验收体系增强 | 高 | 文档一致性、边界、安全措辞等自动检查 |
| P9.3 | 复盘记录增强 | 高 | 每次选股结果更容易追溯参数、数据源、验证摘要 |
| P9.4 | 小白排障增强 | 中 | 页面和文档能解释常见故障的下一步 |
| P9.5 | 发布版打标准备 | 中 | tag 前最终清单、版本说明、验收留档 |

## 5. P9.0 来时路复盘与路线图

### 目标

从 P1 到 P8 做一次完整复盘，明确项目为什么走到现在、当前边界是什么、P9 应该如何推进。

### 允许修改

- 新增 `docs/PROJECT_HISTORY.md`
- 新增 `docs/P9_ROADMAP.md`
- 轻微更新 `PROJECT_STATE.md`

### 禁止修改

- 不修改 `app.py`
- 不修改 `main.py`
- 不修改 `data/`
- 不修改 `strategies/`
- 不修改 `reports/`
- 不修改 `validation/`
- 不修改 `requirements*.txt`
- 不修改启动脚本

### 验收

```bash
python3 scripts/confirm_release_ready.py
rg -n "P1|P2|P3|P4|P5|P6|P7|P8|P9|长期可用|可复盘|发布候选" docs/PROJECT_HISTORY.md docs/P9_ROADMAP.md PROJECT_STATE.md
git diff --name-only
```

## 6. P9.1 公开文档一致性治理

### 目标

把公开文档统一到当前真实状态，避免小白看到旧流程、旧数据状态或旧启动要求。

### 重点检查

- README.md
- CHANGELOG.md
- docs/USER_GUIDE.md
- docs/TROUBLESHOOTING.md
- docs/MANUAL_UI_CHECKLIST.md
- docs/UI_ACCEPTANCE.md
- docs/P8_7_RELEASE_REVIEW.md
- PROJECT_STATE.md

### 重点问题

- v0.5 历史描述可以保留，但必须标明是历史基线，不应被误读为当前 P8 完成态。
- 当前主路径必须统一为：双击启动 → 选参数 → 开始选股 → 看结果。
- skill_fallback 必须保持“可选第三级兜底”口径。
- baostock 必须保持“轻量依赖已包含，约 570 条日 K”口径。

### 禁止做什么

- 不改产品代码。
- 不改验收脚本逻辑。
- 不为了文档统一改动真实功能。

### 验收

```bash
python3 scripts/confirm_release_ready.py
rg -n "四步引导|四步完成|三步引导|两步核心|必须安装备用|先安装备用" README.md CHANGELOG.md docs/USER_GUIDE.md docs/TROUBLESHOOTING.md docs/MANUAL_UI_CHECKLIST.md docs/UI_ACCEPTANCE.md PROJECT_STATE.md || true
git diff --name-only
```

## 7. P9.2 验收体系增强

### 目标

让“有没有破坏主路径、文档有没有打架、边界有没有越线”尽量自动检查。

### 建议产出

- 新增一个轻量文档一致性检查脚本，例如 `scripts/confirm_docs_consistency.py`。
- 将关键检查接入 `scripts/confirm_release_ready.py`，或先作为独立脚本运行。
- 检查当前主路径文案、fallback 可选口径、baostock 口径、投资建议措辞边界。

### 允许修改

- `scripts/confirm_docs_consistency.py`
- `scripts/confirm_release_ready.py`
- 相关文档
- `PROJECT_STATE.md`

### 禁止修改

- 不修改评分、排序、数据链路。
- 不修改选股结果结构，除非只是读取检查。
- 不引入新依赖。

### 验收

```bash
python3 scripts/confirm_docs_consistency.py
python3 scripts/confirm_release_ready.py
```

## 8. P9.3 复盘记录增强

> **P9.3-0 设计已完成**，详见 `docs/P9_3_REPLAY_TRACE_DESIGN.md`。

### 目标

让每次选股更容易复盘：这次是用什么参数、什么数据源、什么策略、什么时候生成、验证结果如何。

### 建议方向

优先增强已有 JSON 和 Markdown 报告，不做数据库。

可记录：

- 运行时间。
- 股票池、扫描数量、Top 数量、起始日期。
- 策略 ID 和策略名称。
- 数据源分布。
- 覆盖不足比例。
- 置信度分布。
- 报告文件路径。
- 验证摘要。

### 允许修改

- `main.py`
- `strategies/selection.py`
- `reports/generator.py`
- `validation/`
- `app.py` 只做展示层小改
- 相关验收脚本和文档

### 禁止修改

- 不改评分公式。
- 不改排序逻辑。
- 不改数据源优先级。
- 不新增数据库。
- 不让复盘记录影响选股结果。

### 验收

```bash
python3 -m py_compile app.py main.py
.venv/bin/python main.py select --universe static --limit 10 --top 5
.venv/bin/python main.py report
python3 scripts/confirm_release_ready.py
```

## 9. P9.4 小白排障增强

### 目标

减少小白遇到问题时的迷路感。系统应尽量告诉用户：发生了什么、是否严重、下一步怎么做。

### 重点场景

- Python 未安装或版本不对。
- 依赖安装失败。
- 端口被占用。
- 网络波动导致数据源降级。
- baostock 登录失败。
- 选股等待时间较长。
- 没有生成报告或报告过期。

### 允许修改

- `app.py`
- `start_ui.command`
- `scripts/install_fallback.command`
- `docs/TROUBLESHOOTING.md`
- `docs/USER_GUIDE.md`
- 相关验收脚本

### 禁止修改

- 不改评分排序。
- 不改数据链路优先级。
- 不把可选 fallback 重新说成启动前提。
- 不让排障提示制造恐慌。

### 验收

```bash
python3 -m py_compile app.py
bash -n start_ui.command
bash -n scripts/install_fallback.command
python3 scripts/confirm_release_ready.py
```

## 10. P9.5 发布版打标准备

### 目标

在 P9.1-P9.4 完成后，准备一个可长期引用的发布版本。

### 建议产出

- 发布版 checklist。
- CHANGELOG 更新。
- 版本号建议。
- tag 前最终验收记录。

### 可选 tag

二选一，届时再决定：

- `v0.5-p8`：强调这是 v0.5 基线上的 P8 增强完成版。
- `v0.6-rc1`：强调进入下一个候选版本。

### 禁止做什么

- 不在 P9.1-P9.4 未完成前抢先打 tag。
- 不把 tag 当成功证明，必须以验收结果为准。

### 验收

```bash
python3 scripts/confirm_release_ready.py
git status --short
git log --oneline -8 --decorate
```

## 11. 推荐执行顺序

1. P9.0：先建全项目地图。
2. P9.1：先清文档口径，避免用户看到冲突信息。
3. P9.2：把文档和边界检查自动化。
4. P9.3：增强复盘记录，让结果更可追溯。
5. P9.4：改善排障体验。
6. P9.5：最后再考虑发布打标。

## 12. P9 成功标准

P9 完成时，应满足：

- 小白主路径仍然不变。
- 发布前一键验收稳定通过。
- 公开文档不互相打架。
- 每次选股结果能追溯参数、数据源和验证摘要。
- 常见问题有清晰排障路径。
- 项目边界仍然清楚，没有把系统推向复杂化。
