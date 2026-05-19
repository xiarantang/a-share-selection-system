# P10.2 真实 UI 启动与截图复核设计

> 创建时间：2026-05-19
> 阶段：P10.2-0（仅设计/诊断，不改产品代码，不启动 Streamlit，不更新截图）
> 基线：v0.6-rc1 已打标，P10.1 已完成

---

## 1. P10.2 目标

确认当前真实 UI 与截图、验收脚本口径一致。不是新增功能，不是改 UI。

---

## 2. 当前诊断

### 2.1 截图脚本 scripts/screenshot_home.py

脚本创建于 P7.7，最后更新于 P8.3-4。存在以下旧关键词残留：

| 行号 | 旧关键词 | 问题 | 当前 UI 应为 |
|------|----------|------|-------------|
| 45 | `四步完成选股` | 首页已改为「选参数 → 开始选股 → 看结果」 | 首页不再使用步骤计数 |
| 68 | `strong_watch` | 结果页决策标签已中文化 | UI 展示层使用「强观察」 |
| 1 | `P7.7 验收截图脚本` | 阶段标记过时 | 可更新为 P10.2 |

其他关键词仍然有效：
- `A股智能选股系统` / `开始选股` / `可以开始选股` / `首次使用检查` / `免责声明` — 首页仍包含
- `选股完成` / `候选表格` / `数据区间` / `验证摘要` / `整体质量` / `免责声明` — 结果页仍包含
- `覆盖不全` — 仅在覆盖不足时出现，脚本中作为关键词检查可能导致间歇性失败

### 2.2 现有截图

| 文件 | 大小 | 最后更新 | 来源阶段 |
|------|------|----------|----------|
| docs/screenshots/home.png | ~183KB | 2026-05-18 | P8.6-2 UI 冒烟验收 |
| docs/screenshots/result.png | ~147KB | 2026-05-18 | P8.6-2 UI 冒烟验收 |

截图是在 P8.6-2 时从真实 Streamlit 页面截取的。P8.6 之后 main 没有 app.py 产品代码变更（已由 confirm_release_state.py 验证 tag..HEAD diff 无产品代码）。因此截图内容应仍代表当前真实 UI，但需要在 P10.2-2 中实际确认。

### 2.3 confirm_p83_ui.py vs screenshot_home.py

| 维度 | confirm_p83_ui.py | screenshot_home.py |
|------|-------------------|-------------------|
| 检查方式 | 静态文本 + JSON 运行时 | 真实浏览器截图 + 关键词 |
| 覆盖范围 | 44 项静态/运行时检查 | 首页 + 结果页截图 |
| 关键词口径 | 已在 P8.3-4 同步为当前 UI | 仍有旧关键词残留 |
| 角色 | 发布验收（CI 友好） | 真实视觉确认 |

---

## 3. P10.2 拆分

### P10.2-1 修正截图脚本关键词/验收口径

**目标**：将 screenshot_home.py 的关键词检查对齐到当前 UI 文案。

允许修改：
- scripts/screenshot_home.py

禁止修改：
- app.py / main.py / start_ui.command / strategies/ / data/ / reports/ / validation/ / docs/screenshots/

主要改动：
1. 首页关键词：`四步完成选股` → 移除（当前 UI 不使用步骤计数）
2. 结果页关键词：`strong_watch` → 替换为当前 UI 展示层中文标签（如 `强观察` 或 `观察`）
3. 脚本头注释：`P7.7` → 更新为 P10.2
4. `覆盖不全` 关键词：改为仅在覆盖不足时才检查的可选项，或替换为始终出现的确定性关键词

### P10.2-2 启动 Streamlit 做真实截图复核

**目标**：用修正后的脚本从真实 Streamlit 页面截图，确认截图内容与当前 UI 一致。

允许修改：
- docs/screenshots/home.png（如需更新）
- docs/screenshots/result.png（如需更新）
- PROJECT_STATE.md

禁止修改：
- app.py / main.py / start_ui.command / scripts/ / strategies/ / data/ / reports/ / validation/

前置条件：
- P10.2-1 脚本修正完成
- Streamlit 可本地启动（双击 start_ui.command 或 streamlit run app.py）
- Playwright + Chrome 可用

如截图内容与 P8.6-2 无实质差异（因为 app.py 未改），可以确认截图仍有效，不强制重新截取。但需要脚本关键词检查全部通过。

### P10.2-3 文档收口

**目标**：记录真实 UI 复核结果和是否更新截图。

允许修改：
- PROJECT_STATE.md
- docs/P10_ROADMAP.md

禁止修改：
- 产品代码 / scripts/ / docs/screenshots/（除 P10.2-2 已更新外）

---

## 4. 明确不做

| 不做 | 原因 |
|------|------|
| 不改 UI 文案 | P10 是观察期，不是 UI 改版期 |
| 不改产品逻辑 | 评分/排序/数据链路/报告逻辑不变 |
| 不改评分/排序 | 6 因子评分体系经多轮验收，当前稳定 |
| 不移动 release tag | v0.6-rc1 锚定在 commit `3461390` |
| 不把截图脚本当投资决策链路 | 截图仅做视觉确认，不改变选股结果 |
| 不输出投资建议类措辞 | 禁词红线 |

---

## 5. 验收命令

每一步都必须通过的验收：

```bash
# 发布前一键验收（12 项）
python3 scripts/confirm_release_ready.py

# 文档口径一致性（19 项）
python3 scripts/confirm_docs_consistency.py

# release tag/main 状态（6 项）
python3 scripts/confirm_release_state.py

# 截图脚本关键词（P10.2-1 之后）
python3 scripts/screenshot_home.py  # 需 Streamlit 运行中

# 仓库状态检查
git tag --points-at 3461390  # 应显示 v0.6-rc1
```

---

## 6. 免责声明

本系统仅供研究学习，不构成投资建议。P10.2 为发布后真实 UI 复核，不改变选股结果。
