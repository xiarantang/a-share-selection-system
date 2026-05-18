# 发布前检查清单

> 每次发布前逐项检查，确保交付质量。
> 当前发布前一键验收聚合 12 项自动检查，建议先跑一键验收再逐项手动确认。

---

## 1. 自动验收（一键完成）

```bash
python3 scripts/confirm_release_ready.py
```

聚合 12 项检查（语法、UI 验收、策略验收、CLI 选股/报告、run_metadata 复盘记录、排障体验、废弃 API 残留、文档口径一致性等），全部通过 exit 0，任一失败 exit 1。

### 独立验收（可选单独运行）

```bash
# 文档口径一致性（19 项）
python3 scripts/confirm_docs_consistency.py

# run_metadata 复盘记录验收（20 项）
python3 scripts/confirm_run_metadata.py

# 排障体验验收（13 项）
python3 scripts/confirm_troubleshooting.py
```

---

## 2. 环境

- [ ] `python3 --version` >= 3.9
- [ ] `.venv/` 虚拟环境存在且依赖已安装 (`pip install -r requirements-ui.txt`)
- [ ] （可选）第三级兜底数据通道（skill_fallback）可安装：双击 `scripts/install_fallback.command`。系统已内置 baostock（约 570 条日 K），不装也能正常使用。

---

## 3. 启动

- [ ] `test -x start_ui.command` — 可执行权限存在
- [ ] `bash -n start_ui.command` — 无语法错误
- [ ] `bash -n scripts/install_fallback.command` — 无语法错误
- [ ] 双击 `start_ui.command` 可正常启动，浏览器打开 `http://localhost:8501`
- [ ] 首页显示「✅ 系统就绪」或明确提示缺少什么
- [ ] 首页截图已更新到 `docs/screenshots/home.png`

---

## 4. 选股

- [ ] 点击「🚀 开始选股」按钮，30-60 秒内完成，显示「✅ 选股完成」
- [ ] 候选表格 Tab 有数据（排名/代码/名称/评分/决策/风险/置信度）
- [ ] 数据区间和覆盖不全提示在主页面可见
- [ ] 验证摘要关键指标在主页面可见（整体质量/平均评分/覆盖不足率）
- [ ] 错误/等待/空结果提示为白话，技术详情在折叠区内
- [ ] 结果页截图已更新到 `docs/screenshots/result.png`

---

## 5. CLI 全链路

- [ ] 语法检查全部通过
```bash
python3 -B -c "import ast; [ast.parse(open(f).read()) for f in ['main.py','app.py','data/fetcher.py','data/universe.py','strategies/selection.py','validation/selection_validator.py','validation/backtest_validator.py','reports/generator.py']]"
```
- [ ] `.venv/bin/python main.py select --universe static --limit 10 --top 5 --start 2024-01-01` EXIT:0
- [ ] `.venv/bin/python main.py report` EXIT:0

---

## 6. 文档

- [ ] `docs/USER_GUIDE.md` 存在，内容准确
- [ ] `docs/TROUBLESHOOTING.md` 存在，覆盖常见问题
- [ ] `README.md` 版本号正确，截图链接有效
- [ ] `CHANGELOG.md` 已更新当前版本内容
- [ ] `PROJECT_STATE.md` 已更新当前阶段

---

## 7. tag 前确认（手动，不自动打 tag）

```bash
# 确认工作区干净
git status --short

# 确认最近提交
git log --oneline -8 --decorate

# 确认当前 HEAD 无多余 tag
git tag --points-at HEAD
```

- [ ] `git status --short` 输出为空（工作区干净）
- [ ] `git log --oneline -8 --decorate` 最新 commit 为预期内容
- [ ] `git tag --points-at HEAD` 仅显示预期的 tag（或为空）
- [ ] 确认版本号后，由人工决定是否执行 `git tag` 和 `git push --tags`

---

> 检查完成的人在此签名：__________ 日期：__________
>
> 免责声明：本系统仅供研究学习，不构成投资建议。
