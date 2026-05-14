# 新对话接续提示词

你正在继续开发 A 股智能选股系统。请先阅读：
- PROJECT_STATE.md
- README.md
- app.py
- main.py
- strategies/selection.py
- validation/selection_validator.py
- validation/backtest_validator.py
- reports/generator.py

**最高目标**：小白可用的可视化 A 股选股系统。CLI 只是底层引擎和验收入口。

**已完成**：P0-P5.4（数据/选股/验证/复盘），P6.0-P6.1.1（Streamlit可视化/小白一键启动/轻量依赖）。

**下一步 P7**：产品化打磨

任务（不改功能代码，只做体验层）：
1. 界面体验优化：布局调整、loading 状态、无数据占位提示
2. 错误提示友好化：akshare 失败时给小白看得懂的提示，不崩溃
3. 数据覆盖可视化：在界面上直观展示数据覆盖范围（起始日~结束日），不用看日志

**禁止**：AI/qlib/实盘/后端分离/数据库/登录/复制评分逻辑/改 app.py 选股调用链以外的功能代码

验收：
```
.venv/bin/python -m py_compile app.py main.py strategies/selection.py validation/selection_validator.py validation/backtest_validator.py reports/generator.py
.venv/bin/python main.py select --universe static --limit 10 --top 5 --start 2024-01-01
.venv/bin/python main.py backtest-validate --selection reports/output/selection_latest.json --top 5
.venv/bin/python main.py report --selection reports/output/selection_latest.json
.venv/bin/streamlit run app.py --server.headless true --server.port 8501
git status --short --ignored
```

commit: P7产品化打磨: 界面优化/错误提示/数据覆盖可视化

路径: /Users/niuniu/projects/a-share-selection-system
GitHub: https://github.com/xiarantang/a-share-selection-system
