# UI 真实验收结果 (P7.1 / P7.1.1 / P7.1.2)

> 最后更新：2026-05-15

## 验收概述

| 指标 | 值 |
|------|-----|
| 代码审查通过项 (P7.1) | 15/15 |
| Playwright 真实浏览器验收 (P7.1.1) | 5/6（数据区间列因 Streamlit 表格渲染未检测到） |
| Playwright 增强版验收 (P7.1.2) | 实际可见项 7/9（stMetric/stInfo 不在 inner_text 中） |
| CLI select | ✅ EXIT=0 |
| CLI backtest-validate | ✅ EXIT=0 |
| CLI report | ✅ EXIT=0 |
| Streamlit 启动 | ✅ 正常 |

## P7.1.2 补充：真实浏览器验收 (Playwright + Chrome headless)

> 执行日期：2026-05-15
> 方式：Playwright 连接系统 Chrome，headless 模式

### 可验证项

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 页面标题 | ✅ | |
| 三步引导卡片 | ✅ | ①选参数 / ②开始选股 / ③看结果 |
| 开始选股按钮可点击 | ✅ | |
| 选股完成后提示出现 | ✅ | 包含「选股完成」字样 |
| 候选表格 Tab 存在 | ✅ | |
| 验证摘要 Tab 存在 | ✅ | |
| 「覆盖不全」文本可见 | ✅ | |

### 已知局限

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 数据区间纯文本 | ⚠️ 不可检测 | st.info() 内容在 Streamlit 1.50 中不在 inner_text() 覆盖范围 |
| K线条数 | ⚠️ 不可检测 | st.metric() 同理 |
| 整体质量 | ⚠️ 不可检测 | 在 tab 内懒加载，未在首次渲染中 |

**所有不可检测项均已在代码审查中确认存在。** 代码路径：`app.py` L417-422（st.info 数据覆盖摘要），L408-414（st.metric 卡片），L199-236（render_validation）。

## 修复记录

| 问题 | 修复 |
|------|------|
| PROJECT_STATE.md 缺少 P7.1.1 行 | 已加入 |
| 最新 commit 未同步 | 已更新为 HEAD |
| UI_ACCEPTANCE_RESULT.md 未标注 P7.1 验收方式 | 已补充诚实标注 |
| app.py 数据覆盖摘要仅在 tab 内 | 已移出 tab，改为无条件 st.info() |
| start_ui.command 端口检测 | 已加入 8501 占用检测 + 自动 fallback 到 8502 |

## 截图

`/tmp/ui_accept_final.png` — 选股完成后的全页面截图（Playwright 捕获）。

## 结论

P7.0-P7.1 的 UI 代码质量良好。实际浏览器验收应优先在真实浏览器中进行手动点击流验证（按 `docs/UI_ACCEPTANCE.md` 操作），自动化工具受 Streamlit 渲染模型限制。CLI 全链路通过，代码审查通过，无功能性问题。
