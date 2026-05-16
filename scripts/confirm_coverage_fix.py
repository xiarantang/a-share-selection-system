"""P8.1-3.1 coverage 验证 — 单元3反例 + 集成5只。用法: .venv/bin/python scripts/confirm_coverage_fix.py"""
import sys
sys.path.insert(0, ".")
from strategies.selection import _has_coverage_warning
from data.fetcher import AShareDataFetcher

def test_unit():
    print("=" * 50)
    print("  单元: _has_coverage_warning()")
    print("=" * 50)
    ok = True
    # 反例1: 570条/baostock/晚1天 → False
    r1 = _has_coverage_warning(570, "baostock", "2024-01-02", "2024-01-01")
    p1 = (r1 is False)
    print(f"  {'✅' if p1 else '❌'} 570/bao/晚1天 => {r1} (预期False)")
    # 反例2: 570条/baostock/晚31天 → True
    r2 = _has_coverage_warning(570, "baostock", "2024-02-01", "2024-01-01")
    p2 = (r2 is True)
    print(f"  {'✅' if p2 else '❌'} 570/bao/晚31天 => {r2} (预期True)")
    # 反例3: 120条/skill_fallback → True
    r3 = _has_coverage_warning(120, "skill_fallback", "2025-11-13", "2024-01-01")
    p3 = (r3 is True)
    print(f"  {'✅' if p3 else '❌'} 120/sf => {r3} (预期True)")
    ok = p1 and p2 and p3
    print(f"  单元: {'✅ PASS' if ok else '❌ FAIL'}")
    return ok

def test_integration():
    print(f"\n{'=' * 50}")
    print("  集成: 5只真实baostock")
    print("=" * 50)
    f = AShareDataFetcher()
    ok = 0
    for sym in ["600519","000001","000858","600036","601398"]:
        df = f.get_daily_kline(sym, start_date="2024-01-01")
        src, rows = f._last_source, len(df) if df is not None else 0
        ast = str(df.index[0])[:10] if rows>0 else "N/A"
        cov = _has_coverage_warning(rows, src, ast, "2024-01-01")
        s = "⚠️" if cov else "✅"
        print(f"  {s} {sym} {src} {rows}条 {ast} cov={cov}")
        if rows>=250 and not cov: ok+=1
    print(f"  {ok}/5 达标无覆盖")
    return ok==5

if __name__ == "__main__":
    u = test_unit()
    i = test_integration()
    print(f"\n{'✅ 全通过' if (u and i) else '❌ 有失败'}")
    sys.exit(0 if (u and i) else 1)
