"""
回测层：基于 backtrader 的 A 股回测引擎
=========================================
封装 backtrader，提供 A 股专用配置（T+1、涨跌停、手续费等）。
"""

from datetime import datetime
from typing import Callable, Dict, List, Optional

import backtrader as bt
import pandas as pd
from loguru import logger

from config.settings import BacktestConfig, get_config
from data.fetcher import AShareDataFetcher


class AShareCommission(bt.CommInfoBase):
    """A 股手续费模型：佣金 + 印花税（卖出）"""
    params = (
        ("commission", 0.0003),     # 佣金 0.03%
        ("stamp_duty", 0.001),      # 印花税 0.1%（仅卖出）
        ("min_commission", 5.0),    # 最低佣金 5 元
    )

    def _getcommission(self, size, price, pseudoexec):
        value = abs(size) * price
        comm = max(value * self.p.commission, self.p.min_commission)
        if size < 0:  # 卖出：加印花税
            comm += value * self.p.stamp_duty
        return comm


class PandasDataFeed(bt.feeds.PandasData):
    """将 pandas DataFrame 适配为 backtrader 数据源"""
    params = (
        ("datetime", None),  # index is datetime
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("openinterest", -1),
    )


class AShareBacktestEngine:
    """A 股回测引擎"""

    def __init__(self, config: Optional[BacktestConfig] = None):
        self.config = config or get_config().backtest
        self.fetcher = AShareDataFetcher()
        self.cerebro = None
        self.results = None

    def setup(self, strategy_class: type):
        """初始化回测环境"""
        cerebro = bt.Cerebro()

        # 资金
        cerebro.broker.setcash(self.config.initial_cash)

        # 手续费
        comminfo = AShareCommission(
            commission=self.config.commission,
            stamp_duty=self.config.stamp_duty,
        )
        cerebro.broker.addcommissioninfo(comminfo)

        # 添加策略
        cerebro.addstrategy(strategy_class)

        self.cerebro = cerebro
        logger.info(
            f"回测引擎初始化: 初始资金={self.config.initial_cash}, "
            f"佣金={self.config.commission}, 印花税={self.config.stamp_duty}"
        )

    def add_data(self, df: pd.DataFrame, name: str = "stock"):
        """添加股票数据"""
        if self.cerebro is None:
            raise RuntimeError("请先调用 setup()")
        data = PandasDataFeed(dataname=df)
        self.cerebro.adddata(data, name=name)

    def add_data_from_fetcher(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        """从数据获取器加载 K 线并添加到回测"""
        start = start_date or self.config.start_date
        end = end_date or self.config.end_date
        df = self.fetcher.get_daily_kline(symbol, start, end)
        if df.empty:
            logger.error(f"无法获取 {symbol} 的K线数据")
            return
        # 计算技术指标
        df = self.fetcher.calc_technical_indicators(df)
        self.add_data(df, name=symbol)
        logger.info(f"已加载 {symbol} K线: {len(df)} 条, {df.index[0]} ~ {df.index[-1]}")

    def add_benchmark_data(self, benchmark: str = "000300"):
        """添加基准指数数据用于对比"""
        df = self.fetcher.get_index_data(benchmark)
        if not df.empty:
            self.add_data(df, name=f"benchmark_{benchmark}")

    def run(self):
        """执行回测"""
        if self.cerebro is None:
            raise RuntimeError("请先调用 setup()")

        start_value = self.cerebro.broker.getvalue()
        logger.info(f"回测开始: 初始资金={start_value:.2f}")

        self.results = self.cerebro.run()
        self._final_value = self.cerebro.broker.getvalue()

        logger.info(f"回测结束: 最终资金={self._final_value:.2f}")
        return self.results

    def get_performance(self) -> Dict:
        """获取回测绩效指标"""
        if self.results is None:
            return {"error": "请先运行回测"}

        final_value = getattr(self, "_final_value", 0)
        initial = self.config.initial_cash
        total_return = (final_value - initial) / initial * 100

        metrics = {
            "initial_cash": initial,
            "final_value": final_value,
            "total_return_pct": round(total_return, 2),
            # backtrader 内置分析器结果
            "analyzers": {},
        }

        # 提取第一个策略的分析器
        if self.results:
            strat = self.results[0]
            for aname in dir(strat.analyzers):
                if aname.startswith("_"):
                    continue
                try:
                    analyzer = getattr(strat.analyzers, aname)
                    analysis = analyzer.get_analysis()
                    # 简化输出
                    if isinstance(analysis, dict):
                        metrics["analyzers"][aname] = {
                            k: round(v, 4) if isinstance(v, float) else v
                            for k, v in list(analysis.items())[:10]
                        }
                except Exception:
                    pass

        return metrics

    def plot(self, save_path: Optional[str] = None):
        """绘制回测曲线"""
        if self.cerebro is None:
            raise RuntimeError("请先运行回测")
        try:
            figs = self.cerebro.plot(
                style="candlestick",
                barup="red",
                bardown="green",
                volume=True,
                savefig=save_path,
            )
            return figs
        except Exception as e:
            logger.error(f"绘图失败: {e}")
            return None


# ---- 示例：简单的均线交叉策略 ----

class MACrossStrategy(bt.Strategy):
    """双均线交叉策略（示例）"""
    params = (
        ("fast", 5),
        ("slow", 20),
    )

    def __init__(self):
        self.ma_fast = bt.indicators.SMA(self.data.close, period=self.p.fast)
        self.ma_slow = bt.indicators.SMA(self.data.close, period=self.p.slow)
        self.crossover = bt.indicators.CrossOver(self.ma_fast, self.ma_slow)

    def next(self):
        if not self.position:
            if self.crossover > 0:  # 金叉买入
                self.buy()
        elif self.crossover < 0:  # 死叉卖出
            self.close()
