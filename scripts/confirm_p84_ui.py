#!/usr/bin/env python3
"""
P8.4-3 UI 策略选择器验收脚本
============================
检查 app.py 静态文本 + 运行时数据：
1. 导入 DEFAULT_STRATEGY_ID / get_strategy / list_strategies
2. run_selection 支持 strategy_id 参数
3. 使用 list_strategies(enabled_only=True) 渲染策略选择器
4. 选股调用传入 strategy_id
5. 返回数据包含 strategy_id 和 strategy
6. 不包含 execute_strategy / importlib / entry_function 动态执行
7. 不包含投资建议禁词（允许免责声明中的"不构成投资建议"/"不是收益预测"）
8. latest JSON 顶层包含 strategy_id / strategy
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PASS = 0
FAIL = 0

APP_PY = PROJECT_ROOT / "app.py"
LATEST_JSON = PROJECT_ROOT / "reports" / "output" / "selection_latest.json"

# 禁词：在 app.py 正向文案中不应出现
FORBIDDEN_POSITIVE = ["推荐买入", "推荐卖出", "目标价", "预期收益", "保证收益"]

# 允许出现的免责声明关键词（不应被误报）
ALLOWED_DISCLAIMER = ["不构成投资建议", "不是收益预测", "不代表未来收益"]


def check(label: str, condition: bool):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label}")


app_text = APP_PY.read_text()

# ── 1. 导入检查 ──────────────────────────────────────────────────
print("\n[1] 导入检查")

check("导入 DEFAULT_STRATEGY_ID", "DEFAULT_STRATEGY_ID" in app_text)
check("导入 get_strategy", "get_strategy" in app_text)
check("导入 list_strategies", "list_strategies" in app_text)
check(
    "from strategies.registry 导入",
    "from strategies.registry import" in app_text
    and "DEFAULT_STRATEGY_ID" in app_text,
)

# ── 2. run_selection 签名 ───────────────────────────────────────
print("\n[2] run_selection strategy_id 参数")

# 找函数定义
match = re.search(r"def run_selection\([^)]*\)", app_text)
check("run_selection 存在", match is not None)
if match:
    sig = match.group(0)
    check("run_selection 有 strategy_id 参数", "strategy_id" in sig)
    check("run_selection 默认值 DEFAULT_STRATEGY_ID", "DEFAULT_STRATEGY_ID" in sig)

# ── 3. 策略校验逻辑 ─────────────────────────────────────────────
print("\n[3] 策略校验逻辑")

check("使用 get_strategy(strategy_id) 校验", "get_strategy(strategy_id)" in app_text)
check("无效策略抛出 ValueError", "ValueError" in app_text)

# ── 4. list_strategies(enabled_only=True) 策略选择器 ────────────
print("\n[4] 策略选择器渲染")

check(
    "使用 list_strategies(enabled_only=True)",
    "list_strategies(enabled_only=True)" in app_text,
)
check("策略选择器 st.selectbox", 'st.selectbox' in app_text and 'strategy' in app_text.split('st.selectbox')[-1].split('st.selectbox')[0] if app_text.count('st.selectbox') > 1 else '"策略"' in app_text)

# 更直接地检查
check("策略选择器显示 name", "strategy_options" in app_text or "s[\"name\"]" in app_text)

# ── 5. 选股调用传入 strategy_id ──────────────────────────────────
print("\n[5] 选股调用传入 strategy_id")

check(
    "run_selection 调用包含 strategy_id",
    "strategy_id=selected_strategy" in app_text,
)
check("last_strategy 写入 session_state", "st.session_state.last_strategy" in app_text)

# ── 6. 返回数据包含 strategy_id 和 strategy ──────────────────────
print("\n[6] 返回数据字段")

check('返回数据含 "strategy_id"', '"strategy_id"' in app_text)
check('返回数据含 "strategy"', '"strategy"' in app_text)
check("strategy_info 包含 id/name/description", "strategy_info" in app_text)
check("strategy_info 包含 suitable_scenario", "suitable_scenario" in app_text)
check("strategy_info 包含 risk_reminder", "risk_reminder" in app_text)

# ── 7. 不包含动态执行 ────────────────────────────────────────────
print("\n[7] 无动态执行")

check("无 execute_strategy", "execute_strategy" not in app_text)
check("无 importlib", "importlib" not in app_text)
check("无 entry_function", "entry_function" not in app_text)

# ── 8. 无投资建议禁词 ────────────────────────────────────────────
print("\n[8] 无投资建议禁词")

for word in FORBIDDEN_POSITIVE:
    check(f"无禁词 '{word}'", word not in app_text)

# 免责声明中允许的措辞应存在
check("免责声明含'不构成投资建议'", "不构成投资建议" in app_text)

# ── 9. 结果页策略展示 ────────────────────────────────────────────
print("\n[9] 结果页策略展示")

check("展示当前策略名称", "当前策略" in app_text)
check("展示适用场景", "适用场景" in app_text)
check("展示风险提醒", "risk_reminder" in app_text)

# ── 10. latest JSON 顶层策略字段 ──────────────────────────────────
print("\n[10] latest JSON 策略字段")

if LATEST_JSON.exists():
    with open(LATEST_JSON) as f:
        data = json.load(f)
    check("JSON 含 strategy_id", "strategy_id" in data)
    check("JSON strategy_id == 'default'", data.get("strategy_id") == "default")
    check("JSON 含 strategy dict", isinstance(data.get("strategy"), dict))
    strategy = data.get("strategy", {})
    check("JSON strategy.id == 'default'", strategy.get("id") == "default")
    check("JSON strategy.name 非空", len(strategy.get("name", "")) > 0)
else:
    check("latest JSON 存在（跳过 JSON 检查）", False)
    print("  提示: 请先运行 select 以生成 selection_latest.json")

# ── 汇总 ──────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"验收结果: {PASS} PASS / {FAIL} FAIL")
if FAIL:
    print("P8.4-3 UI 策略选择器验收未通过")
    sys.exit(1)
else:
    print("P8.4-3 UI 策略选择器验收通过")
    sys.exit(0)
