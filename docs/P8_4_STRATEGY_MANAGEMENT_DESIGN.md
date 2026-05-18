# P8.4 策略管理设计

> 日期：2026-05-18 | 阶段：P8.4-0（设计文档）
> 前置：P8.1 数据质量增强 ✅、P8.2 策略可解释增强 ✅、P8.3 UI 体验增强 ✅
> 约束：不改评分公式，不改排序，不改数据链路，不引入 AI/qlib，不换前端框架

---

## 1. 结论先行

P8.4 应该从**最小策略管理层**起步，而不是评分重写。

当前系统只有一套硬编码的规则因子策略（6 因子评分 + decision/risk_level/confidence），直接编译在 `strategies/selection.py` 里。没有注册机制、没有元数据、没有策略选择入口。P8.4 的目标是为将来的多策略扩展铺一条安全的路——先搭骨架，再做选择器，最后才考虑第二套策略。每一步都可以独立交付和验收。

**核心原则：只加壳，不改芯。**

---

## 2. 目标与非目标

### 2.1 目标

| 编号 | 目标 | 说明 |
|------|------|------|
| G-1 | 策略注册骨架 | 定义策略元数据格式和注册表，当前仅注册默认策略 |
| G-2 | CLI 可选策略参数 | `select --strategy default` 为可选参数，不传时行为与现在完全一致 |
| G-3 | Streamlit 策略选择器 | UI 侧栏增加策略下拉框，默认选中默认策略，附带小白说明和风险提示 |
| G-4 | 文档和验收 | 每步交付后有验收脚本和 PROJECT_STATE 更新 |
| G-5 | 向后兼容 | 所有改动不破坏现有 JSON 字段、CLI 行为、报告格式 |

### 2.2 非目标

| 编号 | 非目标 | 说明 |
|------|--------|------|
| NG-1 | 不写第二套策略 | P8.4 只搭骨架和选择器，不引入新策略逻辑 |
| NG-2 | 不改评分/排序 | 策略管理层只是调度入口，不改 `score_stock()` / `compute_factors()` |
| NG-3 | 不改数据链路 | 不动 akshare/baostock/skill_fallback 优先级和降级逻辑 |
| NG-4 | 不引入 AI/qlib | 策略选择、参数配置、决策逻辑不使用 AI |
| NG-5 | 不做交易执行 | 不接入券商 API，不下单，不做实盘 |
| NG-6 | 不输出投资建议 | 不使用"建议买入/卖出/目标价/收益预测"等措辞 |
| NG-7 | 不做策略参数化调优 | 不暴露因子权重、阈值等内部参数给用户 |
| NG-8 | 不做策略回测对比 | 不做"策略 A vs 策略 B"对比面板 |

---

## 3. 当前状态总结

### 3.1 策略现状

系统当前只有一套策略，硬编码在 `strategies/selection.py`：

- **评分模型**：6 因子规则评分（data_quality/trend/momentum/volume/risk/pattern，满分 100）
- **计算函数**：`compute_factors()` + `score_stock()`
- **引擎类**：`SelectionEngine`，暴露 `select()` / `select_top()` 两个方法
- **输出字段**：score, reasons, risks, factor_scores, factor_values, decision, risk_level, confidence, coverage_warning, explain
- **无注册机制**：CLI 直接调用 `SelectionEngine().select()`，UI 直接实例化 `SelectionEngine`

### 3.2 CLI 调用链

```
main.py select → SelectionEngine().select(symbols, start_date) → score_stock() → 结果列表
```

### 3.3 UI 调用链

```
app.py → 实例化 SelectionEngine() → select() → 展示结果（Top3 卡片 + 候选表格 + 逐只详情）
```

### 3.4 验证链路

```
select → validate → backtest-validate → report
```

### 3.5 关键约束

- `select` 命令不支持 `--strategy` 参数
- `app.py` 没有策略选择入口
- JSON 输出没有 `strategy_id` 字段
- 报告不标注使用的策略

---

## 4. 用户界面概念设计

### 4.1 Streamlit 策略选择器

**位置**：侧栏参数区域，在"股票池"和"扫描数量"之间。

**布局**（示意）：

