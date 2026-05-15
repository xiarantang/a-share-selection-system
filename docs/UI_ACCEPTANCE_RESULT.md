# UI 真实验收结果 (P7.1)

> 验收日期：2026-05-15
> 验收方式：代码审查对照 `docs/UI_ACCEPTANCE.md` + Streamlit headless 启动验证 + CLI 全链路验证

## 验收概述

| 指标 | 值 |
|------|-----|
| 代码审查通过项 | 15/15 |
| Streamlit 启动 | ✅ 正常 (headless mode, port 8501) |
| CLI select | ✅ EXIT=0 |
| CLI backtest-validate | ✅ EXIT=0 |
| CLI report | ✅ EXIT=0 |
| 发现的问题 | 0 |
| 修复内容 | 无 |
| 未解决问题 | 0 |

## 逐项验收详情

### 1. 启动系统 ✅

- `start_ui.command` 语法检查通过 (`bash -n`)
- Streamlit headless 模式启动正常，监听 `http://localhost:8501`

### 2. 首页引导 ✅

代码中存在 `render_step_guide()` 函数，包含三列卡片：
- ① 选参数
- ② 开始选股
- ③ 看结果

左侧栏有 `**① 选择股票池**`、`**② 一键运行**`、`**③ 查看结果**` 三步编号。

### 3. 选股功能 ✅

- 股票池默认 `static`，下拉选项含三个选项
- `st.button("🚀 开始选股")` 按钮存在
- 加载状态：`st.spinner("⏳ 正在选股中")` 
- 成功提示区分数据源状态（akshare 可用/不可用）
- 全部失败时给出人性化错误提示

### 4. 候选表格 ✅

- `build_candidates_df()` 包含「数据区间」列
- 「覆盖」列显示 ✓ 或 ⚠️不全
- 决策列有 `color_decision()` 着色函数（strong_watch 绿/watch 浅绿/avoid 红）
- 表格上方有 `build_coverage_summary()` 五指标卡片

### 5. 逐只详情 ✅

- expander 显示评分/决策/风险/置信度
- 显示数据区间（actual_start ~ actual_end）
- 覆盖不全时标题追加 "⚠️覆盖不全"，展开后有白话警告
- 六因子得分和因子数值完整展示

### 6. 验证摘要 ✅

- `render_validation()` 函数包含 quality_label 中文解释
- 三档质量说明：数据充足/结果仅供参考/不建议参考
- 分布统计（置信度/决策/风险）完整
- 行业分布柱状图

### 7. 历史复盘 ✅

- 按钮灰色禁用（无选股结果时）
- `st.info("💡 尚未运行历史复盘")` 操作指引
- `st.caption("复盘需要重新拉取数据，较慢")` 说明

### 8. 报告 ✅

- `generate_report()` 复用 `reports.generator`
- `st.info("📁 报告已保存至...")` 路径提示

### 9. 数据覆盖可视化 ✅

全链路覆盖：
- 候选表「数据区间」列 + 覆盖摘要五指标卡片（数据范围/最少/最多/平均K线/覆盖不全数）
- 逐只详情中的覆盖警告
- 验证摘要中的覆盖不足率

**不需要翻日志。**

## 结论

P7.0 产品化打磨第一版的 UI 代码质量良好，所有验收项均通过代码审查。无发现任何文档与实现不一致或需修复的问题。Streamlit 应用可正常启动，CLI 全链路通过。

## 附录：CLI 验证输出

```
.venv/bin/python main.py select --universe static --limit 10 --top 5: EXIT=0
.venv/bin/python main.py backtest-validate --top 5: EXIT=0  
.venv/bin/python main.py report: EXIT=0
.venv/bin/streamlit run app.py --server.headless true: 正常启动 (200 OK)
```
