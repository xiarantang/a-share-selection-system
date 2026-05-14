# 新对话接续提示词

你正在继续开发 A 股智能选股系统。请先阅读：
- PROJECT_STATE.md
- README.md
- main.py
- strategies/selection.py
- validation/selection_validator.py
- validation/backtest_validator.py
- reports/generator.py

**最高目标**：小白可用的可视化 A 股选股系统。CLI 只是底层引擎。

**已完成**：P0-P5.4（数据/选股/验证/复盘），docs产品目标。

**下一步 P6.0**：Streamlit 本地 UI 第一版

任务：
- 新增 app.py
- 界面选股票池/limit/top/start
- 一键选股/验证/复盘/报告
- 展示候选表格/验证摘要/历史复盘/报告
- 提示"仅供研究学习"

**禁止**：AI/qlib/实盘/后端分离/数据库/登录/复制评分逻辑

验收：
```
python3 -m py_compile app.py main.py strategies/selection.py validation/selection_validator.py validation/backtest_validator.py reports/generator.py
python3 main.py select --universe static --limit 10 --top 5 --start 2024-01-01
python3 main.py backtest-validate --selection reports/output/selection_latest.json --top 5
python3 main.py report --selection reports/output/selection_latest.json
git status --short --ignored
```

commit: P6.0可视化界面: Streamlit本地UI/小白入口/README使用说明

路径: /Users/niuniu/projects/a-share-selection-system
GitHub: https://github.com/xiarantang/a-share-selection-system
