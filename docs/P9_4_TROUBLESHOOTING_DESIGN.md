# P9.4 小白排障增强设计文档

> 创建时间：2026-05-19
> 阶段：P9.4-0（仅设计，不实现）
> 基线：v0.5 + P8 发布候选 + P9.1-P9.3 文档治理与复盘记录增强

---

## 1. 当前排障体验诊断

### 1.1 已有排障素材

| 来源 | 覆盖场景 | 语气 | skill_fallback 定位 |
|------|----------|------|---------------------|
| docs/TROUBLESHOOTING.md (10 项) | 启动/Python/Git/浏览器/选股卡住/空结果/覆盖不全/术语 | 小白白话 | 可选 |
| docs/USER_GUIDE.md FAQ (5 项) | 卡住/覆盖不全/akshare失败/更新数据/加股票 | 小白白话 | 可选 |
| README.md 已知限制表 | 数据覆盖/数据源波动/等待时间/非预测 | 双重受众 | 可选 |
| app.py 内联提示 | 选股spinner/成功/失败/覆盖不全/回退/免责 | 混合 | 可选 |

### 1.2 诊断问题归纳

| # | 问题 | 影响 |
|---|------|------|
| D-1 | app.py 选股 spinner 只说"不要关闭页面"，无进度感知 | 小白等 30s+ 不知是否卡死 |
| D-2 | app.py 选股全部失败时，error 直接暴露技术细节（Python traceback） | 小白看到技术报错容易恐慌 |
| D-3 | app.py 复盘报错同样直接暴露 traceback | 同 D-2 |
| D-4 | 覆盖不全 info 提示"不应当直接作为投资决策依据"但未指向排障文档 | 小白不知道去哪看更多 |
| D-5 | TROUBLESHOOTING.md #6 说"某一源慢不影响最终结果"，但 UI 实际会阻塞等待 | 说法与体验不一致 |
| D-6 | USER_GUIDE FAQ 只覆盖 TROUBLESHOOTING 的 5/10 项 | 只看 USER_GUIDE 的小白错过关键排障 |
| D-7 | 无 Python 版本冲突排障（Homebrew vs 系统 Python） | 装 Python 后仍可能跑不起来 |
| D-8 | 无 pip install 失败排障（架构不匹配/ensurepip 不可用） | venv 创建失败无指引 |
| D-9 | 端口冲突用了 `lsof ... | xargs kill -9` 但未解释命令含义 | 小白盲目执行危险命令 |
| D-10 | 无实际报错信息对照表 | 小白搜索具体报错文本找不到匹配 |

### 1.3 做得好的地方（保持）

- skill_fallback 三处文档统一为"可选"，未说成启动前提
- 免责声明在 README / USER_GUIDE / TROUBLESHOOTING / app.py 四处一致
- TROUBLESHOOTING 整体语气小白友好（"不要慌"、"白话解释"）
- 数据源三级降级（akshare -> baostock -> skill_fallback）说明清晰

---

## 2. P9.4 总目标

**让小白知道"发生了什么、是否严重、下一步怎么做"，而不只是看到技术报错。**

具体目标：

1. 公开排障文档口径收口：修复诊断中发现的不一致，补充关键缺失场景。
2. UI 错误/等待/空结果提示增强：让 app.py 的 inline 提示更小白友好。
3. 启动脚本提示增强：让 start_ui.command 的关键输出更可读。
4. 排障验收脚本与发布前收口：确保排障增强不引入回归。

---

## 3. 不做清单

| 不做 | 原因 |
|------|------|
| 不改评分 / 排序 | 6 因子评分体系经多轮验收，当前稳定 |
| 不改数据链路优先级 | akshare -> baostock -> skill_fallback 三级降级已验收 |
| 不做自动修电脑环境 | 超出选股系统范围，风险高 |
| 不制造恐慌 | 排障提示用低压力表达，不渲染严重性 |
| 不把 skill_fallback 说成必装 | 三处文档已统一为可选，保持一致 |
| 不输出投资建议措辞 | 禁词红线 |
| 不改 Windows/Linux 支持范围 | 当前只支持 macOS，跨平台不在 P9 范围 |
| 不做数据库 / 登录 / 实盘交易 | 核心边界 |

---

## 4. 场景分级

### 4.1 启动前

| 场景 | 当前体验 | 改进方向 |
|------|----------|----------|
| Python 未安装 | TROUBLESHOOTING #2 有指引 | 保持，补 venv 失败场景 |
| pip install 失败 | 无指引 | 新增：常见原因 + 手动安装命令 |
| 端口 8501 被占 | TROUBLESHOOTING #5 有 lsof 命令 | 补命令含义说明 + 替代方案 |
| 浏览器打不开 localhost | TROUBLESHOOTING #5 有 | 保持 |

### 4.2 选股中

| 场景 | 当前体验 | 改进方向 |
|------|----------|----------|
| 等待时间长 (>60s) | spinner 只说"不要关闭页面" | 补进度提示或阶段说明 |
| 网络波动 / 数据源降级 | 成功提示里提到 skill_fallback | 保持，确保语气不恐慌 |
| 全部失败 | error 暴露 traceback | 隐藏 traceback 到折叠区，主提示白话 |
| 部分成功部分失败 | success 提示含数量 | 保持，已足够 |

