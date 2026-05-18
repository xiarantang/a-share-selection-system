# P8.7 发布前总复盘与下一阶段边界设计

> 创建时间：2026-05-18
> 阶段：P8.7-0（仅文档，不修改产品代码）
> 依据：P8.1–P8.6 已完成的全部阶段记录

---

## 1. P8.1–P8.6 已完成能力总结

### 1.1 数据层（P8.1）

| 项目 | 状态 |
|------|------|
| 主数据源切换为 baostock | ✅ 稳定 570 条日 K |
| akshare 作为前置优先源 | ✅ 保留 |
| skill_fallback 兜底 | ✅ 保留 |
| 三级降级链路 akshare → baostock → skill_fallback | ✅ 已验收 |
| 覆盖率误报修正 | ✅ `_has_coverage_warning()` 抽出并验证 |
| CLI / 报告 / UI 三处数据源展示一致 | ✅ P8.1-4 收口 |

### 1.2 策略解释层（P8.2）

| 项目 | 状态 |
|------|------|
| `_build_explain()` 生成小白解释 | ✅ summary / strengths / weaknesses / risk_note / confidence_note |
| JSON 结果含 explain 字段 | ✅ Top5 验证通过 |
| Markdown 报告接入 explain | ✅ 优雅降级 |
| Streamlit UI 接入 explain | ✅ expander 顶部展示 |
| 投资建议措辞禁词检查 | ✅ |

### 1.3 UI 体验优化（P8.3）

| 项目 | 状态 |
|------|------|
| 首页简化引导（选参数 → 开始选股 → 看结果） | ✅ |
| Top3 速览卡片 | ✅ 奖牌 + 评分 + 中文标签 |
| 决策/风险/置信度中文标签 | ✅ UI 展示层映射，底层英文不变 |
| 因子得分中文标签 + 小图标 | ✅ |
| 技术指标详情折叠 | ✅ 不堆首层 |
| 风险分级着色（绿/橙/红） | ✅ |
| 数据区间友好化（"约近 X 个月"） | ✅ |
| 结果页数据概览 `st.caption` 可读性修复 | ✅ |
| 44 项自动验收脚本 + 截图更新 | ✅ |

### 1.4 策略管理层（P8.4）

| 项目 | 状态 |
|------|------|
| 策略元数据注册表 `strategies/registry.py` | ✅ |
| CLI `--strategy` 可选参数 | ✅ 无效策略 exit 1 |
| UI 策略选择器 | ✅ 侧栏展示策略名称/场景/风险提醒 |
| JSON 结果顶层新增 strategy_id / strategy 元数据 | ✅ |
| 兼容旧签名 `execute_strategy(strategy_name, script=None, args=None)` | ✅ |
| 文档验收收口 | ✅ 路线图一致性确认 |

### 1.5 AI 辅助解释边界评审（P8.5）

| 项目 | 状态 |
|------|------|
| 决策文档 | ✅ 结论：暂缓实现 |
| 硬性禁止边界明确 | ✅ |
| 可接受最小方案设计（仅设计，未实现） | ✅ |
| 文档字段名一致性收口 | ✅ |

### 1.6 UI 兼容性与验收（P8.6）

| 项目 | 状态 |
|------|------|
| `use_container_width` → `width="stretch"` | ✅ 4 处替换 |
| `applymap` → `map` | ✅ 1 处替换 |
| 版本约束升级（streamlit>=1.39.0, pandas>=2.1.0） | ✅ |
| UI 冒烟验收 + 截图更新 | ✅ |
| start_ui.command 启动脚本冒烟验收 | ✅ Python3 检测/虚拟环境/依赖就绪/HTTP 200 |
| 公开文档状态一致性收口 | ✅ README / USER_GUIDE / UI_ACCEPTANCE_RESULT |

---

## 2. 当前小白路径

双击 `start_ui.command` → 自动安装依赖 → 打开浏览器 → 左侧选择参数（股票池/策略/扫描数量/展示数量/起始日期）→ 点击"开始选股" → 等待结果 → Top3 速览 + 候选表格 + 逐只详情（含小白解释、风险分级、因子得分）。

### 核心流程一句话总结

> **双击 start_ui.command → 选参数 → 开始选股 → 看结果。**

---

## 3. 已验收入口清单

