# P10.4 v0.6 正式版决策记录

> 创建时间：2026-05-19
> 阶段：P10.4（决策记录，不打 tag）
> 基线：v0.6-rc1 tag 指向 commit `3461390`

---

## 1. 当前基线

| 项目 | 值 |
|------|-----|
| release tag | `v0.6-rc1`，指向 commit `3461390` |
| main 最新 commit | `f670716`（P10.4） |
| main 与 tag 关系 | main 在 tag 之后有多个文档/验收提交，均未改产品代码 |
| 发布前一键验收 | `confirm_release_ready.py` 12/12 通过 |
| 文档口径一致性 | `confirm_docs_consistency.py` 19/19 通过 |
| release 状态守门 | `confirm_release_state.py` 6/6 通过 |
| 真实 UI 截图复核 | `screenshot_home.py` 退出码 0，截图已更新 |

---

## 2. P10 观察期结论摘要

### P10.1 tag/main/公开文档状态一致性守门

- v0.6-rc1 tag 固定指向 `3461390`，发布后文档提交不移动 rc1 tag
- release 状态复盘用 `confirm_release_state.py`，产品回归用 `confirm_release_ready.py`
- 核心结论：tag 后 main 文档提交是正常收口，不应移动 tag

### P10.2 真实 UI 启动与截图复核

- 真实 Streamlit 可启动，`screenshot_home.py` 关键词已对齐真实 UI 并退出码 0
- 截图已更新：home.png ~198KB、result.png ~185KB
- 未修改产品代码

### P10.3 发布后问题记录模板

- 新增 `docs/POST_RELEASE_NOTES.md`，含问题分级、状态定义、13 字段记录表格
- 模板已就绪，等待真实小白试用反馈

---

## 3. 决策：暂不自动打 v0.6

**决策结论**：暂不将 v0.6-rc1 升为 v0.6，进入真实小白试用观察期。

**决策理由**：

1. 技术验收全部通过（12/12 + 19/19 + 6/6 + 截图复核），具备继续观察的条件
2. 尚未完成一轮真实小白试用，没有足够的用户反馈支撑正式版决策
3. 需要用 `docs/POST_RELEASE_NOTES.md` 记录真实使用中发现的问题
4. 正式版打标是不可逆操作，应由人工确认后执行

---

## 4. 升级为 v0.6 的人工条件

以下条件全部满足后，可由人工确认是否打 v0.6 tag：

| 条件 | 当前状态 |
|------|----------|
| `confirm_release_ready.py` 12/12 通过 | ✅ |
| `confirm_release_state.py` 6/6 通过 | ✅ |
| `confirm_docs_consistency.py` 19/19 通过 | ✅ |
| 真实 UI 截图复核通过 | ✅ |
| `docs/POST_RELEASE_NOTES.md` 无未处理阻断问题 | ⏳ 待观察 |
| 至少一轮真实小白试用完成 | ⏳ 待观察 |
| 人工确认可以打标 | ⏳ 待确认 |

如需打 v0.6 tag，人工执行以下命令（**仅在人工确认后执行**）：

```bash
# 确认当前状态
python3 scripts/confirm_release_ready.py
python3 scripts/confirm_release_state.py
python3 scripts/confirm_docs_consistency.py

# 确认 POST_RELEASE_NOTES 无阻断问题
cat docs/POST_RELEASE_NOTES.md

# 打标（仅人工确认后执行）
git tag -a v0.6 -m "v0.6: A股选股系统正式版"
git push origin v0.6
```

---

## 5. 回退/继续观察规则

| 情况 | 处理方式 |
|------|----------|
| 发现阻断性问题 | 记录到 `docs/POST_RELEASE_NOTES.md`，修复后考虑 v0.6-rc2 |
| 发现重要问题 | 记录并修复，不影响正式版时间线 |
| 发现一般/观察级问题 | 记录，可在后续迭代中处理 |
| 无阻断性问题 | 完成小白试用后，按第 4 节条件人工确认是否打 v0.6 |

**关键规则**：不移动、不删除 v0.6-rc1 tag。如需重新打标，打新的 rc2 tag。

---

## 6. P10 完成结论

P10（发布后观察与真实小白验收）全部子阶段已完成：

- P10.1：release tag/main 状态守门 ✅
- P10.2：真实 UI 启动与截图复核 ✅
- P10.3：发布后问题记录模板 ✅
- P10.4：v0.6 正式版决策记录 ✅

当前状态：v0.6-rc1 处于发布后观察期，技术验收全部通过，等待真实小白试用反馈。

下一步：真实小白试用观察，用 `docs/POST_RELEASE_NOTES.md` 记录问题，确认无阻断性问题后人工决定是否打 v0.6 tag。

---

## 7. 免责声明

本系统仅供研究学习，不构成投资建议。P10.4 为发布后决策记录，不改变选股结果。