```
侧栏
├── 📊 股票池          [static (55只精选)  ▼]
├── 🧭 选股策略        [默认规则策略       ▼]  ← 新增
│   └── ℹ️ 当前策略：基于6因子规则评分（趋势+动量+量能+风控+形态+数据质量），
│       适合A股主板中大盘个股筛选。
│       ⚠️ 仅供研究学习，不构成投资建议。
├── 🔢 扫描数量        [10  ▼]
├── 📋 展示数量        [5   ▼]
├── 📅 数据起始日期    [2024-01-01]
├── [🚀 开始选股]
└── ⚠️ 免责声明
```

**交互规则**：

| 规则 | 说明 |
|------|------|
| 默认选中 | 页面打开时默认选中"默认规则策略"，与当前行为完全一致 |
| 不可取消 | 至少选中一个策略，不能为空 |
| 策略说明 | 选中后展示该策略的 `description`（1-2 句话）和 `risk_reminder`（风险提示） |
| 禁用词 | 策略说明和风险提示中不使用"买入/卖出/目标价/收益预测/建议买/建议卖"等措辞 |
| 小白友好 | 策略名称使用中文，说明用通俗语言 |

### 4.2 CLI 策略参数

```
# 现有行为不变（不传 --strategy 时默认使用 default）
python3 main.py select --universe static --limit 10 --top 5

# 可选指定策略（P8.4-2 新增，向后兼容）
python3 main.py select --universe static --limit 10 --top 5 --strategy default
```

**规则**：

| 规则 | 说明 |
|------|------|
| `--strategy` 可选 | 不传时使用默认策略，行为与 P8.3 完全一致 |
| `--strategy` 值校验 | 传入不存在的 strategy_id 时，报错并打印可用策略列表 |
| 无额外必选参数 | 不引入 `--strategy-params` 等复杂配置 |

### 4.3 结果标注

选股结果 JSON 新增 `strategy_id` 字段（仅标注，不改变其他字段）：

```json
{
  "strategy_id": "default",
  "candidates": [...],
  ...
}
```

报告和 UI 展示可选展示策略名称（如"选股策略：默认规则策略"），不影响已有内容。

---

## 5. 策略元数据概念设计

### 5.1 元数据字段

每个策略在注册时需要提供以下元数据（仅设计，不实现）：

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `id` | str | 是 | 唯一标识符，小写英文+下划线 | `"default"` |
| `name` | str | 是 | 中文显示名称 | `"默认规则策略"` |
| `description` | str | 是 | 1-2 句话的策略说明，小白可读 | `"基于6因子规则评分（趋势+动量+量能+风控+形态+数据质量），适合A股主板中大盘个股筛选。"` |
| `suitable_scenario` | str | 是 | 适用场景描述 | `"A股主板中大盘，日常选股筛选"` |
| `risk_reminder` | str | 是 | 风险提示文案 | `"规则因子评分不预测收益，数据不足时评分置信度会降低。"` |
| `enabled` | bool | 是 | 是否启用 | `True` |
| `entry_function` | str | 是 | 入口函数名（模块级） | `"strategies.selection:SelectionEngine"` |

### 5.2 注册表概念

注册表是一个轻量的字典/列表结构（仅设计，不实现）：

```
STRATEGY_REGISTRY = {
    "default": {
        "id": "default",
        "name": "默认规则策略",
        "description": "基于6因子规则评分...",
        "suitable_scenario": "A股主板中大盘，日常选股筛选",
        "risk_reminder": "规则因子评分不预测收益，数据不足时评分置信度会降低。",
        "enabled": True,
        "entry_function": "strategies.selection:SelectionEngine",
    }
}
```

### 5.3 设计约束

| 约束 | 说明 |
|------|------|
| 不用数据库 | 注册表放在 Python 模块中（如 `strategies/registry.py`），纯代码 |
| 不用配置文件 | 不引入 YAML/JSON/TOML 策略配置文件，避免增加解析复杂度 |
| 不用插件机制 | 不做动态加载、热插拔，策略在代码中静态注册 |
| 不暴露内部参数 | 元数据不含因子权重、阈值等内部实现细节 |

---

## 6. CLI 兼容性概念

### 6.1 向后兼容原则

