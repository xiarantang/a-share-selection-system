"""
选股引擎：基于K线的基础因子评分模型
======================================
计算 MA/涨跌幅/成交量放大/MACD/RSI，输出满分100的评分。
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from loguru import logger

from data.fetcher import AShareDataFetcher


def _safe_float(val, default=0.0):
    try:
        v = float(val)
        return v if pd.notna(v) and np.isfinite(v) else default
    except (ValueError, TypeError):
        return default


def compute_factors(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "close" not in df.columns:
        return df
    close = df["close"].astype(float)
    volume = df["volume"].astype(float)

    df["MA5"] = close.rolling(5).mean()
    df["MA20"] = close.rolling(20).mean()
    df["MA60"] = close.rolling(60).mean()
    df["return_20d"] = close.pct_change(20) * 100
    df["return_60d"] = close.pct_change(60) * 100

    vol_ma5 = volume.rolling(5).mean()
    vol_ma20 = volume.rolling(20).mean()
    df["vol_ratio"] = vol_ma5 / (vol_ma20 + 1e-8)

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df["MACD_DIF"] = ema12 - ema26
    df["MACD_DEA"] = df["MACD_DIF"].ewm(span=9, adjust=False).mean()
    df["MACD_HIST"] = 2 * (df["MACD_DIF"] - df["MACD_DEA"])

    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta.where(delta < 0, 0.0))
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / (avg_loss + 1e-8)
    df["RSI14"] = 100 - (100 / (1 + rs))
    return df


def score_stock(df: pd.DataFrame) -> Tuple[float, List[str], List[str]]:
    if df.empty or len(df) < 60:
        return 0.0, ["数据不足(<60条)"], []

    latest = df.iloc[-1]
    reasons, risks = [], []
    score = 0.0

    ma5 = _safe_float(latest.get("MA5"))
    ma20 = _safe_float(latest.get("MA20"))
    ma60 = _safe_float(latest.get("MA60"))
    close = _safe_float(latest.get("close"))

    if ma5 > ma20 > ma60 > 0:
        score += 40
        reasons.append("多头排列 MA5>MA20>MA60")
    elif ma5 > ma20 > 0:
        score += 25
        reasons.append("MA5>MA20 未站上MA60")
    elif close > ma60 > 0:
        score += 15
        reasons.append("股价在MA60上方")
    else:
        score += 5
        risks.append(f"均线空头")

    ret20 = _safe_float(latest.get("return_20d"))
    ret60 = _safe_float(latest.get("return_60d"))
    if 2 < ret20 < 15:
        score += 15
        reasons.append(f"20日 +{ret20:.1f}%")
    elif 0 < ret20 <= 2:
        score += 10
    elif ret20 > 15:
        score += 5
        risks.append(f"20日涨幅过大 +{ret20:.1f}%")
    else:
        score += 5
        if ret20 < -5:
            risks.append(f"20日跌幅 {ret20:.1f}%")

    if ret60 > 0:
        score += 5
    else:
        risks.append(f"60日跌 {ret60:.1f}%")

    vol_ratio = _safe_float(latest.get("vol_ratio"), 1.0)
    if 1.2 < vol_ratio < 3.0:
        score += 15
        reasons.append(f"量能 {vol_ratio:.1f}x")
    elif 1.0 < vol_ratio <= 1.2:
        score += 10
    else:
        score += 5
        if vol_ratio < 0.8:
            risks.append(f"缩量 {vol_ratio:.1f}x")

    dif = _safe_float(latest.get("MACD_DIF"))
    dea = _safe_float(latest.get("MACD_DEA"))
    hist = _safe_float(latest.get("MACD_HIST"))
    if dif > dea and dif > 0:
        score += 15
        reasons.append("MACD零轴多头")
    elif dif > dea:
        score += 10
        reasons.append("MACD金叉")
    else:
        score += 2
        if hist < 0:
            risks.append("MACD死叉")

    rsi = _safe_float(latest.get("RSI14"), 50)
    if 40 < rsi < 70:
        score += 10
    elif rsi >= 70:
        score += 5
        risks.append(f"RSI={rsi:.0f}超买")
    elif rsi >= 30:
        score += 6
    else:
        score += 3
        risks.append(f"RSI={rsi:.0f}超卖")

    return round(score, 1), reasons, risks


class SelectionEngine:
    def __init__(self):
        self.fetcher = AShareDataFetcher()

    def select(self, symbols: List[str], start_date: str = "2024-01-01") -> List[Dict]:
        results = []
        for sym in symbols:
            df = self.fetcher.get_daily_kline(sym, start_date=start_date)
            if df is None or df.empty:
                results.append({"symbol": sym, "error": "数据获取失败", "score": 0, "rank": 0})
                continue
            source = self.fetcher._last_source
            rows = len(df)
            df = compute_factors(df)
            score, reasons, risks = score_stock(df)
            latest_close = _safe_float(df.iloc[-1].get("close"))
            actual_start = str(df.index[0])[:10] if len(df) > 0 else "N/A"
            actual_end = str(df.index[-1])[:10] if len(df) > 0 else "N/A"
            results.append({
                "symbol": sym, "score": score, "reasons": reasons, "risks": risks,
                "latest_close": round(latest_close, 2), "data_source": source,
                "rows": rows, "actual_start": actual_start, "actual_end": actual_end,
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        for i, r in enumerate(results):
            r["rank"] = i + 1
        return results

    def select_top(self, symbols: List[str], top: int = 10, start_date: str = "2024-01-01") -> List[Dict]:
        return self.select(symbols, start_date)[:top]
