#!/usr/bin/env python3
"""
P8.4-4 / P8.4-4.1 文档验收脚本
==================
检查:
1. README.md 包含「默认规则策略」、「--strategy default」、「不传」等同/默认策略说明
2. docs/USER_GUIDE.md 包含「策略」和「默认规则策略」
3. docs/P8_4_STRATEGY_MANAGEMENT_DESIGN.md 不再包含误导表述「调用对应入口函数（当前只有 default）」
4. PROJECT_STATE.md 包含 P8.4-4 完成和 P8.4 阶段完成
5. README.md / docs/USER_GUIDE.md 不含旧说法「四步引导|三步引导|两步核心」
6. 不新增正向投资建议措辞（允许免责声明中的「不构成投资建议」「不是收益预测」）
7. docs/P8_ROADMAP.md 路线图一致性：不含 multi-factor-v1、含 default、含 P8.5-0 决策评审门
8. PROJECT_STATE.md 含 P8.4-4.1 路线图一致性收口记录
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0

README = PROJECT_ROOT / "README.md"
USER_GUIDE = PROJECT_ROOT / "docs" / "USER_GUIDE.md"
DESIGN_DOC = PROJECT_ROOT / "docs" / "P8_4_STRATEGY_MANAGEMENT_DESIGN.md"
PROJECT_STATE = PROJECT_ROOT / "PROJECT_STATE.md"

# 正向投资建议禁词（不应出现在非免责声明上下文中）
FORBIDDEN_POSITIVE = ["推荐买入", "推荐卖出", "目标价", "预期收益", "保证收益"]

# 允许的免责声明措辞（不应被误报）
ALLOWED_DISCLAIMER = ["不构成投资建议", "不是收益预测", "不代表未来收益"]


def check(label: str, condition: bool):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS  {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label}")


def read_file(path: Path) -> str:
    if not path.exists():
        print(f"  ERROR 文件不存在: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def has_forbidden_positive(text: str, path_label: str):
    """检查文本中是否包含正向投资建议禁词（排除免责声明上下文）。"""
    for word in FORBIDDEN_POSITIVE:
        if word in text:
            check(f"{path_label} 无禁词 '{word}'", False)
        else:
            check(f"{path_label} 无禁词 '{word}'", True)


# ── 1. README.md 检查 ──────────────────────────────────────────────
print("\n[1] README.md 策略说明")

readme_text = read_file(README)
check("README.md 存在", len(readme_text) > 0)

check("README 含「默认规则策略」", "默认规则策略" in readme_text)
check("README 含「--strategy default」", "--strategy default" in readme_text)
check("README 含「不传」等同/默认策略说明", "不传" in readme_text and "默认策略" in readme_text)
check("README 含策略管理能力条目", "策略管理" in readme_text or "策略选择" in readme_text)
check("README 侧栏描述含「策略」", "策略" in readme_text.split("左侧栏")[1].split("点击")[0] if "左侧栏" in readme_text else False)

# ── 2. USER_GUIDE.md 检查 ──────────────────────────────────────────
print("\n[2] USER_GUIDE.md 策略参数")

guide_text = read_file(USER_GUIDE)
check("USER_GUIDE 存在", len(guide_text) > 0)

check("USER_GUIDE 含「策略」", "策略" in guide_text)
check("USER_GUIDE 含「默认规则策略」", "默认规则策略" in guide_text)
check("USER_GUIDE 含策略说明（不改变评分公式）", "不改变评分公式" in guide_text)
check("USER_GUIDE 结果区含策略/适用场景/风险提醒说明", "适用场景" in guide_text or "风险提醒" in guide_text)

# ── 3. P8_4 设计文档误导表述检查 ────────────────────────────────────
print("\n[3] P8_4 设计文档误导表述")

design_text = read_file(DESIGN_DOC)
check("设计文档存在", len(design_text) > 0)

check("无误导表述「调用对应入口函数（当前只有 default）」",
      "调用对应入口函数（当前只有 default）" not in design_text)
check("P8.4-1 标注完成", "P8.4-1" in design_text and "✅" in design_text.split("P8.4-1")[1][:20] if "P8.4-1" in design_text else False)
check("P8.4-2 标注完成", "P8.4-2" in design_text and "✅" in design_text.split("P8.4-2")[1][:20] if "P8.4-2" in design_text else False)
check("P8.4-3 标注完成", "P8.4-3" in design_text and "✅" in design_text.split("P8.4-3")[1][:20] if "P8.4-3" in design_text else False)
check("P8.4-4 标注完成", "P8.4-4" in design_text and "✅" in design_text.split("P8.4-4")[1][:20] if "P8.4-4" in design_text else False)

# ── 4. PROJECT_STATE.md 检查 ────────────────────────────────────────
print("\n[4] PROJECT_STATE.md 完成状态")

state_text = read_file(PROJECT_STATE)
check("PROJECT_STATE 存在", len(state_text) > 0)

check("PROJECT_STATE 含 P8.4-4 完成", "P8.4-4" in state_text)
check("PROJECT_STATE 含 P8.4 阶段完成", "P8.4 策略管理阶段已完成" in state_text)

# ── 5. 旧说法检查 ──────────────────────────────────────────────────
print("\n[5] 无旧说法残留")

old_patterns = ["四步引导", "三步引导", "两步核心", "四步完成选股", "三步完成选股", "两步完成选股"]
for pattern in old_patterns:
    check(f"README 无旧说法「{pattern}」", pattern not in readme_text)
    check(f"USER_GUIDE 无旧说法「{pattern}」", pattern not in guide_text)

# ── 6. 禁词检查 ────────────────────────────────────────────────────
print("\n[6] 无正向投资建议禁词")

has_forbidden_positive(readme_text, "README")
has_forbidden_positive(guide_text, "USER_GUIDE")

# 免责声明中允许的措辞应存在
check("README 含免责声明「不构成投资建议」", "不构成投资建议" in readme_text)
check("USER_GUIDE 含免责声明「不构成投资建议」", "不构成投资建议" in guide_text)

# ── 7. P8_ROADMAP 一致性检查 ──────────────────────────────────────
print("\n[7] P8_ROADMAP 路线图一致性")

ROADMAP = PROJECT_ROOT / "docs" / "P8_ROADMAP.md"
roadmap_text = read_file(ROADMAP)
check("P8_ROADMAP 存在", len(roadmap_text) > 0)

check("P8_ROADMAP 不含旧策略 ID「multi-factor-v1」", "multi-factor-v1" not in roadmap_text)
check("P8_ROADMAP 含正确策略 ID「default」", "default" in roadmap_text)
check("P8_ROADMAP 含「P8.5-0」决策评审门", "P8.5-0" in roadmap_text)
check("P8_ROADMAP 含「决策评审」", "决策评审" in roadmap_text)
check("P8_ROADMAP 不把「报告策略名称和版本」作为已完成验收",
      "报告策略名称和版本" not in roadmap_text and "报告里能看到策略名称和版本" not in roadmap_text)

# ── 8. PROJECT_STATE P8.4-4.1 检查 ────────────────────────────────
print("\n[8] PROJECT_STATE P8.4-4.1 收口")

check("PROJECT_STATE 含 P8.4-4.1", "P8.4-4.1" in state_text)
check("PROJECT_STATE 含路线图一致性收口", "路线图一致性收口" in state_text)
check("PROJECT_STATE 含 P8.5-0 下一步建议", "P8.5-0" in state_text)

# ── 汇总 ──────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"验收结果: {PASS} PASS / {FAIL} FAIL")
if FAIL:
    print("P8.4-4 文档验收未通过")
    sys.exit(1)
else:
    print("P8.4-4 文档验收通过")
    sys.exit(0)
