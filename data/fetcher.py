"""
数据层：A股数据获取器
====================
基于 akshare 的统一数据接口，提供行情、财务、资金流、技术指标等全维度数据。
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

import akshare as ak
import pandas as pd
from loguru import logger

from config.settings import DataConfig, get_config


class AShareDataFetcher:
    """A股数据获取器 - 封装 akshare 为统一接口"""

    def __init__(self, config: Optional[DataConfig] = None):
        self.config = config or get_config().data
        os.makedirs(self.config.cache_dir, exist_ok=True)
        self._last_source = "unknown"
        logger.info("AShareDataFetcher 初始化完成")

    # ---- 行情数据 ----

    def get_realtime_quote(self, symbol: str) -> dict:
        """获取个股实时行情"""
        try:
            df = ak.stock_zh_a_spot_em()
            code = symbol.replace("SH", "").replace("SZ", "")
            row = df[df["代码"] == code]
            if row.empty:
                return {}
            r = row.iloc[0]
            return {
                "symbol": symbol,
                "name": r["名称"],
                "price": float(r["最新价"]),
                "change_pct": float(r["涨跌幅"]),
                "volume": int(r["成交量"]),
                "amount": float(r["成交额"]),
                "high": float(r["最高"]),
                "low": float(r["最低"]),
                "open": float(r["今开"]),
                "pre_close": float(r["昨收"]),
                "turnover_rate": float(r.get("换手率", 0)),
                "pe": float(r.get("市盈率-动态", 0)),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"获取 {symbol} 实时行情失败: {e}")
            return {}

    def get_daily_kline(
        self,
        symbol: str,
        start_date: str = "2024-01-01",
        end_date: Optional[str] = None,
        adjust: str = "qfq",
    ) -> pd.DataFrame:
        """获取个股日K线（前复权）。
        多源 fallback: akshare → a-share-data skill (腾讯/新浪/雪球/东财) → 本地缓存。
        成功拉到后保存到 data/cache/。
        """
        end_date = end_date or datetime.now().strftime("%Y%m%d")
        cache_path = os.path.join(
            self.config.cache_dir,
            f"{symbol}_{start_date.replace('-','')}_{end_date.replace('-','')}.parquet",
        )

        # 1. 尝试 akshare
        df = self._fetch_akshare(symbol, start_date, end_date, adjust)
        if df is not None and not df.empty:
            self._last_source = "akshare"
            self._save_cache(cache_path, df)
            return df

        # 2. akshare 失败 → 尝试 a-share-data skill fallback 脚本
        logger.info(f"akshare 失败, 尝试 skill fallback: {symbol}")
        df = self._fetch_skill_fallback(symbol, start_date, end_date, adjust)
        if df is not None and not df.empty:
            self._last_source = "skill_fallback"
            self._save_cache(cache_path, df)
            return df

        # 3. 网络都失败 → 尝试本地缓存
        if os.path.exists(cache_path):
            try:
                df = pd.read_parquet(cache_path)
                if not df.empty:
                    self._last_source = "cache"
                    logger.info(f"从本地缓存读取 {symbol}: {len(df)} 条")
                    return df
            except Exception as e:
                logger.warning(f"缓存读取失败 {symbol}: {e}")

        # 4. 全部失败
        self._last_source = "failed"
        logger.error(f"获取 {symbol} 日K线失败: 所有数据源不可用")
        return pd.DataFrame()

    def _fetch_akshare(
        self, symbol: str, start_date: str, end_date: str, adjust: str
    ) -> Optional[pd.DataFrame]:
        try:
            df = ak.stock_zh_a_hist(
                symbol=symbol, period="daily",
                start_date=start_date.replace("-", ""),
                end_date=end_date.replace("-", ""),
                adjust=adjust,
            )
            if df is None or df.empty:
                return None
            df = df.rename(columns={
                "日期": "date", "开盘": "open", "收盘": "close",
                "最高": "high", "最低": "low", "成交量": "volume",
                "成交额": "amount", "振幅": "amplitude",
                "涨跌幅": "pct_change", "涨跌额": "change",
                "换手率": "turnover",
            })
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            return df
        except Exception as e:
            logger.warning(f"akshare 获取 {symbol} 失败: {e}")
            return None

    def _fetch_skill_fallback(
        self, symbol: str, start_date: str, end_date: str, adjust: str
    ) -> Optional[pd.DataFrame]:
        """调用 a-share-data/scripts/fetch_history_fallback.py --json"""
        import subprocess
        import json
        import re

        script = os.path.expanduser(
            "~/.agents/skills/a-share-data/scripts/fetch_history_fallback.py"
        )
        if not os.path.exists(script):
            logger.warning(f"fallback 脚本不存在: {script}")
            return None

        try:
            cmd = [
                "python3", script,
                "--kline", symbol,
                "--start", start_date,
                "--end", end_date,
                "--json",
            ]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=20,
            )
            if result.returncode != 0:
                logger.warning(f"skill fallback exit={result.returncode}: {result.stderr[:200]}")
                return None

            raw = result.stdout.strip()
            if not raw:
                return None

            # 提取第一个 JSON 数组（跳过前置 warning 行）
            match = re.search(r'\[.*\]', raw, re.DOTALL)
            if not match:
                logger.warning(f"skill fallback 输出无JSON数组: {raw[:200]}")
                return None

            rows = json.loads(match.group())
            if not isinstance(rows, list) or not rows:
                return None

            df = pd.DataFrame(rows)
            # 字段映射: time→date, pctChg→pct_change, preclose→pre_close
            col_map = {
                "time": "date", "pctChg": "pct_change", "preclose": "pre_close",
            }
            df = df.rename(columns=col_map)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df.set_index("date", inplace=True)
            for col in ["open", "high", "low", "close", "volume"]:
                if col not in df.columns:
                    df[col] = 0.0
            logger.info(f"skill fallback 成功: {symbol} {len(df)} 条")
            return df
        except subprocess.TimeoutExpired:
            logger.warning("skill fallback 超时(20s)")
            return None
        except json.JSONDecodeError as e:
            logger.warning(f"skill fallback JSON解析失败: {e}")
            return None
        except Exception as e:
            logger.warning(f"skill fallback 异常: {e}")
            return None

    def _save_cache(self, path: str, df: pd.DataFrame):
        try:
            df.to_parquet(path)
        except Exception as e:
            logger.warning(f"缓存保存失败: {e}")

    def get_minute_kline(self, symbol: str, freq: str = "5") -> pd.DataFrame:
        """获取分钟K线"""
        try:
            df = ak.stock_zh_a_hist_min_em(symbol=symbol, period=freq, adjust="qfq")
            return df
        except Exception as e:
            logger.error(f"获取 {symbol} 分钟K线失败: {e}")
            return pd.DataFrame()

    # ---- 市场全景 ----

    def get_market_spot_all(self) -> pd.DataFrame:
        """获取全市场实时行情快照"""
        try:
            return ak.stock_zh_a_spot_em()
        except Exception as e:
            logger.error(f"获取全市场行情失败: {e}")
            return pd.DataFrame()

    def get_index_data(self, index_code: str = "000300") -> pd.DataFrame:
        """获取指数行情"""
        try:
            df = ak.stock_zh_index_daily_em(symbol=f"sh{index_code}")
            return df
        except Exception as e:
            logger.error(f"获取指数 {index_code} 失败: {e}")
            return pd.DataFrame()

    # ---- 财务数据 ----

    def get_financial_statements(self, symbol: str) -> Dict[str, pd.DataFrame]:
        """获取三大报表"""
        result = {}
        try:
            result["income"] = ak.stock_profit_sheet_by_report_em(symbol=symbol)
            result["balance"] = ak.stock_balance_sheet_by_report_em(symbol=symbol)
            result["cashflow"] = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
        except Exception as e:
            logger.error(f"获取 {symbol} 财报失败: {e}")
        return result

    def get_financial_indicators(self, symbol: str) -> pd.DataFrame:
        """获取主要财务指标"""
        try:
            return ak.stock_financial_abstract_ths(symbol=symbol)
        except Exception as e:
            logger.error(f"获取 {symbol} 财务指标失败: {e}")
            return pd.DataFrame()

    # ---- 资金流向 ----

    def get_money_flow(self, symbol: str) -> pd.DataFrame:
        """获取个股资金流向"""
        try:
            return ak.stock_individual_fund_flow(
                stock=symbol, market="sh" if symbol.startswith("6") else "sz"
            )
        except Exception as e:
            logger.error(f"获取 {symbol} 资金流向失败: {e}")
            return pd.DataFrame()

    def get_north_bound_flow(self) -> pd.DataFrame:
        """获取北向资金流向"""
        try:
            return ak.stock_hsgt_north_net_flow_in_em()
        except Exception as e:
            logger.error(f"获取北向资金失败: {e}")
            return pd.DataFrame()

    # ---- 板块与概念 ----

    def get_hot_sectors(self) -> pd.DataFrame:
        """获取热门行业板块"""
        try:
            return ak.stock_board_industry_name_em()
        except Exception as e:
            logger.error(f"获取板块数据失败: {e}")
            return pd.DataFrame()

    def get_concept_board(self) -> pd.DataFrame:
        """获取概念板块"""
        try:
            return ak.stock_board_concept_name_em()
        except Exception as e:
            logger.error(f"获取概念板块失败: {e}")
            return pd.DataFrame()

    # ---- 涨跌停 ----

    def get_limit_up_stocks(self, date: Optional[str] = None) -> pd.DataFrame:
        """获取涨停股票列表"""
        date = date or datetime.now().strftime("%Y%m%d")
        try:
            return ak.stock_zt_pool_em(date=date)
        except Exception as e:
            logger.error(f"获取涨停板数据失败: {e}")
            return pd.DataFrame()

    # ---- 技术指标 ----

    def calc_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """在K线数据上计算常用技术指标"""
        if df.empty:
            return df
        close = df["close"]
        high = df["high"]
        low = df["low"]
        volume = df["volume"]

        # MA
        for p in [5, 10, 20, 60, 120, 250]:
            df[f"MA{p}"] = close.rolling(p).mean()

        # MACD
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        df["MACD_DIF"] = ema12 - ema26
        df["MACD_DEA"] = df["MACD_DIF"].ewm(span=9, adjust=False).mean()
        df["MACD_HIST"] = 2 * (df["MACD_DIF"] - df["MACD_DEA"])

        # RSI(14)
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        df["RSI14"] = 100 - (100 / (1 + rs))

        # KDJ
        low_n = low.rolling(9).min()
        high_n = high.rolling(9).max()
        rsv = (close - low_n) / (high_n - low_n) * 100
        df["KDJ_K"] = rsv.ewm(com=2, adjust=False).mean()
        df["KDJ_D"] = df["KDJ_K"].ewm(com=2, adjust=False).mean()
        df["KDJ_J"] = 3 * df["KDJ_K"] - 2 * df["KDJ_D"]

        # BOLL
        df["BOLL_MID"] = close.rolling(20).mean()
        std = close.rolling(20).std()
        df["BOLL_UP"] = df["BOLL_MID"] + 2 * std
        df["BOLL_DN"] = df["BOLL_MID"] - 2 * std

        # ATR(14)
        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ], axis=1).max(axis=1)
        df["ATR14"] = tr.rolling(14).mean()

        # OBV
        df["OBV"] = (volume * ((close.diff() > 0) * 2 - 1)).cumsum()

        return df

    # ---- 股票池 ----

    def get_stock_universe(self) -> List[str]:
        """获取股票池"""
        if self.config.universe == "csi300":
            return self._get_index_members("000300")
        elif self.config.universe == "csi500":
            return self._get_index_members("000905")
        elif self.config.custom_symbols:
            return self.config.custom_symbols
        else:
            df = self.get_market_spot_all()
            if df.empty:
                return []
            df = df.sort_values("成交额", ascending=False)
            return df.head(500)["代码"].tolist()

    def _get_index_members(self, index_code: str) -> List[str]:
        try:
            df = ak.index_stock_cons(symbol=index_code)
            return df["品种代码"].tolist()
        except Exception as e:
            logger.error(f"获取指数成分股失败: {e}")
            return []


def get_fetcher() -> AShareDataFetcher:
    return AShareDataFetcher()
