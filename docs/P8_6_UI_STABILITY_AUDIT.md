# P8.6 UI 兼容性预检与修复方案

> 创建日期：2026-05-18
> 阶段：P8.6-0（仅预检和方案，未修改任何产品代码）

## 1. 目的

对 app.py 中已知的 Streamlit/Pandas 兼容性小尾巴做系统预检，评估风险，给出 P8.6-1 最小修复方案。本轮不改动 app.py 或任何产品代码。

## 2. 当前环境版本

| 组件 | 本地安装版本 | requirements.txt 约束 | requirements-ui.txt 约束 |
|------|-------------|----------------------|-------------------------|
| Streamlit | 1.50.0（PyPI 最新） | `>=1.28.0` | `>=1.28.0` |
| Pandas | 2.3.3 | `>=2.0.0` | `>=2.0.0` |

## 3. 发现的兼容性风险

### 3.1 Streamlit `use_container_width` 已废弃

Streamlit 从 1.39 起新增 `width` 参数（`width="stretch"` 等效于 `use_container_width=True`），并标记 `use_container_width` 为废弃。官方声明将在 2025-12-31 之后移除该参数。

当前 app.py 共 4 处使用 `use_container_width=True`：

| 行号 | UI 位置 | 组件 |
|------|---------|------|
| 358 | 逐只复盘详情 — 回测结果表格 | `st.dataframe(..., use_container_width=True, hide_index=True)` |
| 492 | 侧栏 — "开始选股"按钮 | `st.button("...", type="primary", use_container_width=True)` |
| 494 | 侧栏 — "历史复盘"按钮 | `st.button("...", use_container_width=True, ...)` |
| 660 | 结果页 — 候选表格 | `st.dataframe(styled_df, use_container_width=True, hide_index=True, ...)` |

**风险**：Streamlit 未来版本移除 `use_container_width` 后，app.py 将在启动时抛出 TypeError，UI 无法使用。当前（1.50.0）仅发出 FutureWarning，不影响功能。

### 3.2 Pandas `Styler.applymap` 已废弃

Pandas 从 2.1.0 起新增 `Styler.map`，标记 `Styler.applymap` 为废弃（FutureWarning）。`Styler.map` 的签名和行为与 `applymap` 完全一致，是直接替换。

当前 app.py 共 1 处使用 `Styler.applymap`：

| 行号 | UI 位置 | 代码 |
|------|---------|------|
| 657 | 结果页 — 候选表格决策列着色 | `df.style.applymap(color_decision, subset=["决策"])` |

**风险**：Pandas 未来版本移除 `applymap` 后，此处将抛出 AttributeError。当前（2.3.3）仅发出 FutureWarning，不影响功能。

## 4. P8.6-1 最小修复方案

### 4.1 修复 `use_container_width` → `width="stretch"`

**替换规则**：

| 原代码 | 替换为 |
|--------|--------|
| `st.dataframe(df, use_container_width=True, ...)` | `st.dataframe(df, width="stretch", ...)` |
| `st.button("...", use_container_width=True)` | `st.button("...", width="stretch")` |

共 4 处替换（行 358、492、494、660），机械替换，无逻辑变化。

**最低版本影响**：`width` 参数在 Streamlit 1.39 引入。当前约束 `>=1.28.0`，需要同步提升至 `>=1.39.0`。

**风险评估**：
- Streamlit 1.39 发布于 2024 年 10 月，距今超过 1 年，生态成熟。
- `streamlit>=1.39.0` 相比 `>=1.28.0` 提高了 11 个小版本，对小白的 `pip install` 成功率几乎无影响（PyPI 始终安装最新 1.50.0）。
- 无破坏性 API 变更影响本项目其他用法（`st.columns` / `st.expander` / `st.tabs` / `st.metric` / `st.column_config` 等均向后兼容）。

**建议**：将 `requirements.txt` 和 `requirements-ui.txt` 中 `streamlit>=1.28.0` 提升为 `streamlit>=1.39.0`。

### 4.2 修复 `Styler.applymap` → `Styler.map`

**替换规则**：

| 原代码 | 替换为 |
|--------|--------|
| `df.style.applymap(color_decision, subset=["决策"])` | `df.style.map(color_decision, subset=["决策"])` |

共 1 处替换（行 657），机械替换，签名和返回值完全一致。

**最低版本影响**：`Styler.map` 在 Pandas 2.1.0 引入。当前约束 `>=2.0.0`，需要同步提升至 `>=2.1.0`。

**风险评估**：
- Pandas 2.1.0 发布于 2023 年 8 月，距今近 3 年。
- `pandas>=2.1.0` 相比 `>=2.0.0` 提高 1 个小版本，对小白的 `pip install` 成功率几乎无影响。
- 无破坏性 API 变更影响本项目其他用法（DataFrame 构造、列操作、时间处理等均向后兼容）。

**建议**：将 `requirements.txt` 和 `requirements-ui.txt` 中 `pandas>=2.0.0` 提升为 `pandas>=2.1.0`。

### 4.3 修复清单汇总

| 文件 | 改动点 | 风险 |
|------|--------|------|
| app.py 行 358 | `use_container_width=True` → `width="stretch"` | 无逻辑变化 |
| app.py 行 492 | `use_container_width=True` → `width="stretch"` | 无逻辑变化 |
| app.py 行 494 | `use_container_width=True` → `width="stretch"` | 无逻辑变化 |
| app.py 行 660 | `use_container_width=True` → `width="stretch"` | 无逻辑变化 |
| app.py 行 657 | `.applymap(` → `.map(` | 无逻辑变化 |
| requirements.txt | `streamlit>=1.28.0` → `>=1.39.0` | 低，版本已发布超 1 年 |
| requirements.txt | `pandas>=2.0.0` → `>=2.1.0` | 低，版本已发布近 3 年 |
| requirements-ui.txt | `streamlit>=1.28.0` → `>=1.39.0` | 同上 |
| requirements-ui.txt | `pandas>=2.0.0` → `>=2.1.0` | 同上 |

**不改动的范围**：评分公式、排序逻辑、数据链路、报告生成、策略管理、CLI 逻辑、验证脚本。

## 5. P8.6-1 执行建议（最小实现）

1. 先改 app.py（5 处机械替换），运行 `python3 -m py_compile app.py` 确认语法。
2. 再改 requirements.txt 和 requirements-ui.txt（4 处版本提升）。
3. 运行全链路验收：`py_compile` → `select EXIT:0` → `report EXIT:0` → UI 手动确认。
4. 不新增验收脚本，复用现有 `py_compile` + CLI 全链路即可覆盖。

## 6. 硬边界确认

- 不参与评分、排序、风控等级、买卖决策链路
- 不生成股票池
- 不改 data/fetcher.py 数据链路
- 不输出买入/卖出/目标价/收益预测等投资建议措辞
- 不要求 API Key 才能启动小白 UI
- 不引入 AI
