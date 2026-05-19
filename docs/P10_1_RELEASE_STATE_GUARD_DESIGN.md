# P10.1 tag/main/公开文档状态一致性守门设计

> 创建时间：2026-05-19
> 阶段：P10.1-0（仅设计，不实现脚本，不改产品代码，不移动 tag）
> 基线：v0.6-rc1 已打标，main 在 tag 之后有文档提交

---

## 1. P10.1 目标

让维护者清楚区分三个概念：

1. **release tag**（v0.6-rc1）：锚定发布时刻的代码快照，指向 commit `3461390`。
2. **main 最新提交**：tag 之后可能继续前进的文档/状态收口提交，不代表发布内容变化。
3. **远端 tag**：GitHub 上 `refs/tags/v0.6-rc1` 应始终存在且指向同一 commit。

**核心结论**：tag 后的 main 文档提交是正常收口，不应移动 tag。维护者复盘时应以 tag 指向的 commit 为发布基线，以 main 最新提交为当前工作状态。

---

## 2. 当前事实

| 项目 | 值 |
|------|-----|
| release tag | `v0.6-rc1` |
| tag 指向 commit | `3461390`（P9.5-3.1: 最终验收记录 commit 号同步） |
| tag 提交内容 | 仅修改 `PROJECT_STATE.md`（1 行） |
| main 最新 commit | `51db203`（P10-0: 发布后观察与真实小白验收路线图） |
| main 与 tag 的距离 | tag 后 3 个提交（P9.5-4 / P9.5-4.1 / P10-0） |

### tag 后提交清单

| commit | 内容 | 改动文件 | 是否改产品代码 |
|--------|------|----------|----------------|
| `cecac10` | P9.5-4: v0.6-rc1 打标后状态同步 | CHANGELOG.md / PROJECT_STATE.md / README.md / docs/P9_5_RELEASE_PREP.md | 否 |
| `148701c` | P9.5-4.1: P9_5_RELEASE_PREP 口径分层收口 | PROJECT_STATE.md / docs/P9_5_RELEASE_PREP.md | 否 |
| `51db203` | P10-0: 发布后观察路线图 | PROJECT_STATE.md / README.md / docs/P10_ROADMAP.md | 否 |

所有 tag 后提交均为文档和状态记录，未修改 app.py / main.py / data/ / strategies/ / reports/ / validation/ / scripts/ / start_ui.command。

---

## 3. 守门检查建议

维护者在发布后任意时间点可运行以下检查，确认 tag/main/远端状态一致：

### 检查 1：tag 仍指向发布 commit

```bash
git tag --points-at 3461390
# 期望输出：v0.6-rc1
# 如果为空：tag 被误删或误移动，需立即排查
```

### 检查 2：HEAD 可能没有 tag（正常）

```bash
git tag --points-at HEAD
# 期望输出：空（main 在 tag 之后有文档提交）
# 如果显示 v0.6-rc1：说明 main 没有新提交，也是正常的
```

### 检查 3：远端 tag 存在且指向正确

```bash
git ls-remote --tags origin v0.6-rc1
# 期望输出：8e4d7e344acc3dea32cbd95b769df2ba37b1ec06  refs/tags/v0.6-rc1
# 如果为空：tag 未推送或被误删
```

### 检查 4：tag 指向的提交内容

```bash
git show --stat v0.6-rc1
# 期望：commit 3461390，tag 消息为 "v0.6-rc1: A股选股系统发布候选"
```

### 检查 5：tag 到 HEAD 之间无产品代码变更

```bash
git diff v0.6-rc1..HEAD --name-only
# 期望：仅出现文档/状态文件（PROJECT_STATE.md / README.md / CHANGELOG.md / docs/*）
# 如果出现以下文件，说明有误改：
#   app.py / main.py / start_ui.command / data/ / strategies/ /
#   reports/generator.py / validation/ / scripts/
```

### 通过标准

| 检查 | 通过条件 |
|------|----------|
| 检查 1 | 输出包含 `v0.6-rc1` |
| 检查 2 | 输出可为空（正常） |
| 检查 3 | 输出包含远端 tag SHA |
| 检查 4 | commit 为 `3461390`，tag 消息正确 |
| 检查 5 | 无产品代码文件 |

---

## 4. 后续拆分建议

### P10.1-1 新增独立脚本 scripts/confirm_release_state.py（已完成 ✅）

- 自动运行上述 5 项检查（实际实现为 6 项：tag 存在 / tag 指向 / HEAD 状态 / 远端 tag / tag 内容 / diff 无产品代码）
- 输出中文通过/失败结果
- 不依赖其他验收脚本，可独立运行
- 运行方式：`python3 scripts/confirm_release_state.py`
- 验收结果：6/6 通过

### P10.1-2 是否接入 confirm_release_ready.py 的取舍评估

**建议：暂不接入。** 原因：

1. `confirm_release_ready.py` 关注的是"当前代码是否可以发布"，检查语法、UI、策略、CLI 等产品能力。
2. `confirm_release_state.py` 关注的是"tag/main 状态是否一致"，检查 git 元数据。
3. tag 固定在 `3461390` 而 main 会继续前进，两者生命周期不同。
4. 将来如果进入 v0.6 正式版流程（P10.4），再评估是否合并。

### P10.1-3 文档收口

- 在 PROJECT_STATE.md 中明确记录"发布后文档提交不移动 rc1 tag"原则
- 如有需要，在 P10_ROADMAP.md 中补充 tag/main 关系说明
- 允许修改：PROJECT_STATE.md、docs/P10_ROADMAP.md
- 禁止修改：产品代码、scripts/（除 P10.1-1 外）

---

## 5. 明确不做

| 不做 | 原因 |
|------|------|
| 不移动 tag | v0.6-rc1 已锚定在 commit `3461390`，除非发现阻断性问题 |
| 不重打 tag | tag 是不可变标记，重打会改变 SHA |
| 不改产品代码 | P10 是观察期，不是功能期 |
| 不把 main 最新提交等同 release tag | main 会继续前进，tag 不会 |
| 不自动修复 | 发现不一致时由人工排查 |
| 不输出投资建议类措辞 | 禁词红线 |

---

## 6. 免责声明

本系统仅供研究学习，不构成投资建议。P10.1 为发布后状态一致性守门，不改变选股结果。
