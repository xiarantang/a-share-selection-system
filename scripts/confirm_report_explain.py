"""P8.2-2 报告 explain 验证"""
import sys
md = open("reports/output/report_latest.md").read()
checks = ["📝 解释", "✅ 加分", "📊 可靠性"]
forbidden = ["买入", "卖出", "目标价", "建议增持", "建议减持"]
ok = True
for kw in checks:
    if kw not in md:
        print(f"❌ 缺少: {kw}")
        ok = False
# 排除否定句式中的"收益预测"（如"不是收益预测"）
import re
for w in forbidden:
    if w in md:
        # 检查是否在否定上下文中
        neg = re.findall(rf"(?:不是|非|不构成)\s*{w}", md)
        if not neg:
            print(f"❌ 禁止词: {w}")
            ok = False
if ok:
    print("✅ 报告 explain 验证通过")
    idx = md.find("📝 解释:")
    if idx >= 0:
        print(md[idx:idx+120])
else:
    print("❌ 失败")
sys.exit(0 if ok else 1)