### 4.3 结果后

| 场景 | 当前体验 | 改进方向 |
|------|----------|----------|
| 覆盖不全 | info 提示"不是报错" | 保持，补"详见排障指南"链接 |
| 报告未生成或过期 | 无 inline 提示 | 报告 Tab 已有"正在生成"spinner，保持 |
| 历史复盘慢 | spinner "较慢" | 保持，已设预期 |
| 历史复盘不代表未来表现 | report Tab caption 有 | 保持 |

---

## 5. 小白文案原则

1. **先白话结论，再给下一步**：先说"不影响使用"，再说"如果实在不放心可以怎么做"。
2. **技术详情放后面**：报错时主提示只说白话原因，traceback 放折叠区或 log。
3. **低压力表达**：用"可选"、"稍后重试"、"检查网络"，不用"必须"、"严重"、"紧急"。
4. **不渲染风险**：覆盖不全不是报错，数据源降级是正常设计，不要写成故障。
5. **指向排障文档**：在关键提示处加"详见 docs/TROUBLESHOOTING.md"或简短指引。
6. **禁词红线**：不使用交易指令类、收益承诺类等投资建议措辞。

---

## 6. 后续拆分

| 阶段 | 内容 | 改动范围 | 验收方式 |
|------|------|----------|----------|
| P9.4-1 | 公开排障文档口径收口 | docs/TROUBLESHOOTING.md / docs/USER_GUIDE.md | ✅ 已完成 |
| P9.4-2 | UI 错误/等待/空结果提示增强 | app.py（只改 inline 提示文案和布局） | ✅ 已完成 |
| P9.4-3 | 启动脚本提示增强 | start_ui.command（只改 echo 输出文案） | ✅ 已完成 |
| P9.4-4 | 排障验收脚本与发布前收口 | PROJECT_STATE.md / docs/ | P9.4-4.1 已完成（独立验收脚本） |

### 6.1 P9.4-1 公开排障文档口径收口

允许修改：docs/TROUBLESHOOTING.md、docs/USER_GUIDE.md、PROJECT_STATE.md
禁止修改：app.py、main.py、scripts/、strategies/、data/、reports/、validation/

主要内容：
- 修复 TROUBLESHOOTING #6 "某一源慢不影响" 与实际 UI 阻塞等待的表述不一致
- 补充 pip install / venv 失败场景
- 补充 lsof kill 命令的含义说明
- USER_GUIDE FAQ 扩充覆盖 TROUBLESHOOTING 的关键场景（至少补到 8/10）

### 6.2 P9.4-2 UI 错误/等待/空结果提示增强

允许修改：app.py、PROJECT_STATE.md
禁止修改：main.py、scripts/、strategies/、data/、reports/、validation/

主要内容：
- 选股/复盘 error 提示：隐藏 traceback 到折叠区，主提示用白话
- 选股 spinner：补充阶段说明（"正在拉取数据" → "正在计算评分"）如可行
- 覆盖不全 info：补"详见排障指南"指引
- 确保不改变功能逻辑，只改展示文案

### 6.3 P9.4-3 启动脚本提示增强

允许修改：start_ui.command、PROJECT_STATE.md
禁止修改：app.py、main.py、scripts/（install_fallback 除外）、strategies/、data/

主要内容：
- start_ui.command 的 echo 输出更小白友好
- 关键步骤补中文说明（如 pip install 阶段、启动浏览器阶段）
- 不改变脚本逻辑，只改输出文案

### 6.4 P9.4-4 排障验收脚本与发布前收口

允许修改：PROJECT_STATE.md、docs/
禁止修改：app.py、main.py、scripts/confirm_release_ready.py、strategies/、data/

主要内容：
- 确认所有排障增强后 confirm_release_ready 11/11 通过
- 确认 confirm_docs_consistency 通过
- PROJECT_STATE.md 记录 P9.4 完成
- 设计文档标记各子阶段完成状态

---

## 7. 验收标准

每一步都必须：

1. `python3 scripts/confirm_release_ready.py` 全部通过（11/11）。
2. `python3 scripts/confirm_docs_consistency.py` 全部通过（19/19）。
3. 不改变 Top 排序（同参数同数据源，结果与 P9.4 之前一致）。
4. 不改变评分、排序、数据链路、JSON 生成逻辑。
5. 不输出交易指令类、收益承诺类等投资建议措辞。

---

## 8. 明确禁止

- **不碰实盘交易**：系统仅供研究学习，不连接券商账户，不执行交易。
- **不引入 AI/qlib 到评分排序链路**：评分、排序、风控等级均为规则计算。
- **不输出投资建议措辞**：排障提示只描述状态和下一步，不给操作建议。
- **不做数据库/登录/复杂前后端**：保持本地文件 + Streamlit 轻量架构。
- **不重写评分/排序**：6 因子评分体系经多轮验收，当前稳定。
- **不改数据链路优先级**：akshare -> baostock -> skill_fallback 三级降级已验收。
- **不把可选 fallback 说成启动前提**：三处文档已统一为可选，保持一致。

---

## 9. 免责声明

本系统仅供研究学习，不构成投资建议。排障增强不改变选股结果，只改善小白使用体验。
