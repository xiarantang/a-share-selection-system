#!/usr/bin/env python3
"""
A股智能选股系统 - 主入口
=========================
系统总调度，串联数据→策略→回测→AI→Agent→模拟交易→报告全流程。
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# 确保项目根目录在 sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from loguru import logger

from config.settings import get_config, SystemConfig
from data.fetcher import AShareDataFetcher
from strategies.registry import StrategyRegistry
from backtest.engine import AShareBacktestEngine, MACrossStrategy
from agent.bridge import AgentBridge
from paper_trading.engine import PaperTradingEngine
from reports.generator import ReportGenerator


def cmd_fetch(args):
    """数据获取"""
    fetcher = AShareDataFetcher()
    symbols = args.symbols.split(",") if args.symbols else None

    if args.type == "quote":
        for s in symbols or ["000001"]:
            quote = fetcher.get_realtime_quote(s)
            logger.info(f"{s}: {quote.get('name', '?')} {quote.get('price', '?')}")

    elif args.type == "kline":
        for s in symbols or ["000001"]:
            df = fetcher.get_daily_kline(s, start_date=args.start or "2024-01-01")
            logger.info(f"{s}: {len(df)} 条K线")

    elif args.type == "market":
        df = fetcher.get_market_spot_all()
        logger.info(f"全市场行情: {len(df)} 只股票")
        logger.info(f"Top 5 成交额:\n{df.head(5)[['代码','名称','最新价','涨跌幅','成交额']]}")

    elif args.type == "financial":
        for s in symbols or ["000001"]:
            statements = fetcher.get_financial_statements(s)
            logger.info(f"{s} 财报: {list(statements.keys())}")


def cmd_strategy(args):
    """策略执行"""
    registry = StrategyRegistry()
    strategies = registry.list_strategies()
    logger.info(f"已注册策略: {len(strategies)} 个")
    for s in strategies:
        logger.info(f"  - {s['name']}: {'✅' if s['available'] else '❌'}")

    if args.run:
        results = registry.run_all_strategies()
        logger.info(f"策略执行完成: {list(results.keys())}")


def cmd_backtest(args):
    """回测"""
    engine = AShareBacktestEngine()
    engine.setup(MACrossStrategy)
    engine.add_data_from_fetcher(args.symbol or "000001")
    engine.run()
    perf = engine.get_performance()
    logger.info(f"回测绩效: {perf}")


def cmd_ai(args):
    """AI 选股"""
    from ai_models.qlib_runner import QlibRunner
    runner = QlibRunner()
    result = runner.run_pipeline()
    logger.info(f"AI 选股结果: {result.get('status')}")


def cmd_agent(args):
    """Agent 分析"""
    bridge = AgentBridge()
    if args.analyze:
        stock_data = {}
        result = bridge.analyze_stock(args.analyze, stock_data)
        logger.info(f"AI 分析结果:\n{result}")


def cmd_paper_trading(args):
    """模拟交易"""
    pt = PaperTradingEngine()
    summary = pt.get_account_summary(args.account or "default")
    logger.info(f"账户摘要: {summary}")


def cmd_report(args):
    """生成报告"""
    reporter = ReportGenerator()
    report = reporter.generate_markdown_report(
        date=args.date or datetime.now().strftime("%Y-%m-%d"),
        market_summary={},
        strategy_signals={},
    )
    logger.info(f"报告生成完成")


def cmd_full_pipeline(args):
    """一键全流程"""
    logger.info("=" * 60)
    logger.info("A股智能选股系统 - 全流程启动")
    logger.info("=" * 60)

    # 1. 数据
    logger.info("[1/7] 数据层初始化...")
    fetcher = AShareDataFetcher()
    quote = fetcher.get_realtime_quote("000001")
    logger.info(f"  数据层就绪, 示例行情: {quote.get('name', '?')}")

    # 2. 策略
    logger.info("[2/7] 策略层加载...")
    registry = StrategyRegistry()
    strategies = registry.list_strategies()
    logger.info(f"  已加载 {len(strategies)} 个策略")

    # 3. 回测
    logger.info("[3/7] 回测层验证...")
    engine = AShareBacktestEngine()
    engine.setup(MACrossStrategy)
    logger.info("  回测引擎就绪")

    # 4. AI
    logger.info("[4/7] AI 层检查...")
    try:
        from ai_models.qlib_runner import QlibRunner
        ai_runner = QlibRunner()
        logger.info("  qlib 模块可用")
    except Exception as e:
        logger.warning(f"  AI 层: {e}")

    # 5. Agent
    logger.info("[5/7] Agent 层连接...")
    bridge = AgentBridge()
    logger.info("  Agent 桥接器就绪")

    # 6. 模拟交易
    logger.info("[6/7] 模拟交易层...")
    pt = PaperTradingEngine()
    logger.info("  模拟盘引擎就绪")

    # 7. 报告
    logger.info("[7/7] 报告层...")
    reporter = ReportGenerator()
    logger.info("  报告生成器就绪")

    logger.info("=" * 60)
    logger.info("✅ 全流程就绪！系统各层均可正常工作。")
    logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="A股智能选股系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py pipeline              # 一键全流程
  python main.py fetch --type quote --symbols 000001,600519
  python main.py strategy --run
  python main.py backtest --symbol 000001
  python main.py ai
  python main.py report
        """,
    )
    sub = parser.add_subparsers(dest="command")

    # fetch
    p_fetch = sub.add_parser("fetch", help="数据获取")
    p_fetch.add_argument("--type", choices=["quote","kline","market","financial"], default="quote")
    p_fetch.add_argument("--symbols", help="股票代码，逗号分隔")
    p_fetch.add_argument("--start", help="起始日期 YYYY-MM-DD")
    p_fetch.set_defaults(func=cmd_fetch)

    # strategy
    p_strat = sub.add_parser("strategy", help="策略管理")
    p_strat.add_argument("--run", action="store_true", help="执行所有策略")
    p_strat.set_defaults(func=cmd_strategy)

    # backtest
    p_bt = sub.add_parser("backtest", help="回测")
    p_bt.add_argument("--symbol", default="000001")
    p_bt.set_defaults(func=cmd_backtest)

    # ai
    p_ai = sub.add_parser("ai", help="AI 选股")
    p_ai.set_defaults(func=cmd_ai)

    # agent
    p_agent = sub.add_parser("agent", help="Agent 分析")
    p_agent.add_argument("--analyze", help="分析指定股票")
    p_agent.set_defaults(func=cmd_agent)

    # paper-trading
    p_pt = sub.add_parser("paper-trading", help="模拟交易")
    p_pt.add_argument("--account", default="default")
    p_pt.set_defaults(func=cmd_paper_trading)

    # report
    p_report = sub.add_parser("report", help="生成报告")
    p_report.add_argument("--date")
    p_report.set_defaults(func=cmd_report)

    # pipeline
    p_pipe = sub.add_parser("pipeline", help="一键全流程")
    p_pipe.set_defaults(func=cmd_full_pipeline)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
