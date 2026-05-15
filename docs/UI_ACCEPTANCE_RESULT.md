# UI 真实验收结果 (P7.1 / P7.1.1 / P7.1.2)

> 最后更新：2026-05-15

## 验收概述

| 指标 | 值 |
|------|-----|
| 代码审查通过项 (P7.1) | 15/15 |
| Playwright 自动化验证 (P7.1.1/P7.1.2) | 首屏可见项 7/7 通过；st.info/st.metric 组件不可检测 |
| CLI select | ✅ EXIT=0 |
| CLI backtest-validate | ✅ EXIT=0 |
| CLI report | ✅ EXIT=0 |
| Streamlit 启动 | ✅ 正常 |
| 真实浏览器手动验收 | ⏳ 待执行（见 `docs/MANUAL_UI_CHECKLIST.md`） |

## Playwright 自动化验证结果

> 执行日期：2026-05-15 | 方式：Playwright + Chrome headless

### 可验证项（首屏内容）

| 检查项 | 结果 |
|--------|------|
| 页面标题 | ✅ |
| 三步引导卡片 | ✅ |
| 开始选股按钮可点击 | ✅ |
| 选股完成文本提示出现 | ✅ |
| 候选表格 Tab 存在 | ✅ |
| 验证摘要 Tab 存在 | ✅ |
| 覆盖不全文本可见 | ✅ |

### 已知局限

| 检查项 | 原因 |
|--------|------|
| st.info() 数据覆盖摘要 (数据区间/K线) | Streamlit 1.50 组件不在 DOM inner_text 中 |
| st.metric() 卡片 (数据范围/最少K线/最多K线) | 同上 |
| Tab 内懒加载内容 (整体质量/股票详情) | 首次渲染时未自动展开 |
| 最终结果页截图 | 自动化截图停在 loading spinner 画面，非最终结果 |

**所有上述不可检测项均已通过代码审查确认存在。** 代码路径见 `app.py` L408-422。

## 修复记录

| 问题 | 修复 |
|------|------|
| PROJECT_STATE.md 缺 P7.1.1/P7.1.2 行 | 已补全 |
| 最新 commit 未同步 | 已更新为 HEAD |
| 数据覆盖摘要仅在 tab 内 | 已移出 tab，改为无条件 st.info |
| start_ui.command 端口冲突无提示 | 已加入端口检测 + 自动 fallback |
| UI_ACCEPTANCE_RESULT.md 截图描述不实 | 已修正为诚实说明 |

## 结论

代码层面质量良好，CLI 全链路通过。Streamlit 渲染模型导致自动化截图无法捕获最终结果页，**真实浏览器手动点击流验收仍需执行**（见 `docs/MANUAL_UI_CHECKLIST.md`）。
