#!/usr/bin/env python3
"""P8.3-4 UI 验收脚本：确认 app.py 页面文本和最新选股结果中文化到位。
用法: python3 scripts/confirm_p83_ui.py
不启动 Streamlit，只静态检查源码文本 + JSON 数据。
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_PY = ROOT / "app.py"
LATEST_JSON = ROOT / "reports/output/selection_latest.json"

CHECKS_PASSED = 0
CHECKS_FAILED = 0


def check(name: str, ok: bool, detail: str = ""):
    global CHECKS_PASSED, CHECKS_FAILED
    if ok:
        CHECKS_PASSED += 1
        print(f"  ✅ {name}")
    else:
        CHECKS_FAILED += 1
        print(f"  ❌ {name}" + (f" — {detail}" if detail else ""))


# ─── 1. 静态文本检查（app.py 源码） ───────────────────────────
print("=" * 60)
print("1. app.py 静态文本检查")
print("=" * 60)

src = APP_PY.read_text()

check("首页引导文案", "选参数 → 开始选股 → 看结果" in src)
check("Top 3 候选速览标题", "Top 3 候选速览" in src)
check("技术指标详情折叠入口", "技术指标详情" in src)
check("免责声明", "仅供研究学习，不构成投资建议" in src)

# 决策中文标签
for tag in ["强观察", "观察", "中性", "回避"]:
    check(f"决策标签: {tag}", f'"{tag}"' in src)

# 风险中文标签
for tag in ["低风险", "中风险", "高风险"]:
    check(f"风险标签: {tag}", f'"{tag}"' in src)

# 置信度中文标签
for tag in ["高置信度", "中置信度", "低置信度"]:
    check(f"置信度标签: {tag}", f'"{tag}"' in src)

# 因子中文标签 + 图标
factor_labels = ["趋势", "动量", "量能", "风控", "数据质量", "形态"]
for fl in factor_labels:
    check(f"因子标签: {fl}", fl in src)

# 验证旧英文标签不在 UI 展示位置（标题和正文）
# 检查逐只详情标题不再直接用 raw decision/risk_level
has_raw_in_detail_title = (
    '{score}/100 {dec} {rl}' in src
    or '— {score}/100 {dec}' in src
)
check("逐只详情标题已用中文", not has_raw_in_detail_title,
      "标题仍使用 raw dec/rl 英文字段")

# 检查风险提示不再一律 st.error
check("风险分级着色(risk_alert)", "risk_alert(rl," in src)

# 检查友好日期区间
check("友好日期区间(friendly_date_range)", "friendly_date_range(" in src)

# 检查禁词不在 UI 正向文案
FORBIDDEN = ["买入", "卖出", "目标价", "收益预测", "建议买", "建议卖"]
for w in FORBIDDEN:
    # 只检查非注释、非免责声明的行
    lines_with = [l.strip() for l in src.splitlines() if w in l and not l.strip().startswith("#")]
    # 排除免责声明语境
    non_disclaimer = [l for l in lines_with if "免责" not in l and "禁止" not in l and "不是" not in l]
    check(f"禁词不在 UI 正向文案: {w}", len(non_disclaimer) == 0,
          f"出现在: {non_disclaimer[:2]}" if non_disclaimer else "")


# ─── 2. 运行时数据检查（最新选股 JSON） ────────────────────────
print()
print("=" * 60)
print("2. 最新选股 JSON 运行时数据检查")
print("=" * 60)

if not LATEST_JSON.exists():
    print("  ⚠️ selection_latest.json 不存在，跳过运行时检查")
    print("  提示: 请先运行 .venv/bin/python main.py select --universe static --limit 10 --top 5")
else:
    with open(LATEST_JSON) as f:
        data = json.load(f)

    top = data.get("top", [])
    check("Top 候选非空", len(top) > 0, f"top 长度: {len(top)}")

    if top:
        # 检查 JSON 底层字段仍是英文（映射只在 UI 展示层）
        first = top[0]
        dec_val = first.get("decision", "")
        rl_val = first.get("risk_level", "")
        conf_val = first.get("confidence", "")
        check("JSON decision 仍为英文", dec_val in ("strong_watch", "watch", "neutral", "avoid"),
              f"实际值: {dec_val}")
        check("JSON risk_level 仍为英文", rl_val in ("low", "medium", "high"),
              f"实际值: {rl_val}")
        check("JSON confidence 仍为英文", conf_val in ("high", "medium", "low"),
              f"实际值: {conf_val}")

        # 检查 explain 字段完整
        exp = first.get("explain", {})
        exp_fields = ["summary", "strengths", "weaknesses", "risk_note", "confidence_note"]
        missing = [k for k in exp_fields if k not in exp]
        check("explain 字段完整", len(missing) == 0, f"缺少: {missing}" if missing else "")

        # 检查因子得分
        fs = first.get("factor_scores", {})
        for fk in ["trend", "momentum", "volume", "risk", "data_quality", "pattern"]:
            check(f"因子得分 {fk} 存在", fk in fs, f"keys: {list(fs.keys())}")

        # 统计决策分布
        decisions = set(r.get("decision", "") for r in top)
        check("至少有 1 种决策类型", len(decisions) > 0, f"决策: {decisions}")

    # 检查禁词不在 JSON explain 中
    all_explain_text = ""
    for r in top:
        all_explain_text += str(r.get("explain", {}))
    forbidden_found = [w for w in FORBIDDEN if w in all_explain_text]
    check("JSON explain 无禁词", len(forbidden_found) == 0,
          f"发现: {forbidden_found}" if forbidden_found else "")


# ─── 3. 截图文件存在性检查 ─────────────────────────────────────
print()
print("=" * 60)
print("3. 截图文件检查")
print("=" * 60)

for name in ["home.png", "result.png"]:
    p = ROOT / "docs/screenshots" / name
    check(f"截图存在: {name}", p.exists() and p.stat().st_size > 1000,
          f"大小: {p.stat().st_size}" if p.exists() else "不存在")


# ─── 汇总 ─────────────────────────────────────────────────────
print()
print("=" * 60)
total = CHECKS_PASSED + CHECKS_FAILED
print(f"汇总: {CHECKS_PASSED}/{total} 通过")
if CHECKS_FAILED > 0:
    print(f"⚠️ {CHECKS_FAILED} 项未通过")
    sys.exit(1)
else:
    print("🎉 全部通过")
    sys.exit(0)
