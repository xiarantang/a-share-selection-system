# P9.5 发布版打标准备设计文档

> 创建时间：2026-05-19
> 阶段：P9.5-0（仅设计，不打 tag）
> 基线：v0.5 + P8 发布候选 + P9.1-P9.4 完成

---

## 1. P9.5 目标

准备一个长期可引用的发布版本。tag 之前必须以验收结果为准，不抢先打 tag，不把 tag 当成功证明。

具体目标：

1. 更新发布清单（RELEASE_CHECKLIST.md）到当前 12 项一键验收口径。
2. 更新变更日志（CHANGELOG.md）记录 P8/P9 全部增强。
3. 输出 tag 前最终验收记录和建议命令，由人工确认后执行。

---

## 2. 当前基线

| 项目 | 值 |
|------|-----|
| 最新 commit | P9.5-0 前置基线 `4b944a9`（P9.4-4.2），当前以最新 commit 为准 |
| 现有 tag | `v0.5`（P7.10 发布候选） |
| 发布前一键验收 | `confirm_release_ready.py` 12/12 通过 |
| 文档口径一致性 | `confirm_docs_consistency.py` 19/19 通过 |
| run_metadata 验收 | `confirm_run_metadata.py` 20/20 通过 |
| 排障体验验收 | `confirm_troubleshooting.py` 13/13 通过 |

### P9.1-P9.4 完成总结

| 阶段 | 内容 | 关键产出 |
|------|------|----------|
| P9.0 | 来时路复盘与路线图 | PROJECT_HISTORY.md + P9_ROADMAP.md |
| P9.1 | 公开文档一致性治理 | README/CHANGELOG/指南/状态文件口径一致 |
| P9.2 | 验收体系增强 | confirm_docs_consistency.py + 接入一键验收 |
| P9.3 | 复盘记录增强 | run_metadata（JSON + 报告 + UI + 独立验收） |
| P9.4 | 小白排障增强 | 排障文档口径 + UI 提示 + 启动脚本 + 排障验收 |

---

## 3. 版本建议

### 选项 A：`v0.5-p8`

- 优点：强调 v0.5 + P8/P9 稳定增强完成态，保持 v0.5 主版本
- 缺点：名称更偏阶段标记而非版本号，不如 semver 格式清晰

### 选项 B：`v0.6-rc1`（推荐）

- 优点：
  - semver 标准格式，清晰表示这是一个新的次版本候选
  - `-rc1` 后缀明确表达"发布候选，待人工最终确认"
  - 与现有 `v0.5` tag 形成清晰的版本递进
  - 后续如需修正可以出 `v0.6-rc2` 或直接 `v0.6`
- 缺点：需要确认 CHANGELOG.md 中版本号同步

### 版本建议结论

推荐 `v0.6-rc1`。但最终是否打 tag、何时打、用什么版本号，仍需人工确认。本文档不抢先 tag。

---

## 4. 后续拆分

| 阶段 | 内容 | 改动范围 |
|------|------|----------|
| P9.5-1 | 更新 RELEASE_CHECKLIST.md | RELEASE_CHECKLIST.md、PROJECT_STATE.md | ✅ 已完成 |
| P9.5-2 | 更新 CHANGELOG.md | CHANGELOG.md、PROJECT_STATE.md | ✅ 已完成 |
| P9.5-3 | tag 前最终验收记录 | PROJECT_STATE.md（输出建议命令，不打 tag） |

### 4.1 P9.5-1 更新 RELEASE_CHECKLIST.md

允许修改：RELEASE_CHECKLIST.md、PROJECT_STATE.md
禁止修改：app.py、main.py、scripts/、strategies/、data/、reports/、validation/

主要内容：
- 修正 fallback 为可选口径
- 补充 12 项一键验收（含 run_metadata 复盘记录验收 + 排障体验验收）
- 补充 tag 前手动确认步骤
- 不改变发布流程的实质，只更新口径

### 4.2 P9.5-2 更新 CHANGELOG.md

允许修改：CHANGELOG.md、PROJECT_STATE.md
禁止修改：app.py、main.py、scripts/、strategies/、data/、reports/、validation/

主要内容：
- 记录 P8 增强条目（数据层、解释、策略管理、UI 稳定性、发布候选）
- 记录 P9 增强条目（文档治理、验收体系、复盘记录、排障增强）
- 保持旧版本历史不动
- 不直写投资建议类禁词

### 4.3 P9.5-3 tag 前最终验收记录

允许修改：PROJECT_STATE.md
禁止修改：所有其他文件

主要内容：
- 确认 confirm_release_ready 12/12 通过
- 确认 confirm_docs_consistency 19/19 通过
- 确认 confirm_run_metadata 20/20 通过
- 确认 confirm_troubleshooting 13/13 通过
- 输出建议 tag 命令（由人工确认后执行）
- 不实际打 tag

---

## 5. 验收命令清单

每一步都必须通过的验收：

```bash
# 发布前一键验收（12 项）
python3 scripts/confirm_release_ready.py

# 文档口径一致性（19 项）
python3 scripts/confirm_docs_consistency.py

# run_metadata 复盘记录验收（20 项）
python3 scripts/confirm_run_metadata.py

# 排障体验验收（13 项）
python3 scripts/confirm_troubleshooting.py

# 仓库状态检查
git status          # 应为 clean
git log --oneline -5  # 确认最新 commit
git tag -l          # 确认 tag 状态
```

---

## 6. 禁止事项

| 禁止 | 原因 |
|------|------|
| 不抢先打 git tag | tag 是不可变标记，必须人工最终确认 |
| 不把 tag 当成功证明 | tag 只是版本锚点，不代表无缺陷 |
| 不改评分 / 排序 | 6 因子评分体系经多轮验收，当前稳定 |
| 不改数据链路优先级 | 三级降级已验收 |
| 不把可选 fallback 写成必装 | 三处文档已统一为可选 |
| 不输出投资建议类禁词 | 禁词红线 |
| 不新增复杂系统 | 保持本地文件 + Streamlit 轻量架构 |

---

## 7. 免责声明

本系统仅供研究学习，不构成投资建议。发布版打标准备不改变选股结果，只确保发布前验收完整。
