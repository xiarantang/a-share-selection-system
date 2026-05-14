"""
回测层：基于 backtrader 的 A 股回测引擎 (v0.1)
==============================================
封装 backtrader，提供 A 股专用配置。
空数据直接拒绝，不允许假成功。
"""

from datetime import datetime
from typing import Dict, Optional

import backtrader as bt
import pandas as pd
from loguru import logger

from config.settings import BacktestConfig, get_config
from data.fetcher import AShareDataFetcher


class AShareCommission(bt.CommInfoBase):
    params = (
        ("commission", 0.0003),
        ("stamp_duty", 0.001),
        ("min_commission", 5.0),
    )

    def _getcommission(self, size, price, pseudoexec):
        value = abs(size) * price
        comm = max(value * self.p.commission, self.p.min_commission)
        if size < 0:
            comm += value * self.p.stamp_duty
        return comm


class PandasDataFeed(bt.feeds.PandasData):
    params = (
        ("datetime", None),
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("openinterest", -1),
    )


class AShareBacktestEngine:
    """A 股回测引擎 - v0.1 严格模式"""

    def __init__(self, config: Optional[BacktestConfig] = None):
        self.config = config or get_config().backtest
        self.fetcher = AShareDataFetcher()
        self.cerebro = None
        self.results = None
        self._data_count = 0
        self._final_value = None

    def setup(self, strategy_class: type):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(self.config.initial_cash)
        comminfo = AShareCommission(
            commission=self.config.commission,
            stamp_duty=self.config.stamp_duty,
        )
        cerebro.broker.addcommissioninfo(comminfo)
        cerebro.addstrategy(strategy_class)
        self.cerebro = cerebro
        self._data_count = 0
        self._final_value = None
        logger.info(
            f"回测引擎初始化: 初始资金={self.config.initial_cash}"
        )

    def add_data(self, df: pd.DataFrame, name: str = "stock") -> bool:
        if self.cerebro is None:
            raise RuntimeError("请先调用 setup()")
        if df is None or df.empty:
            logger.error(f"添加数据失败: {name} 数据为空")
            return False
        data = PandasDataFeed(dataname=df)
        self.cerebro.adddata(data, name=name)
        self._data_count += 1
        return True

    def add_data_from_fetcher(
        self, symbol: str, start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> bool:
        """从数据获取器加载 K 线。返回 True/False。"""
        start = start_date or self.config.start_date
        end = end_date or self.config.end_date
        df = self.fetcher.get_daily_kline(symbol, start, end)
        if df is None or df.empty:
            logger.error(f"回测数据获取失败: {symbol} ({start}~{end}) 无K线")
            return False
        df = self.fetcher.calc_technical_indicators(df)
        self.add_data(df, name=symbol)
        logger.info(f"已加载 {symbol}: {len(df)} 条K线")
        return True

    def run(self):
        """执行回测。无数据时返回 None。"""
        if self.cerebro is None:
            logger.error("回测失败: 未调用 setup()")
            return None
        if self._data_count == 0:
            logger.error("回测失败: 无数据")
            return None

        start_value = self.cerebro.broker.getvalue()
        logger.info(f"回测开始: 初始资金={start_value:.2f}")
        self.results = self.cerebro.run()
        self._final_value = self.cerebro.broker.getvalue()
        logger.info(f"回测结束: 最终资金={self._final_value:.2f}")
        return self.results

    def get_performance(self) -> Dict:
        if self.results is None or self._final_value is None:
            return {"error": "回测未执行或无数据"}
        initial = self.config.initial_cash
        total_return = (self._final_value - initial) / initial * 100
        return {
            "initial_cash": initial,
            "final_value": round(self._final_value, 2),
            "total_return_pct": round(total_return, 2),
        }


class MACrossStrategy(bt.Strategy):
    params = (("fast", 5), ("slow", 20))

    def __init__(self):
        self.ma_fast = bt.indicators.SMA(self.data.close, period=self.p.fast)
        self.ma_slow = bt.indicators.SMA(self.data.close, period=self.p.slow)
        self.crossover = bt.indicators.CrossOver(self.ma_fast, self.ma_slow)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()
