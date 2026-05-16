"""P8.1-1 baostock 最小实验 — 测试 10 只股票历史日 K 数据获取。

用法:
    .venv/bin/pip install -r requirements-experimental.txt
    .venv/bin/python scripts/test_baostock.py
"""
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UNIVERSE_PATH = PROJECT_ROOT / "data" / "static_universe.json"
OUTPUT_PATH = PROJECT_ROOT / "docs" / "P8_1_BAOSTOCK_EXPERIMENT.md"

with open(UNIVERSE_PATH) as f:
    universe = json.load(f)
test_stocks = universe[:10]

try:
    import baostock as bs
except ImportError:
    print("请先安装: .venv/bin/pip install -r requirements-experimental.txt")
    sys.exit(1)


def symbol_to_bs(sym):
    return f"sz.{sym}" if sym.startswith(("0","3")) else f"sh.{sym}"


def fetch_one(sym, start, end):
    code = symbol_to_bs(sym)
    fields = "date,open,high,low,close,volume,amount"
    try:
        rs = bs.query_history_k_data_plus(code, fields, start_date=start, end_date=end, frequency="d", adjustflag="2")
        if rs.error_code != "0":
            return {"success": False, "reason": f"baostock {rs.error_code}: {rs.error_msg}"}
        rows = []
        while rs.next():
            rows.append(rs.get_row_data())
        if not rows:
            return {"success": False, "reason": "0 条数据"}
        return {"success": True, "rows": len(rows), "start_date": rows[0][0], "end_date": rows[-1][0]}
    except Exception as e:
        return {"success": False, "reason": str(e)[:120]}


def main():
    start = "2024-01-01"
    end = time.strftime("%Y-%m-%d")
    results = []

    print("=" * 60)
    print("  P8.1-1 baostock 实验: 10只, 目标 >=8 只 250+条")
    print("=" * 60)

    lg = bs.login()
    if lg.error_code != "0":
        print(f"登录失败: {lg.error_msg}")
        sys.exit(1)
    print("登录成功")

    ok250 = 0
    ok_total = 0

    for i, st in enumerate(test_stocks):
        sym, name = st["symbol"], st.get("name", "")
        print(f"[{i+1}/10] {sym} {name}", end=" ", flush=True)
        r = fetch_one(sym, start, end)
        r["symbol"] = sym
        r["name"] = name
        if r["success"]:
            ok_total += 1
            is250 = r["rows"] >= 250
            if is250:
                ok250 += 1
            print(f"{'✅' if is250 else '⚠️'} {r['rows']}条 [{r['start_date']}~{r['end_date']}]")
        else:
            print(f"❌ {r['reason']}")
        results.append(r)
        time.sleep(0.3)

    bs.logout()
    print(f"\n结果: {ok_total}/10 成功, {ok250}/10 达250+条")

    # 写报告
    md = f"""# P8.1-1 baostock 最小实验结果

> 日期：{time.strftime('%Y-%m-%d')} | 方式：baostock 匿名登录/前复权 | 区间：{start}~{end}

## 总体

| 指标 | 值 |
|------|----|
| 测试数 | 10 |
| 成功 | {ok_total} |
| >=250条 | {ok250} |
| 达标率 | {ok250 * 10}% |

## 逐只

| # | 代码 | 名称 | 结果 | 条数 | 起止 | 备注 |
|---|------|------|------|------|------|------|
"""
    for i, r in enumerate(results):
        sym, name = r["symbol"], r["name"]
        if r["success"]:
            ok = "✅" if r["rows"] >= 250 else "⚠️"
            md += f"| {i+1} | {sym} | {name} | {ok} | {r['rows']} | {r['start_date']}~{r['end_date']} | {'达标' if r['rows']>=250 else '不足250'} |\n"
        else:
            md += f"| {i+1} | {sym} | {name} | ❌ | - | - | {r['reason']} |\n"

    if ok250 >= 8:
        md += "\n## 结论\n\n✅ 通过。建议进入 P8.1-2 正式接入 data/fetcher.py。\n"
    elif ok250 >= 5:
        md += "\n## 结论\n\n🟡 部分通过。建议 baostock + efinance 双接入。\n"
    else:
        md += "\n## 结论\n\n❌ 不通过。建议跳过 baostock，直接实验 efinance。\n"

    md += "\n## 下一步\n- 若通过 → P8.1-2 接入 fetcher\n- 若失败 → P8.1-3 efinance 实验\n"

    OUTPUT_PATH.write_text(md)
    print(f"报告: {OUTPUT_PATH}")
    sys.exit(0 if ok250 >= 8 else 1)


if __name__ == "__main__":
    main()