| 验收入口 | 类型 | 状态 |
|----------|------|------|
| `python3 -m py_compile app.py` | 语法 | ✅ 通过 |
| `python3 main.py select --universe static --limit 10 --top 5` | CLI 选股 | ✅ EXIT:0，10/10 baostock |
| `python3 main.py backtest-validate` | CLI 验证 | ✅ EXIT:0 |
| `python3 main.py report` | CLI 报告 | ✅ EXIT:0 |
| Streamlit UI 冒烟（首页/结果页/逐只详情） | UI | ✅ 无报错无废弃警告 |
| `start_ui.command` 双击启动 | 启动脚本 | ✅ HTTP 200 |
| 截图（home.png / result.png） | 截图 | ✅ 已更新 |
| 44 项自动验收脚本 `confirm_p83_ui.py` | 自动验收 | ✅ 44/44 |
| 策略注册验收 `confirm_p84_registry.py` | 自动验收 | ✅ 35/35 |
| CLI 策略参数验收 `confirm_p84_cli.py` | 自动验收 | ✅ 17/17 |
| UI 策略选择器验收 `confirm_p84_ui.py` | 自动验收 | ✅ 36/36 |
| 文档验收 `confirm_p84_docs.py` | 自动验收 | ✅ 通过 |
| 投资建议措辞禁词检查 | 安全 | ✅ 通过 |

---

## 4. 剩余风险

### 4.1 数据源网络波动

- akshare 依赖外部 API，网络波动时可能失败。
- **已有兜底**：baostock 作为第二级数据源，实测稳定 570 条日 K。
- **已有兜底**：skill_fallback 作为第三级兜底。
- 三级降级链路已在 P8.1 验收。

### 4.2 akshare 偶发失败

- akshare 偶发超时或返回空数据。
- **已有兜底**：baostock 可兜底，不会导致选股失败。
- 首次运行时 baostock 需登录，已有 finally 释放机制。

### 4.3 非投资建议边界

- 系统输出仅供研究学习，不构成投资建议。
- **已有措施**：UI 侧栏免责声明、报告免责声明、explain 禁词检查。
- **已有措施**：AI 辅助解释默认关闭（P8.5 决策）。
- 用户需自行判断投资风险。

### 4.4 其他已知限制

- 当前只有一套「默认规则策略」，策略管理是入口壳。
- baostock 数据覆盖约 2 年（570 个交易日），非全量历史。
- 静态股票池固定，不支持自定义股票池。
- 无自动化测试套件（CI），依赖手动验收脚本。

---

## 5. 下一阶段建议（仅建议，不实现）

### 5.1 优先方向

| 优先级 | 方向 | 说明 |
|--------|------|------|
| P0 | 继续小白体验/验收稳定性 | 补充更多边界场景的冒烟测试；确保不同 macOS 版本双击启动一致 |
| P1 | 文档与用户引导 | 补充常见问题 FAQ；录制操作视频或动图 |
| P2 | 数据源稳定性监控 | 选股结果记录数据源命中率；长期追踪 baostock/akshare 可用率 |

### 5.2 明确暂不进入的方向

| 方向 | 状态 | 原因 |
|------|------|------|
| AI 实现（P8.5 及以后） | 暂不进入 | P8.5-0 决策：边界未完全可自动验收，暂缓 |
| 评分公式修改 | 不改 | 6 因子评分体系经多轮验收，当前稳定 |
| 排序逻辑修改 | 不改 | 评分→排序→TopN 链路已验收 |
| 数据链路修改 | 不改 | akshare → baostock → skill_fallback 三级降级已验收 |
| 报告逻辑修改 | 不改 | Markdown 报告含 explain 优雅降级，已验收 |

---

## 6. 免责声明

本系统仅供研究学习，不构成投资建议。系统输出的选股结果、策略解释、风险等级等信息均基于历史数据的规则计算，不保证未来收益。用户应自行判断投资风险，本系统不承担任何投资损失责任。

---

## 7. 发布前一键验收入口（P8.7-1）

> 从项目根目录运行，一条命令完成所有发布前检查。

```bash
python3 scripts/confirm_release_ready.py
```

### 检查项一览

| 序号 | 检查内容 | 对应命令 |
|------|---------|---------|
| 1 | app.py 语法检查 | `python3 -m py_compile app.py` |
| 2 | P8.3 UI 验收 (44项) | `python3 scripts/confirm_p83_ui.py` |
| 3 | P8.4 策略注册验收 | `python3 scripts/confirm_p84_registry.py` |
| 4 | P8.4 CLI 策略参数验收 | `python3 scripts/confirm_p84_cli.py` |
| 5 | P8.4 UI 策略选择器验收 | `python3 scripts/confirm_p84_ui.py` |
| 6 | P8.4 文档验收 | `python3 scripts/confirm_p84_docs.py` |
| 7 | CLI 选股 (static 10→Top5) | `.venv/bin/python main.py select --universe static --limit 10 --top 5` |
| 8 | CLI 报告生成 | `.venv/bin/python main.py report` |
| 9 | 废弃 API 残留检查 (应为空) | `rg -n "use_container_width\|\.applymap\(" app.py` |
| 10 | 文档口径一致性检查 | `python3 scripts/confirm_docs_consistency.py` |

### 退出码

- `0`：全部通过，可以发布。
- `1`：任一项失败，请修复后再发布。

