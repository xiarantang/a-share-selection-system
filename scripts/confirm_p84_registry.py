#!/usr/bin/env python3
"""
P8.4-1 策略注册骨架验收脚本
============================
检查:
- 默认策略存在且包含所有必填字段
- get_default_strategy() 返回默认策略
- list_strategies() 包含默认策略
- get_strategy("missing") 返回 None
- register_strategy() 可注册禁用策略，enabled_only 过滤生效
- StrategyRegistry 兼容类: list_strategies / execute_strategy / run_all_strategies
- 源码不再包含遗留标记: PRIORITY_SCRIPTS / skills_dir / subprocess.run / SKILL.md
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PASS = 0
FAIL = 0


def check(label: str, condition: bool):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label}")


# ── 1. 模块级函数 ──────────────────────────────────────────────────
print("\n[1] 模块级注册 / 查询函数")

from strategies.registry import (  # noqa: E402
    DEFAULT_STRATEGY_ID,
    REQUIRED_FIELDS,
    STRATEGY_REGISTRY,
    get_default_strategy,
    get_strategy,
    list_strategies,
    register_strategy,
)

check("DEFAULT_STRATEGY_ID == 'default'", DEFAULT_STRATEGY_ID == "default")
check("REQUIRED_FIELDS 包含 7 个字段", len(REQUIRED_FIELDS) == 7)

# 默认策略存在且字段完整
default = get_strategy("default")
check("get_strategy('default') 不为 None", default is not None)
for f in REQUIRED_FIELDS:
    check(f"默认策略含字段 '{f}'", default is not None and f in default)

# get_default_strategy
ds = get_default_strategy()
check("get_default_strategy().id == 'default'", ds["id"] == "default")

# list_strategies 包含默认
enabled = list_strategies(enabled_only=True)
check("list_strategies() >= 1 条", len(enabled) >= 1)
check("list_strategies() 包含 default", any(s["id"] == "default" for s in enabled))

# get_strategy("missing") → None
check("get_strategy('missing') 返回 None", get_strategy("missing") is None)

# ── 2. 注册禁用策略 + enabled_only 过滤 ─────────────────────────────
print("\n[2] 注册禁用策略 + enabled_only 过滤")

register_strategy({
    "id": "test_disabled",
    "name": "测试禁用策略",
    "description": "仅用于验收",
    "suitable_scenario": "测试",
    "risk_reminder": "无",
    "enabled": False,
    "entry_function": "nowhere:None",
})

check("test_disabled 已注册", get_strategy("test_disabled") is not None)
check("test_disabled.enabled == False", get_strategy("test_disabled")["enabled"] is False)
check("list_strategies(enabled_only=True) 不含 test_disabled",
      not any(s["id"] == "test_disabled" for s in list_strategies(enabled_only=True)))
check("list_strategies(enabled_only=False) 含 test_disabled",
      any(s["id"] == "test_disabled" for s in list_strategies(enabled_only=False)))

# 清理测试数据
STRATEGY_REGISTRY.pop("test_disabled", None)

# ── 3. StrategyRegistry 兼容类 ─────────────────────────────────────
print("\n[3] StrategyRegistry 兼容类")

from strategies.registry import StrategyRegistry  # noqa: E402

reg = StrategyRegistry()
compat_list = reg.list_strategies()
check("StrategyRegistry().list_strategies() 非空", len(compat_list) > 0)

first = compat_list[0]
check("兼容记录含 'available'", "available" in first)
check("兼容记录含 'executable'", "executable" in first)
check("兼容记录含 'type'", "type" in first)
check("兼容记录 type == 'builtin'", first.get("type") == "builtin")

exec_r = reg.execute_strategy("default")
check("execute_strategy('default') success=True", exec_r.get("success") is True)

exec_miss = reg.execute_strategy("nonexistent")
check("execute_strategy('nonexistent') success=False", exec_miss.get("success") is False)

results, stats = reg.run_all_strategies()
check("run_all_strategies 返回 (results, stats)", isinstance(results, dict) and isinstance(stats, dict))
check("stats['failed'] == 0", stats.get("failed", -1) == 0)
check("stats['executed'] >= 1", stats.get("executed", 0) >= 1)

# ── 4. 遗留标记检查 ────────────────────────────────────────────────
print("\n[4] 遗留标记检查")

src = (PROJECT_ROOT / "strategies" / "registry.py").read_text()
legacy_markers = ["PRIORITY_SCRIPTS", "skills_dir", "subprocess.run", "SKILL.md"]
for marker in legacy_markers:
    # 排除注释或字符串中的提及（只匹配实际使用而非文档说明）
    # 但按需求，完全不应包含这些标记
    check(f"源码不含 '{marker}'", marker not in src)

# ── 汇总 ──────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"验收结果: {PASS} PASS / {FAIL} FAIL")
if FAIL:
    print("P8.4-1 验收未通过")
    sys.exit(1)
else:
    print("P8.4-1 验收通过")
    sys.exit(0)
