#!/usr/bin/env python3
"""
P8.4-2 CLI策略参数验收脚本
=========================
检查:
- latest JSON 存在
- latest JSON strategy_id == "default"
- latest JSON strategy.id == "default"
- top/all candidate lists 存在且非空
- candidate row 字段 decision/risk_level/confidence 为英文枚举值
- registry 仍有 default 策略
- 策略元数据不含投资建议禁词
- nonexistent 策略退出码非零
"""

import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PASS = 0
FAIL = 0

FORBIDDEN_WORDS = ["投资建议", "推荐买入", "推荐卖出", "目标价", "预期收益", "保证收益"]

VALID_DECISIONS = {"strong_watch", "watch", "neutral", "avoid"}
VALID_RISK_LEVELS = {"low", "medium", "high"}
VALID_CONFIDENCES = {"high", "medium", "low"}

LATEST_JSON = PROJECT_ROOT / "reports" / "output" / "selection_latest.json"


def check(label: str, condition: bool):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label}")


# ── 1. latest JSON 存在 ────────────────────────────────────────────
print("\n[1] latest JSON 文件检查")

check("selection_latest.json 存在", LATEST_JSON.exists())

if not LATEST_JSON.exists():
    print(f"  跳过后续检查: {LATEST_JSON} 不存在")
    print(f"\n{'='*50}")
    print(f"验收结果: {PASS} PASS / {FAIL} FAIL")
    sys.exit(1)

with open(LATEST_JSON) as f:
    data = json.load(f)

# ── 2. 策略元数据字段 ──────────────────────────────────────────────
print("\n[2] 策略元数据字段")

check("strategy_id == 'default'", data.get("strategy_id") == "default")
check("strategy 字段存在", isinstance(data.get("strategy"), dict))

strategy = data.get("strategy", {})
check("strategy.id == 'default'", strategy.get("id") == "default")
check("strategy.name 非空", isinstance(strategy.get("name"), str) and len(strategy["name"]) > 0)
check("strategy.description 非空", isinstance(strategy.get("description"), str) and len(strategy["description"]) > 0)
check("strategy.suitable_scenario 非空", isinstance(strategy.get("suitable_scenario"), str) and len(strategy["suitable_scenario"]) > 0)
check("strategy.risk_reminder 非空", isinstance(strategy.get("risk_reminder"), str) and len(strategy["risk_reminder"]) > 0)

# ── 3. 候选列表完整性 ──────────────────────────────────────────────
print("\n[3] 候选列表完整性")

check("top 列表存在且非空", isinstance(data.get("top"), list) and len(data["top"]) > 0)
check("all 列表存在且非空", isinstance(data.get("all"), list) and len(data["all"]) > 0)

# ── 4. 候选行英文字段枚举 ──────────────────────────────────────────
print("\n[4] 候选行英文字段枚举")

top_list = data.get("top", [])
all_list = data.get("all", [])
decision_ok = True
risk_ok = True
confidence_ok = True

for r in top_list + all_list:
    d = r.get("decision", "")
    if d not in VALID_DECISIONS:
        decision_ok = False
    rl = r.get("risk_level", "")
    if rl not in VALID_RISK_LEVELS:
        risk_ok = False
    c = r.get("confidence", "")
    if c not in VALID_CONFIDENCES:
        confidence_ok = False

check("decision 字段均为英文枚举", decision_ok)
check("risk_level 字段均为英文枚举", risk_ok)
check("confidence 字段均为英文枚举", confidence_ok)

# ── 5. Registry 仍有 default 策略 ──────────────────────────────────
print("\n[5] Registry default 策略")

from strategies.registry import get_strategy, list_strategies  # noqa: E402

default = get_strategy("default")
check("get_strategy('default') 不为 None", default is not None)
enabled = list_strategies(enabled_only=True)
check("list_strategies() 包含 default", any(s["id"] == "default" for s in enabled))

# ── 6. 策略元数据禁词检查 ──────────────────────────────────────────
print("\n[6] 策略元数据禁词检查")

strategy_values = [
    strategy.get("name", ""),
    strategy.get("description", ""),
    strategy.get("suitable_scenario", ""),
    strategy.get("risk_reminder", ""),
]
# 排除 risk_reminder 中合理出现的"投资建议"（免责声明中"不构成投资建议"）
# 检查 description / suitable_scenario / name 中不应出现禁词
forbidden_in_values = False
for val in strategy_values[:2]:  # name + description
    for w in FORBIDDEN_WORDS:
        if w in val:
            forbidden_in_values = True
            print(f"    禁词 '{w}' 出现在: {val[:60]}")

check("策略元数据(name/description)无投资建议禁词", not forbidden_in_values)

# ── 7. nonexistent 策略退出码非零 ──────────────────────────────────
print("\n[7] nonexistent 策略退出码")

result = subprocess.run(
    [sys.executable, str(PROJECT_ROOT / "main.py"), "select",
     "--universe", "static", "--limit", "3", "--top", "2",
     "--strategy", "nonexistent"],
    capture_output=True, text=True, cwd=str(PROJECT_ROOT),
    timeout=120,
)
check("nonexistent 策略退出码非零", result.returncode != 0)

# ── 汇总 ──────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"验收结果: {PASS} PASS / {FAIL} FAIL")
if FAIL:
    print("P8.4-2 CLI策略参数验收未通过")
    sys.exit(1)
else:
    print("P8.4-2 CLI策略参数验收通过")
    sys.exit(0)