| 原则 | 说明 |
|------|------|
| 不传 `--strategy` 时行为不变 | `python3 main.py select --universe static --limit 10 --top 5` 结果与 P8.3 完全一致 |
| `--strategy default` 等价于不传 | 显式传入默认策略 ID，行为与不传相同 |
| JSON 字段只增不删 | 新增 `strategy_id`，不删除/改名任何现有字段 |
| 报告格式不变 | Markdown 报告可选标注策略名称，但不改变已有段落结构 |
| 退出码不变 | select/validate/backtest-validate/report 的 PASS/FAIL 逻辑不变 |

### 6.2 CLI 参数变更（仅设计）

```
# main.py select 子命令新增可选参数
parser.add_argument(
    "--strategy",
    default="default",
    help="选股策略ID（默认：default）。可用策略见 --list-strategies。"
)

# 新增列表命令（可选，P8.4-2 视情况实现）
parser.add_argument(
    "--list-strategies",
    action="store_true",
    help="列出所有可用策略。"
)
```

### 6.3 错误处理

| 场景 | 处理方式 |
|------|----------|
| 传入不存在的 strategy_id | 打印错误信息 + 可用策略列表，EXIT: 1 |
| strategy_id 对应策略 disabled | 打印提示"该策略当前未启用" + 可用策略列表，EXIT: 1 |
| 注册表为空（理论上不会） | 打印"无可用策略"，EXIT: 1 |

---

## 7. 安全边界

### 7.1 绝对禁止

| 编号 | 禁止项 | 原因 |
|------|--------|------|
| S-1 | 不改 `score_stock()` 函数 | 评分公式是系统核心，P8.4 只做管理层 |
| S-2 | 不改 `compute_factors()` 函数 | 因子计算逻辑不变 |
| S-3 | 不改 `SelectionEngine.select()` 的核心逻辑 | 只在外层加调度，不改内部 |
| S-4 | 不改数据链路 | akshare/baostock/skill_fallback 优先级不变 |
| S-5 | 不引入 AI/qlib | 策略选择不使用 AI，策略逻辑不使用 qlib |
| S-6 | 不做交易执行 | 不接入券商 API，不下单 |
| S-7 | 不输出投资建议 | 不使用"买入/卖出/目标价/收益预测"等措辞 |

### 7.2 允许但需谨慎

| 编号 | 允许项 | 注意事项 |
|------|--------|----------|
| A-1 | 新增 `strategies/registry.py` | 仅注册逻辑，不含评分 |
| A-2 | `main.py` 增加 `--strategy` 参数 | 可选参数，默认值保持现有行为 |
| A-3 | `app.py` 增加策略选择器 | 侧栏新增下拉框，不影响结果展示区 |
| A-4 | JSON 结果新增 `strategy_id` | 只增不删，不影响现有字段 |
| A-5 | 报告可选标注策略名称 | 不改变报告段落结构 |

---

## 8. 分步交付计划

### P8.4-1：注册骨架

**目标**：创建 `strategies/registry.py`，注册默认策略，提供查询接口。

**允许新增的文件**：
- `strategies/registry.py`

**允许修改的文件**：
- 无（本阶段不动 main.py / app.py）

**具体内容**：

| 内容 | 说明 |
|------|------|
| 注册表数据结构 | `STRATEGY_REGISTRY` 字典，初始包含 `default` 策略元数据 |
| `register_strategy(meta)` | 注册函数 |
| `get_strategy(strategy_id)` | 按 ID 查询，返回元数据或 None |
| `list_strategies()` | 返回所有 enabled=True 的策略列表 |
| `get_default_strategy()` | 返回默认策略（`default`） |
| 默认策略注册 | 启动时自动注册 `default` 策略 |

**验收命令**：
```bash
python3 -m py_compile strategies/registry.py
python3 -c "from strategies.registry import list_strategies; print(list_strategies())"
python3 main.py select --universe static --limit 10 --top 5  # 行为不变
python3 main.py backtest-validate
python3 main.py report
```

**验收标准**：
- `list_strategies()` 返回包含 `default` 的列表
- `get_strategy("default")` 返回完整元数据
- `get_strategy("nonexistent")` 返回 None
- CLI 全链路行为不变
- JSON 输出不变（本阶段不加 `strategy_id`）

---

### P8.4-2：CLI 可选策略参数

**目标**：`main.py select` 支持 `--strategy` 可选参数。

