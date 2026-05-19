# P10 发布后观察与真实小白验收路线图

> 创建时间：2026-05-19
> 阶段：P10-0（仅规划，不改产品代码，不打 tag）
> 基线：v0.6-rc1 已打标，发布前一键验收 12/12 通过

---

## 1. P10 总目标

P10 不是新增功能冲刺。目标是：

1. **观察**：v0.6-rc1 发布后，观察双击启动主路径、数据稳定性、小白反馈。
2. **真实小白验收**：让非技术用户试用，记录问题和体验。
3. **小修**：根据观察结果做体验/文档/验收层面的小修，不动评分排序数据链路。
4. **正式版决策**：基于观察结果决定是否从 v0.6-rc1 升为 v0.6，仍不自动打 tag。

---

## 2. 当前基线

| 项目 | 值 |
|------|-----|
| main 最新 commit | `148701c`（P9.5-4.1） |
| tag | `v0.6-rc1`，指向 commit `3461390` |
| main 与 tag 关系 | main 在 tag 之后有 P9.5-4 / P9.5-4.1 两个文档提交，均未改产品代码 |
| 发布前一键验收 | `confirm_release_ready.py` 12/12 通过 |
| 文档口径一致性 | `confirm_docs_consistency.py` 19/19 通过 |
| run_metadata 验收 | `confirm_run_metadata.py` 20/20 通过 |
| 排障体验验收 | `confirm_troubleshooting.py` 13/13 通过 |

---

## 3. P10 原则

| 原则 | 说明 |
|------|------|
| 保护双击启动主路径 | 双击 start_ui.command → 选参数 → 开始选股 → 看结果，这是核心体验 |
| 先观察再修复 | 发布后先跑一轮真实使用，不要预判问题 |
| 修复只改体验/文档/验收 | 允许改 app.py 展示层文案、docs/ 文档、scripts/ 验收脚本；不改评分/排序/数据链路/报告逻辑 |
| tag 不随便移动 | v0.6-rc1 已锚定在 commit `3461390`，除非发现阻断性问题才考虑 v0.6-rc2 |
| 小白优先 | 每个决策从"小白双击后看到什么"出发 |
| 不输出投资建议类措辞 | 禁词红线不变 |
| 保留免责声明 | 仅供研究学习，不构成投资建议 |

---

## 4. 阶段拆分

### P10.1 tag/main/公开文档状态一致性守门（P10.1-0/1/2 已完成）

**目标**：明确 tag 指向与 main 后续文档提交的关系，确保复盘时不会误读。

**设计文档**：[docs/P10_1_RELEASE_STATE_GUARD_DESIGN.md](P10_1_RELEASE_STATE_GUARD_DESIGN.md)

允许修改：
- docs/（新增说明文档或更新现有文档）
- scripts/（如需新增轻量检查脚本）
- PROJECT_STATE.md

禁止修改：
- app.py / main.py / start_ui.command / strategies/ / data/ / reports/ / validation/ / 评分/排序/数据链路

验收命令：
```bash
git tag --points-at 3461390          # 应显示 v0.6-rc1
python3 scripts/confirm_release_ready.py
python3 scripts/confirm_docs_consistency.py
```

### P10.2 真实 UI 启动与截图复核

**目标**：双击路径 / Streamlit 页面 / 首页结果截图确认。如 UI 无实际改动，不强制更新截图。

允许修改：
- docs/screenshots/（如截图需更新）
- docs/（验收记录文档）
- PROJECT_STATE.md

禁止修改：
- app.py / main.py / start_ui.command / strategies/ / data/ / reports/ / validation/ / 评分/排序/数据链路

验收命令：
```bash
python3 scripts/confirm_release_ready.py   # 含 P8.3 UI 验收 44 项
ls -la docs/screenshots/home.png docs/screenshots/result.png
```

### P10.3 发布后问题记录模板

**目标**：建立 `docs/POST_RELEASE_NOTES.md`，记录小白试用反馈、复现步骤、处理状态。

允许修改：
- docs/POST_RELEASE_NOTES.md（新增）
- PROJECT_STATE.md

禁止修改：
- app.py / main.py / start_ui.command / scripts/ / strategies/ / data/ / reports/ / validation/ / 评分/排序/数据链路

问题记录模板字段建议：
- 编号 / 日期 / 发现者 / 问题描述 / 复现步骤 / 影响范围 / 处理状态 / 修复阶段 / 备注

验收命令：
```bash
test -f docs/POST_RELEASE_NOTES.md && echo "文件存在"
python3 scripts/confirm_docs_consistency.py
```

### P10.4 v0.6 正式版决策记录

**目标**：基于 P10.1–P10.3 观察结果，决定是否从 rc1 升为 v0.6。不自动打 tag。

允许修改：
- PROJECT_STATE.md
- docs/（决策记录文档）
- README.md（仅版本号口径同步）
- CHANGELOG.md（仅版本标题同步，如需）

禁止修改：
- app.py / main.py / start_ui.command / scripts/ / strategies/ / data/ / reports/ / validation/ / 评分/排序/数据链路
- 不创建或移动 git tag（v0.6 仍需人工确认后手动打标）

决策条件（参考）：
- P10.1 状态一致性守门通过
- P10.2 UI 复核无阻断性问题
- P10.3 问题记录中无未处理的阻断性反馈
- 发布前一键验收仍 12/12 通过
- 如果以上条件满足，建议打 v0.6 tag；否则先修问题，考虑 v0.6-rc2

---

## 5. 明确不做

| 不做 | 原因 |
|------|------|
| 不加新策略 | 当前只有默认规则策略，P10 是观察期不是功能期 |
| 不改评分/排序 | 6 因子评分体系经多轮验收，当前稳定 |
| 不改数据链路优先级 | 三级降级已验收，baostock 稳定 570 条 |
| 不引入 AI/qlib/多 Agent | P8.5-0 已决策暂缓，P10 不重新打开 |
| 不做登录/数据库/实盘 | 核心边界不变 |
| 不自动打 tag | tag 是不可变标记，仍需人工确认 |
| 不输出投资建议类措辞 | 禁词红线 |

---

## 6. 免责声明

本系统仅供研究学习，不构成投资建议。P10 为发布后观察与验收阶段，不改变选股结果。
