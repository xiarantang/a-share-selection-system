# P9.3 复盘记录增强设计文档

> 创建时间：2026-05-18
> 阶段：P9.3-0（仅设计，不实现）→ P9.3-1 JSON 字段已实现
> 基线：v0.5 + P8 发布候选 + P9.1-P9.2 文档治理

---

## 1. 当前问题

selection_latest.json 已包含丰富的选股结果、策略解释和验证摘要：

```
顶层 keys: generated_at / strategy_id / strategy / universe / stats / top / all / validation
validation keys: total_count / success_count / coverage_warning_ratio / confidence_dist / decision_dist / risk_level_dist / sector_dist / data_source_dist / avg_score / top_score / overall_quality / ...
top[n] keys: symbol / name / sector / score / decision / risk_level / confidence / rows / actual_start / actual_end / data_source / coverage_warning / explain / factor_scores / factor_values / reasons / risks / rank
```

但以下信息散落在不同字段或缺失，未形成统一的复盘记录口径：

| 信息 | 当前位置 | 问题 |
|------|----------|------|
| 运行入口（CLI / UI） | 无 | 不知道这次结果是命令行还是 UI 跑的 |
| 命令行参数 | `universe` 部分有 | `limit` / `top` / `start` 日期未在顶层直接体现 |
| 策略信息 | `strategy_id` + `strategy` | 已有，但与复盘记录未归组 |
| 数据源分布 | `stats.source_dist` + `validation.data_source_dist` | 两处重复 |
| 验证摘要 | `validation` | 已有，但与运行参数未归组 |
| Markdown 报告路径 | 无 | 不知道报告保存在哪里 |
| Top 排序结果摘要 | 需要遍历 `top` 数组 | 缺少一个一眼看到的摘要 |

**核心问题**：用户（或维护者）打开 selection_latest.json 时，无法一眼看清"这次跑的什么参数、用的什么策略、数据源如何、结果质量如何、报告在哪"。

---

## 2. P9.3 总目标

**不改评分、不改排序、不改数据链路**，只增强可追溯记录。

具体目标：

1. JSON 顶层新增 `run_metadata` 字段，将运行参数、策略信息、数据源分布、验证摘要、报告路径等统一归组。
2. Markdown 报告新增"本次运行复盘信息"小节，展示 run_metadata 的关键内容。
3. Streamlit UI 可后续在数据概览或报告 Tab 轻量展示，不在本阶段实现。

---

## 3. 建议新增字段：run_metadata

JSON 顶层新增 `run_metadata` 字段，结构设计如下：

```json
{
  "run_metadata": {
    "generated_at": "2026-05-18T23:47:33.402066",
    "entrypoint": "cli",
    "command": "main.py select --universe static --limit 10 --top 5 --start 2024-01-01 --strategy default",
    "params": {
      "universe": "static",
      "limit": 10,
      "top": 5,
      "start": "2024-01-01",
      "strategy_id": "default"
    },
    "strategy": {
      "id": "default",
      "name": "默认规则策略"
    },
    "data_summary": {
      "source_dist": {"baostock": 10},
      "avg_rows": 570,
      "coverage_warning_ratio": 0.0
    },
    "result_summary": {
      "total": 10,
      "success": 10,
      "top_score": 69,
      "avg_score": 55.3,
      "confidence_dist": {"high": 8, "medium": 2, "low": 0},
      "decision_dist": {"strong_watch": 2, "watch": 5, "neutral": 2, "avoid": 1},
      "risk_level_dist": {"low": 7, "medium": 3, "high": 0},
      "overall_quality": "good"
    },
    "report_path": "reports/output/report_20260518.md",
    "selection_path": "reports/output/selection_latest.json"
  }
}
```

### 3.1 字段来源与约束

