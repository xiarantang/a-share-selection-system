"""
股票池模块：管理候选股票列表
============================
支持 manual / sample / hs300 / top_amount 四种股票池。
"""

from typing import List, Optional

import akshare as ak
import pandas as pd
from loguru import logger

SAMPLE_SYMBOLS = ["600519", "000001", "300750"]


def get_universe(
    universe: str = "sample",
    limit: int = 50,
    symbols: Optional[List[str]] = None,
) -> tuple:
    """返回 (symbols, source_description)。"""
    if universe == "manual" and symbols:
        return symbols, "manual"

    if universe == "sample":
        syms = symbols or SAMPLE_SYMBOLS
        return syms[:limit], "sample"

    if universe == "hs300":
        try:
            df = ak.index_stock_cons(symbol="000300")
            syms = df["品种代码"].tolist()[:limit]
            logger.info(f"沪深300成分股: {len(syms)} 只 (limit={limit})")
            return syms, "hs300"
        except Exception as e:
            logger.warning(f"获取沪深300失败: {e}, 回退 sample")
            return SAMPLE_SYMBOLS[:limit], "sample_fallback"

    if universe == "top_amount":
        try:
            df = ak.stock_zh_a_spot_em()
            if df.empty:
                raise ValueError("全市场行情为空")
            df = df.sort_values("成交额", ascending=False)
            syms = df["代码"].tolist()[:limit]
            logger.info(f"成交额Top{limit}: {len(syms)} 只")
            return syms, "top_amount"
        except Exception as e:
            logger.warning(f"获取Top成交额失败: {e}, 回退 sample")
            return SAMPLE_SYMBOLS[:limit], "sample_fallback"

    logger.warning(f"未知 universe={universe}, 回退 sample")
    return SAMPLE_SYMBOLS[:limit], "sample"
