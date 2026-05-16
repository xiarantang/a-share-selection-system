# P8.2 策略解释方案设计

> 日期：2026-05-16 | 阶段：P8.2-0（设计文档）
> 约束：不改评分公式，不改排序，不引入 AI

---

## 1. 现有字段回顾

select() 每条结果已有：`reasons`, `risks`, `factor_scores`, `factor_values`, `decision`, `risk_level`, `confidence`, `rows`, `data_source`。解释所需信息已齐，无需AI。

## 2. explain 字段设计

```python
explain = {
    "summary": str,          # 一句话总括
    "strengths": [str],      # 主要加分项（1-3条，复用reasons）
    "weaknesses": [str],     # 主要扣分/风险（1-3条，复用risks）
    "risk_note": str,        # 风险提示（按risk_level生成）
    "confidence_note": str,  # 置信度说明（按confidence/rows/cov生成）
}
```

### 生成规则

**summary**: `{score}分 / {决策中文}。{reasons[0]}，{reasons[1]或"基于N条K线"}。`

**strengths**: `reasons[:3]` 直接复用。

**weaknesses**: `risks[:3]`，无风险则 `["暂无显著风险信号"]`。

**risk_note**: 按 risk_level 输出：
- low → "当前风险信号较少，数据相对稳定。"
- medium → "存在一定风险信号：{risks}。建议关注后续走势。"
- high → "风险信号较多：{risks}。需谨慎对待。"

**confidence_note**: 按 confidence + rows 组合：
- high + ≥250 → "基于N条K线评分，数据充足，评分较为可靠。"
- medium → "基于N条K线评分，数据一般。"
- low 或 <120 → "数据不足（仅N条），评分置信度低，不应当直接作为决策依据。"

## 3. 三处展示

| 处 | 展示方式 |
|----|---------|
| CLI JSON | 每条结果新增 `"explain": {...}` 字段 |
| Markdown报告 | 逐只追加 `📝 解释 / ✅ 加分 / ⚠️ 风险 / 📊 可靠性` 四行 |
| Streamlit UI | expander顶部新增 `📝 summary` + expander内 `📊 可靠性说明` |

## 4. 禁止输出

❌ 建议买入/卖出/目标价/收益预测/任何投资建议

## 5. 实现步骤

P8.2-1: 实现 `_build_explain()` + 追加到 select 返回
P8.2-2: 更新 reports/generator.py
P8.2-3: 更新 app.py
P8.2-4: 收口验收

## 6. 不做什么

❌ 不改评分公式/因子权重/排序/JSON现有字段/不引入AI