**允许修改的文件**：
- `main.py`（仅 select 子命令的参数解析和调度逻辑）

**禁止修改的文件**：
- `strategies/selection.py`
- `data/fetcher.py`
- `reports/generator.py`
- `validation/` 目录
- `app.py`

**具体改动**：

| 改动 | 说明 |
|------|------|
| 新增 `--strategy` 参数 | 可选，默认值 `"default"`，不传时行为与 P8.3 一致 |
| 参数校验 | 传入不存在的 strategy_id 时报错并打印可用列表 |
| 结果新增 `strategy_id` | JSON 输出顶层新增 `"strategy_id": "default"`，不影响其他字段 |
| 调度逻辑 | 根据 strategy_id 查注册表，获取 entry_function，调用对应引擎 |

**向后兼容保证**：
- `python3 main.py select --universe static --limit 10 --top 5` 输出与 P8.3 完全一致（仅多一个 `strategy_id` 字段）
- `python3 main.py select ... --strategy default` 等价于不传 `--strategy`
- `validate` / `backtest-validate` / `report` 命令行为不变

**验收命令**：
```bash
python3 -m py_compile main.py
python3 main.py select --universe static --limit 10 --top 5
python3 main.py select --universe static --limit 10 --top 5 --strategy default
python3 main.py select --universe static --limit 10 --top 5 --strategy nonexistent  # 应报错
python3 main.py backtest-validate
python3 main.py report
```

**验收标准**：
- 不传 `--strategy` 时结果与 P8.3 一致
- 传 `--strategy default` 时结果与不传一致
- 传入不存在的 ID 时报错（EXIT: 1）并打印可用列表
- JSON 新增 `strategy_id` 字段
- CLI 全链路通过

---

### P8.4-3：Streamlit 策略选择器

**目标**：侧栏增加策略下拉框，结果区标注策略名称。

**允许修改的文件**：
- `app.py`（仅侧栏参数区和结果标注区）

**禁止修改的文件**：
- `strategies/selection.py`
- `data/fetcher.py`
- `reports/generator.py`
- `validation/` 目录
- `main.py`

**具体改动**：

| 改动 | 说明 |
|------|------|
| 侧栏新增策略选择器 | `st.selectbox`，选项来自注册表，默认选中 `default` |
| 策略说明展示 | 选中后展示 `description`（1-2 句）和 `risk_reminder` |
| 结果标注 | 结果区顶部或数据概览区域标注"选股策略：默认规则策略" |
| 传参给引擎 | 选择策略后，调用对应入口函数（当前只有 default） |

**UI 设计原则**（继承 P8.3）：
- 中文优先
- 颜色有意义
- 渐进式展示
- 不做营销

**验收命令**：
```bash
python3 -m py_compile app.py
python3 main.py select --universe static --limit 10 --top 5
python3 main.py backtest-validate
python3 main.py report
```

**验收标准**：
- 侧栏显示策略下拉框，默认选中"默认规则策略"
- 选中后展示策略说明和风险提示
- 风险提示中不包含"买入/卖出/目标价/收益预测"等禁词
- 选股结果与不选策略时一致（当前只有 default）
- CLI 全链路不受影响

---

### P8.4-4：文档和验收

**目标**：更新文档和验收脚本，确认 P8.4 全部完成。

**允许修改的文件**：
- `docs/USER_GUIDE.md`（增加策略选择说明）
- `README.md`（更新能力描述）
- `scripts/` 目录下的确认脚本（新增 `scripts/confirm_p84.py`）
- `PROJECT_STATE.md`

**禁止修改的文件**：
- `strategies/selection.py`
- `data/fetcher.py`
- `reports/generator.py`
- `validation/` 目录

**具体改动**：

| 改动 | 说明 |
|------|------|
| 验收脚本 | `scripts/confirm_p84.py`：验证注册表、CLI 参数、UI 元素 |
| 用户指南 | 新增"策略选择"段落 |
| README | 更新能力列表和 CLI 参数说明 |
| PROJECT_STATE | 记录 P8.4 完成状态 |

**验收标准**：
- 验收脚本全部通过
- 用户指南包含策略选择说明
- README 能力描述准确
- CLI 全链路通过
- 禁词检查通过

---

## 9. P8.4 整体验收清单

