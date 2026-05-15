# 发布前检查清单

> 每次发布前逐项检查，确保交付质量。

## 环境

- [ ] `python3 --version` >= 3.9
- [ ] `.venv/` 虚拟环境存在且依赖已安装 (`pip install -r requirements-ui.txt`)
- [ ] `~/.agents/skills/a-share-data/scripts/fetch_history_fallback.py` 备用数据通道已安装

## 启动

- [ ] `bash -n start_ui.command` 无语法错误
- [ ] `bash -n scripts/install_fallback.command` 无语法错误
- [ ] 双击 `start_ui.command` 可正常启动，浏览器打开 `http://localhost:8501`
- [ ] 首页显示「✅ 可以开始选股」或明确提示缺少什么
- [ ] 首页截图已更新到 `docs/screenshots/home.png`

## 选股

- [ ] 点击「🚀 开始选股」按钮，30-60 秒内完成，显示「✅ 选股完成」
- [ ] 候选表格 Tab 有数据（排名/代码/名称/评分/决策/风险/置信度）
- [ ] 数据区间和覆盖不全提示在主页面可见
- [ ] 验证摘要关键指标在主页面可见（整体质量/平均评分/覆盖不足率）
- [ ] 结果页截图已更新到 `docs/screenshots/result.png`

## CLI 全链路

- [ ] 语法检查全部通过
```bash
python3 -B -c "import ast; [ast.parse(open(f).read()) for f in ['main.py','app.py','data/fetcher.py','data/universe.py','strategies/selection.py','validation/selection_validator.py','validation/backtest_validator.py','reports/generator.py']]"
```
- [ ] `python3 main.py select --universe static --limit 10 --top 5 --start 2024-01-01` EXIT:0
- [ ] `python3 main.py backtest-validate --selection reports/output/selection_latest.json --top 5` EXIT:0
- [ ] `python3 main.py report --selection reports/output/selection_latest.json` EXIT:0

## 文档

- [ ] `docs/USER_GUIDE.md` 存在，内容准确
- [ ] `docs/TROUBLESHOOTING.md` 存在，覆盖常见问题
- [ ] `docs/UI_ACCEPTANCE_RESULT.md` 存在，截图路径正确
- [ ] `README.md` 版本号正确，截图链接有效
- [ ] `CHANGELOG.md` 已更新当前版本内容
- [ ] `PROJECT_STATE.md` 已更新当前阶段

## Git

- [ ] `git status` 干净，无未提交文件
- [ ] 已 `git push` 到 `main`
- [ ] commit message 清晰描述本阶段内容

## 截图脚本

- [ ] `scripts/screenshot_home.py` 可在 Streamlit 运行后生成首页 + 结果页截图
- [ ] 截图保存在 `docs/screenshots/home.png` 和 `docs/screenshots/result.png`

---

> 检查完成的人在此签名：__________ 日期：__________
