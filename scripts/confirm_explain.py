"""P8.2-1 explain 验证。用法: .venv/bin/python scripts/confirm_explain.py"""
import json, sys

with open("reports/output/selection_latest.json") as f:
    d = json.load(f)

top = d.get("top", [])
REQUIRED = ["summary", "strengths", "weaknesses", "risk_note", "confidence_note"]
FORBIDDEN = ["买入", "卖出", "目标价", "收益预测"]

ok = 0
for r in top[:5]:
    exp = r.get("explain", {})
    missing = [k for k in REQUIRED if k not in exp]
    fb = [w for w in FORBIDDEN if w in str(exp)]
    if missing:
        print(f"❌ #{r['rank']} {r['symbol']} 缺少: {missing}")
    elif fb:
        print(f"❌ #{r['rank']} {r['symbol']} 禁止词: {fb}")
    else:
        print(f"✅ #{r['rank']} {r['symbol']} {r['score']}分 {repr(exp['summary'][:60])}")
        ok += 1

print(f"\n{ok}/{min(5,len(top))} 条通过")
sys.exit(0 if ok == min(5, len(top)) else 1)