| 编号 | 检查项 | 验证方式 |
|------|--------|----------|
| AC-1 | 注册表包含 default 策略 | `from strategies.registry import list_strategies; assert len(list_strategies()) >= 1` |
| AC-2 | default 策略元数据完整 | `get_strategy("default")` 返回所有必填字段 |
| AC-3 | CLI 不传 `--strategy` 行为不变 | `select` 输出与 P8.3 一致 |
| AC-4 | CLI 传 `--strategy default` 行为不变 | 与不传结果一致 |
| AC-5 | CLI 传入不存在 ID 报错 | EXIT: 1，打印可用列表 |
| AC-6 | JSON 新增 `strategy_id` 字段 | 结果包含 `"strategy_id": "default"` |
| AC-7 | JSON 其他字段不变 | 对比 P8.3 输出，除 `strategy_id` 外无差异 |
| AC-8 | UI 侧栏有策略选择器 | 截图验证 |
| AC-9 | UI 策略说明和风险提示无禁词 | 不含"买入/卖出/目标价/收益预测" |
| AC-10 | UI 选股结果与不选策略时一致 | 当前只有 default 策略 |
| AC-11 | CLI 全链路通过 | select + validate + backtest-validate + report 均 EXIT: 0 |
| AC-12 | `py_compile` 通过 | app.py / main.py / strategies/registry.py |
| AC-13 | 未改评分/排序/数据链路 | `git diff strategies/selection.py` 无变化 |
| AC-14 | 未改报告生成逻辑 | `git diff reports/generator.py` 无变化 |
| AC-15 | 未改数据层 | `git diff data/` 无变化 |
| AC-16 | 禁词检查通过 | 不在正向文案中出现"买入/卖出/目标价/收益预测/建议买/建议卖" |
| AC-17 | 文档更新完成 | USER_GUIDE / README / PROJECT_STATE 已更新 |
| AC-18 | 验收脚本通过 | `scripts/confirm_p84.py` 全部检查通过 |

---

## 10. 设计原则总结

| 编号 | 原则 | 说明 |
|------|------|------|
| DP-1 | 只加壳，不改芯 | 策略管理层是调度壳，不改评分/排序/数据 |
| DP-2 | 最小骨架先行 | 先搭注册表，再做选择器，最后才考虑新策略 |
| DP-3 | 向后兼容 | 每步交付后，现有行为不变 |
| DP-4 | 中文优先 | 策略名称、说明、风险提示全部中文 |
| DP-5 | 禁词红线 | 不使用"买入/卖出/目标价/收益预测/建议买/建议卖" |
| DP-6 | 不暴露内部参数 | 用户看到的是策略名称和说明，不是因子权重和阈值 |
| DP-7 | 不做复杂配置 | 不引入 YAML/JSON/TOML 策略配置文件 |
| DP-8 | 保持双击启动 | `start_ui.command` 启动方式不变 |
| DP-9 | 保持 CLI 验收 | `py_compile` / `select` / `backtest-validate` / `report` 必须通过 |
| DP-10 | 每步独立交付 | 每个子步骤可独立 commit + push + 验收 |

---

## 11. 风险和缓解

| 风险 | 缓解措施 |
|------|----------|
| 注册表过度设计 | 保持最简结构（字典 + 查询函数），不引入类继承或工厂模式 |
| UI 策略选择器分散注意力 | 默认选中 default 策略，说明简洁，不占过多空间 |
| `--strategy` 参数增加认知负担 | 不传时行为不变，参数说明明确 |
| 误入策略参数化调优 | P8.4 明确排除参数暴露，只做策略选择 |
| 误入评分重写 | 注册表不含评分逻辑，entry_function 指向现有引擎 |

---

## 12. 与 P8.3 的关系

P8.4 继承 P8.3 的所有设计原则和 UI 规范：

- 继承 P8.3 的中文标签映射（决策/风险/置信度）
- 继承 P8.3 的 Top3 速览卡片和逐只详情展示
- 继承 P8.3 的风险分级着色（红/橙/绿）
- 继承 P8.3 的禁词红线
- 策略选择器遵循 P8.3 的侧栏简化风格

P8.4 不修改 P8.3 已完成的任何 UI 区域内容，只在侧栏新增一个选择器。