### 输出格式

每项显示"通过/失败/跳过原因"，失败时附上命令和最后一段输出，方便定位问题。

---

## 8. P8.7-4 / P8.7-5 收口结果

### 8.1 P8.7-4 公开文档数据层描述一致性收口（`67e2c72`）

- docs/USER_GUIDE.md + docs/TROUBLESHOOTING.md 两份小白文档：移除所有"约 120 条""~120 条"硬编码数字，skill_fallback 统一描述为"第三级兜底（数据量可能较少）"
- 保留数据链路：akshare → baostock（~570 条日 K）→ skill_fallback
- 未修改产品代码、评分、排序、数据链路、报告逻辑

### 8.2 P8.7-5 启动入口 fallback 可选状态收口（`3966bf5`）

- app.py：FALLBACK_SCRIPT 不存在时从 st.error（阻止选股）改为 st.info（可选提示）
- start_ui.command：缺少 fallback 只提示"可选"，移除阻塞性文案
- scripts/install_fallback.command：标题改为"可选：安装第三级兜底数据通道"
- README.md：启动入口收口为两步启动，安装 fallback 章节改为可选
- 未修改评分、排序、数据链路、报告逻辑

### 8.3 小白启动路径确认

小白启动路径为：**双击 start_ui.command → 选参数 → 开始选股 → 看结果**。

`install_fallback` 只是可选兜底，不是启动前提。requirements-ui 已包含 baostock，skill_fallback 为可选第三级兜底。

---

## 9. 验收检查示例

```bash
# 关键词检查
rg -n "P8.7-0|P8.7-1|P8.6|start_ui.command|双击|不构成投资建议|暂不进入 AI|评分|排序|数据链路|confirm_release_ready" docs/P8_7_RELEASE_REVIEW.md PROJECT_STATE.md scripts/confirm_release_ready.py

# 产品代码和验收脚本语法检查（只读，不修改）
python3 -m py_compile app.py scripts/confirm_release_ready.py

# 发布前一键验收
python3 scripts/confirm_release_ready.py

# 确认工作区干净
git status --short
```

---

## 10. 发布候选结论（P8.7-6）

> v0.5 + P8 全部阶段（P8.1–P8.7）已完成，当前处于**发布候选**状态。

### 10.1 系统能做什么

- 通过 6 因子规则评分对 A 股静态股票池（55 只）进行量化筛选，输出 Top 候选及小白解释。
- 数据层：akshare → baostock（~570 条日 K）→ skill_fallback 三级降级，baostock 已包含在轻量依赖 `requirements-ui.txt` 中。
- 策略管理：策略元数据注册表 + CLI `--strategy` 参数 + UI 策略选择器（当前只有「默认规则策略」，不改变评分公式）。
- 验证与报告：选股质量评估 + 历史窗口复盘 + Markdown 日报，JSON 结果含 explain 小白解释字段。
- 可视化 UI：Streamlit 本地界面，Top3 速览卡片、中文决策/风险/置信度标签、风险分级着色、因子得分小图标。

### 10.2 怎么启动

小白路径：

> **双击 start_ui.command → 选参数 → 开始选股 → 看结果。**

- `start_ui.command` 自动检测 Python3、创建虚拟环境、安装 `requirements-ui.txt` 轻量依赖（含 baostock）、启动 Streamlit。
- 浏览器打开 `http://localhost:8501`，左侧选择参数（股票池/策略/扫描数量/展示数量/起始日期），点击"开始选股"。
- skill_fallback 是**可选第三级兜底**，不是启动前提；不安装也能正常使用。

### 10.3 怎么验收

发布前一键验收入口（维护者用）：

```bash
python3 scripts/confirm_release_ready.py
```

聚合 10 项检查（语法、UI 验收、策略验收、CLI 选股/报告、废弃 API 残留、文档口径一致性等），全部通过 exit 0，任一失败 exit 1。

### 10.4 边界：不能做什么

- **不碰实盘交易**：系统仅供研究学习，不连接券商账户，不执行交易。
- **不引入 AI/qlib 到评分排序链路**：P8.5 决策明确暂缓 AI 辅助解释；评分、排序、风控等级均为规则计算，不依赖机器学习模型。
- **不输出投资建议措辞**：系统输出为规则因子评分和解释；explain 禁词检查已验证。
- 数据覆盖受限于 baostock 约 2 年（570 个交易日），非全量历史。
- 静态股票池固定 55 只，暂不支持自定义。
- 无 CI 自动化测试，依赖手动验收脚本。

### 10.5 结论

当前 v0.5 + P8.1–P8.7 全部阶段已完成并通过验收。系统功能完整、启动路径清晰、边界明确，处于可发布的候选状态。后续如需迭代，应在不触碰上述边界的前提下进行。
