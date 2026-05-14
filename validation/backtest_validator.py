"""历史窗口复盘验证。对 top 候选做 in-sample 验证，不预测未来。"""
from collections import Counter

def forward_check(candidate, df, holding_days=10):
    if df is None or df.empty or len(df) < holding_days + 5:
        return {"symbol": candidate.get("symbol","?"), "skipped": True, "skipped_reason": "数据不足"}
    split = max(len(df) - holding_days, len(df)//2)
    valid_df = df.iloc[split:]
    if len(valid_df) < 3:
        return {"symbol": candidate.get("symbol","?"), "skipped": True, "skipped_reason": "验证区间太短"}
    sp = float(valid_df.iloc[0].get("close",0))
    ep = float(valid_df.iloc[-1].get("close",0))
    if sp <= 0:
        return {"symbol": candidate.get("symbol","?"), "skipped": True, "skipped_reason": "价格异常"}
    fwd_ret = (ep - sp) / sp * 100
    lo = valid_df.get("low", valid_df.get("close")).astype(float)
    rm = lo.expanding().max()
    dds = (lo - rm) / (rm + 1e-8) * 100
    max_dd = min(dds) if len(dds) > 0 else 0
    vol = valid_df.get("close").pct_change().std() * 100 if len(valid_df) > 1 else 0
    label = "win" if fwd_ret > 2 else "flat" if fwd_ret > -2 else "loss"
    return {
        "symbol": candidate.get("symbol","?"),
        "name": candidate.get("name",""),
        "sector": candidate.get("sector",""),
        "score": candidate.get("score",0),
        "decision": candidate.get("decision","?"),
        "confidence": candidate.get("confidence","?"),
        "start_date": str(valid_df.index[0])[:10] if len(valid_df)>0 else "?",
        "end_date": str(valid_df.index[-1])[:10] if len(valid_df)>0 else "?",
        "holding_days": len(valid_df),
        "start_price": round(sp,2),
        "end_price": round(ep,2),
        "forward_return_pct": round(fwd_ret,2),
        "max_drawdown_pct": round(max_dd,2),
        "volatility_pct": round(vol,2),
        "result_label": label,
        "skipped": False,
    }

def run_backtest_validation(data, top=10, fetcher=None):
    candidates = data.get("top") or data.get("results") or []
    if not candidates: return [], {"warnings":["无候选数据"]}
    if fetcher is None:
        from data.fetcher import AShareDataFetcher
        fetcher = AShareDataFetcher()
    req_start = data.get("requested_start", "2024-01-01")
    results = []
    for c in candidates[:top]:
        if c.get("error"):
            results.append({"symbol":c.get("symbol","?"),"skipped":True,"skipped_reason":"获取失败"})
            continue
        df = fetcher.get_daily_kline(c["symbol"], start_date=req_start)
        results.append(forward_check(c, df))
    skipped = [r for r in results if r.get("skipped")]
    done = [r for r in results if not r.get("skipped")]
    labels = Counter(r.get("result_label","?") for r in done)
    returns = [r.get("forward_return_pct",0) for r in done]
    dds = [r.get("max_drawdown_pct",0) for r in done]
    summary = {
        "total_checked": len(results),
        "skipped": len(skipped),
        "win_count": labels.get("win",0),
        "flat_count": labels.get("flat",0),
        "loss_count": labels.get("loss",0),
        "avg_forward_return_pct": round(sum(returns)/len(returns),2) if returns else 0,
        "avg_max_drawdown_pct": round(sum(dds)/len(dds),2) if dds else 0,
        "best": max(returns) if returns else 0,
        "worst": min(returns) if returns else 0,
        "warnings": [],
    }
    if len(done) == 0:
        summary["warnings"].append(f"全部{len(skipped)}只跳过验证")
    elif len(skipped) > 0:
        summary["warnings"].append(f"{len(skipped)}只跳过")
    return results, summary
