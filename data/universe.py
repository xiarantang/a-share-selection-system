"""
股票池模块 v0.2
================
支持 manual / sample / static / hs300 / top_amount，返回完整 metadata。
"""

import json
import os
from typing import Dict, List, Optional

import akshare as ak
from loguru import logger

SAMPLE_SYMBOLS = ["600519", "000001", "300750"]
_STATIC_CACHE = None


def _load_static():
    global _STATIC_CACHE
    if _STATIC_CACHE is None:
        path = os.path.join(os.path.dirname(__file__), "static_universe.json")
        try:
            with open(path) as f:
                _STATIC_CACHE = json.load(f)
        except Exception:
            _STATIC_CACHE = []
    return _STATIC_CACHE


def get_universe(universe="static", limit=50, symbols=None):
    """返回 (symbols_list, metadata_dict)"""
    def _meta(source, syms, syms_meta, fb=False, reason=""):
        return {
            "universe_requested": universe, "universe_source": source,
            "is_fallback": fb, "fallback_reason": reason,
            "count": min(len(syms), limit), "symbols_meta": syms_meta[:limit],
        }

    if universe == "manual" and symbols:
        return symbols[:limit], _meta("manual", symbols, [])
    if universe == "sample":
        syms = symbols or SAMPLE_SYMBOLS
        return syms[:limit], _meta("sample", syms, [])
    if universe == "static":
        all_s = _load_static()
        syms = [s["symbol"] for s in all_s]
        return syms[:limit], _meta("static", syms, all_s)
    if universe == "hs300":
        try:
            df = ak.index_stock_cons(symbol="000300")
            syms = df["品种代码"].tolist()
            logger.info(f"沪深300: {len(syms)} 只 (limit={limit})")
            return syms[:limit], _meta("hs300", syms, [])
        except Exception as e:
            reason = f"沪深300获取失败: {e}"
            logger.warning(reason + ", 回退 static")
            all_s = _load_static()
            syms = [s["symbol"] for s in all_s]
            return syms[:limit], _meta("static", syms, all_s, True, reason)
    if universe == "top_amount":
        try:
            df = ak.stock_zh_a_spot_em()
            if df.empty:
                raise ValueError("全市场行情为空")
            df = df.sort_values("成交额", ascending=False)
            syms = df["代码"].tolist()
            logger.info(f"成交额Top{limit}: {len(syms)} 只")
            return syms[:limit], _meta("top_amount", syms, [])
        except Exception as e:
            reason = f"Top成交额获取失败: {e}"
            logger.warning(reason + ", 回退 static")
            all_s = _load_static()
            syms = [s["symbol"] for s in all_s]
            return syms[:limit], _meta("static", syms, all_s, True, reason)

    all_s = _load_static()
    syms = [s["symbol"] for s in all_s]
    return syms[:limit], _meta("static", syms, all_s, True, f"未知类型:{universe}")


def lookup_meta(symbol):
    for s in _load_static():
        if s["symbol"] == symbol:
            return s
    return {"symbol": symbol, "name": "", "sector": ""}