| 字段 | 来源 | 说明 |
|------|------|------|
| `generated_at` | 已有顶层字段 | 直接复用 |
| `entrypoint` | 新增 | `"cli"` 或 `"ui"`，在调用入口处传入 |
| `command` | 新增 | CLI 时为完整命令行；UI 时为 `"streamlit run app.py"` |
| `params` | 部分已有 | `universe` 来自已有字段；`limit`/`top`/`start`/`strategy_id` 从参数传入 |
| `strategy` | 已有顶层字段 | 提取 id 和 name |
| `data_summary` | 已有 validation | 从 `validation.data_source_dist` 和遍历 `top` 计算 |
| `result_summary` | 已有 validation | 从 `validation` 提取关键字段 |
| `report_path` | 新增 | 报告生成后回填路径 |
| `selection_path` | 新增 | JSON 保存后回填路径 |

**关键约束**：所有字段均来自已有结果或已有验证摘要，不重新跑评分、不影响排序、不改数据链路。

### 3.2 entrypoint 取值

| 场景 | entrypoint 值 | command 值 |
|------|---------------|------------|
| CLI `main.py select` | `"cli"` | 完整命令行字符串 |
| Streamlit UI | `"ui"` | `"streamlit run app.py"` |
| 其他脚本调用 | `"script"` | 脚本路径 |

---

## 4. Markdown 报告新增小节

在 Markdown 报告末尾（免责声明之前）新增：

```markdown
## 本次运行复盘信息

| 项目 | 值 |
|------|-----|
| 生成时间 | 2026-05-18 23:47:33 |
| 运行方式 | 命令行 |
| 命令 | main.py select --universe static --limit 10 --top 5 |
| 策略 | 默认规则策略 (default) |
| 数据源 | baostock: 10 只 |
| 平均数据条数 | 570 条 |
| 覆盖不足率 | 0% |
| 整体质量 | good |
| Top 评分 | 69 |
| 平均评分 | 55.3 |
```

**设计原则**：
- 不重复报告中已有的详细内容，只提供一个一眼可读的运行快照。
- 数据全部来自 run_metadata，不做额外计算。
- 老 JSON 没有 run_metadata 时优雅降级，不显示此小节。

---

## 5. Streamlit UI 展示（后续阶段，不在本阶段实现）

建议在数据概览区域下方用 `st.caption` 或折叠区轻量展示 run_metadata 关键信息：

- 运行方式 + 生成时间
- 数据源分布 + 覆盖率
- 整体质量 + 平均评分

不新增 Tab、不新增页面、不改变 Top3 速览和候选表格。

---

## 6. P9.3 后续拆分

| 阶段 | 内容 | 改动范围 |
|------|------|----------|
| P9.3-1 | JSON 复盘记录字段实现 | strategies/selection.py（新增 `_build_run_metadata()`） | ✅ 已完成 |
| P9.3-2 | Markdown 报告接入复盘记录 | reports/generator.py |
| P9.3-3 | UI 轻量展示与小白说明 | app.py（数据概览区下方折叠） |
| P9.3-4 | 验收脚本与文档收口 | scripts/ + docs/ |

---

## 7. 验收标准

每一步都必须：

1. `python3 scripts/confirm_release_ready.py` 全部通过。
2. `python3 scripts/confirm_docs_consistency.py` 全部通过。
3. 不改变 Top 排序（同参数同数据源，结果与 P9.3 之前一致）。
4. 不改变评分、排序、数据链路、报告逻辑。

---

## 8. 明确禁止

- **不碰实盘交易**：系统仅供研究学习，不连接券商账户，不执行交易。
- **不引入 AI/qlib 到评分排序链路**：评分、排序、风控等级均为规则计算。
- **不输出投资建议措辞**：复盘记录只记录运行参数和数据摘要。
- **不做数据库/登录/复杂前后端**：保持本地文件 + Streamlit 轻量架构。
- **不重写评分/排序**：6 因子评分体系经多轮验收，当前稳定。
- **不改数据链路**：akshare → baostock → skill_fallback 三级降级已验收。
- **不改报告逻辑**：Markdown 报告只新增小节，不修改已有内容。

---

## 9. 免责声明

本系统仅供研究学习，不构成投资建议。复盘记录增强不改变选股结果，只提升可追溯性。
