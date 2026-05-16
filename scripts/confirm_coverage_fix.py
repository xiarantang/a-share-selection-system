"""P8.1-3 coverage_warning 修正验证。用法: .venv/bin/python scripts/confirm_coverage_fix.py"""
import sys
from datetime import datetime

sys.path.insert(0, ".")
from data.fetcher import AShareDataFetcher


def main():
    symbols = ["600519", "000001", "000858", "600036", "601398"]
    f = AShareDataFetcher()
    ok = 0
    for sym in symbols:
        df = f.get_daily_kline(sym, start_date="2024-01-01")
        src = f._last_source
        rows = len(df) if df is not None else 0
        if rows == 0:
            print(f"{sym} ❌ 获取失败")
            continue
        ast = str(df.index[0])[:10]
        # 新逻辑
        if ast == "N/A":
            has_cov = True
        elif rows >= 250 and src in ("akshare", "baostock"):
            try:
                ast_dt = datetime.strptime(ast, "%Y-%m-%d")
                req_dt = datetime.strptime("2024-01-01", "%Y-%m-%d")
                has_cov = (req_dt - ast_dt).days > 10
            except Exception:
                has_cov = False
        else:
            has_cov = ast > "2024-01-01"
        status = "⚠️ 误判" if (rows >= 250 and has_cov) else ("✅" if not has_cov else "⚠️")
        print(f"{sym} {src:<14} {rows}条 {ast} {status}")
        if rows >= 250 and not has_cov:
            ok += 1
    print(f"\n{ok}/{len(symbols)} 只达标且无覆盖不足")
    sys.exit(0 if ok == len(symbols) else 1)


if __name__ == "__main__":
    main()
