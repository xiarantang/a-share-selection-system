#!/usr/bin/env python3
"""
A股智能选股系统 - 主入口 (v0.1)
=========================
系统总调度，串联数据→策略→回测→AI→Agent→模拟交易→报告全流程。
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

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
            name = quote.get('name', '?') if quote else '?'
            price = quote.get('price', '?') if quote else '?'
            if quote and name != '?':
                logger.info(f"  ✅ {s}: {name} {price}")
            else:
                logger.info(f"  ❌ {s}: 获取失败")

    elif args.type == "kline":
        results = {"ok": [], "fail": []}
        for s in symbols or ["000001"]:
            df = fetcher.get_daily_kline(s, start_date=args.start or "2024-01-01")
            if df is not None and not df.empty:
                results["ok"].append((s, len(df), df.index[0], df.index[-1]))
            else:
                results["fail"].append(s)
        for s, n, start, end in results["ok"]:
            logger.info(f"  ✅ {s}: {n} 条K线 ({str(start)[:10]} ~ {str(end)[:10]})")
        for s in results["fail"]:
            logger.info(f"  ❌ {s}: 获取失败或空数据")
        logger.info(f"  结果: {len(results['ok'])} 成功 / {len(results['fail'])} 失败")

    elif args.type == "market":
        df = fetcher.get_market_spot_all()
        if df is not None and not df.empty:
            logger.info(f"✅ 全市场行情: {len(df)} 只股票")
            top5 = df.head(5)[['代码', '名称', '最新价', '涨跌幅', '成交额']]
            for _, r in top5.iterrows():
                logger.info(f"  {r['代码']} {r['名称']} {r['最新价']} ({r['涨跌幅']:+.2f}%)")
        else:
            logger.info("❌ 全市场行情获取失败")

    elif args.type == "financial":
        for s in symbols or ["000001"]:
            statements = fetcher.get_financial_statements(s)
            available = [k for k, v in statements.items() if v is not None and not (hasattr(v, 'empty') and v.empty)]
            if available:
                logger.info(f"  ✅ {s}: 报表 {available}")
            else:
                logger.info(f"  ❌ {s}: 财报获取失败")


def cmd_strategy(args):
    """策略执行"""
    registry = StrategyRegistry()
    strategies = registry.list_strategies()
    logger.info(f"已注册策略: {len(strategies)} 个")
    for s in strategies:
        s_type = s.get("type", "unknown")
        icon = "📄" if s_type == "doc-only" else "▶️" if s.get("executable") else "❓"
        logger.info(f"  {icon} {s['name']} [{s_type}]")

    if args.run:
        results = registry.run_all_strategies()
        ok = sum(1 for r in results.values() if r.get("success"))
        fail = len(results) - ok
        logger.info(f"策略执行完成: {ok} 成功 / {fail} 失败")
        for name, r in results.items():
            status = "✅" if r.get("success") else "❌"
            detail = r.get("error", r.get("note", ""))
            logger.info(f"  {status} {name}: {detail}")


def cmd_backtest(args):
    """回测"""
    engine = AShareBacktestEngine()
    engine.setup(MACrossStrategy)
    ok = engine.add_data_from_fetcher(args.symbol or "000001")
    if not ok:
        logger.info(f"❌ 回测失败: {args.symbol} 无K线数据，无法运行")
        return
    results = engine.run()
    if results is None:
        logger.info("❌ 回测失败: 无数据或执行异常")
        return
    perf = engine.get_performance()
    if perf.get("error"):
        logger.info(f"❌ 回测失败: {perf['error']}")
    else:
        logger.info(f"✅ 回测完成: 收益 {perf.get('total_return_pct', '?')}%")


def cmd_ai(args):
    """AI 选股 (experimental)"""
    logger.info("⚠️  AI 选股模块当前为 experimental 状态")
    logger.info("   原因: qlib 数据未下载，pipeline 未真实跑通")
    logger.info("   需先执行: python -m qlib.cli.data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn")
    logger.info("   当前返回: experimental / not ready")


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
    if "error" in summary:
        logger.info(f"❌ 模拟账户错误: {summary['error']}")
    else:
        logger.info(f"✅ 账户 {summary['account_id']}: 总资产 {summary['total_value']}, 现金 {summary['cash']}")


def cmd_report(args):
    """生成报告"""
    reporter = ReportGenerator()
    report = reporter.generate_markdown_report(
        date=args.date or datetime.now().strftime("%Y-%m-%d"),
        market_summary={},
        strategy_signals={},
    )
    logger.info(f"✅ 报告已生成: {report[:50]}...")


def cmd_full_pipeline(args):
    """PASS/FAIL 全模块检查"""
    logger.info("=" * 60)
    logger.info("A股智能选股系统 v0.1 - 模块检查")
    logger.info("=" * 60)

    checks = {}

    # 1. 数据层 - 必需
    logger.info("[1/7] 数据层...")
    try:
        fetcher = AShareDataFetcher()
        df = fetcher.get_daily_kline("000001", start_date="2024-06-01")
        if df is not None and not df.empty:
            checks["data"] = ("PASS", f"akshare 正常 ({len(df)} 条K线)")
        else:
            checks["data"] = ("FAIL", "K线获取返回空")
    except Exception as e:
        checks["data"] = ("FAIL", str(e)[:80])

    # 2. 策略层 - 必需
    logger.info("[2/7] 策略层...")
    try:
        registry = StrategyRegistry()
        strategies = registry.list_strategies()
        executable = [s for s in strategies if s.get("type") != "doc-only"]
        checks["strategy"] = ("PASS", f"{len(strategies)} 个Skill, {len(executable)} 个可执行")
    except Exception as e:
        checks["strategy"] = ("FAIL", str(e)[:80])

    # 3. 回测层 - 必需
    logger.info("[3/7] 回测层...")
    try:
        engine = AShareBacktestEngine()
        engine.setup(MACrossStrategy)
        ok = engine.add_data_from_fetcher("000001")
        if ok:
            engine.run()
            perf = engine.get_performance()
            if not perf.get("error"):
                checks["backtest"] = ("PASS", f"收益 {perf.get('total_return_pct','?')}%")
            else:
                checks["backtest"] = ("FAIL", perf["error"])
        else:
            checks["backtest"] = ("FAIL", "无K线数据")
    except Exception as e:
        checks["backtest"] = ("FAIL", str(e)[:80])

    # 4. AI 层 - experimental
    logger.info("[4/7] AI 层...")
    try:
        import qlib  # noqa
        checks["ai"] = ("WARN", "qlib 已安装但数据未配置，标记 experimental")
    except ImportError:
        checks["ai"] = ("SKIP", "qlib 未安装 (experimental)")

    # 5. Agent 层 - 非必需
    logger.info("[5/7] Agent 层...")
    try:
        bridge = AgentBridge()
        checks["agent"] = ("PASS", "桥接器可用（LLM需 API Key）")
    except Exception as e:
        checks["agent"] = ("FAIL", str(e)[:80])

    # 6. 模拟交易
    logger.info("[6/7] 模拟交易层...")
    try:
        pt = PaperTradingEngine()
        summary = pt.get_account_summary("default")
        if "error" in summary:
            pt.create_account("default", 100000)
            checks["paper_trading"] = ("PASS", "账户已创建")
        else:
            checks["paper_trading"] = ("PASS", f"总资产 {summary.get('total_value','?')}")
    except Exception as e:
        checks["paper_trading"] = ("FAIL", str(e)[:80])

    # 7. 报告层 - 必需
    logger.info("[7/7] 报告层...")
    try:
        reporter = ReportGenerator()
        checks["report"] = ("PASS", "生成器可用")
    except Exception as e:
        checks["report"] = ("FAIL", str(e)[:80])

    # 汇总输出
    logger.info("=" * 60)
    logger.info("检查结果:")
    for name, (status, detail) in checks.items():
        icon = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "SKIP": "⏭️"}.get(status, "❓")
        logger.info(f"  {icon} [{status}] {name}: {detail}")

    core_required = ["data", "strategy", "backtest", "report"]
    core_pass = all(checks.get(c, ("FAIL",))[0] == "PASS" for c in core_required)
    logger.info("=" * 60)
    if core_pass:
        logger.info("✅ 核心模块通过 (data/strategy/backtest/report)")
    else:
        failed_core = [c for c in core_required if checks.get(c, ("FAIL",))[0] != "PASS"]
        logger.info(f"❌ 核心模块未通过: {failed_core}")
    logger.info("⚠️  AI 层为 experimental，Agent 层需配置 API Key")
    logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="A股智能选股系统 v0.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py pipeline
  python main.py fetch --type kline --symbols 600519,000001,300750 --start 2024-01-01
  python main.py strategy --run
  python main.py backtest --symbol 000001
  python main.py report
        """,
    )
    sub = parser.add_subparsers(dest="command")

    p_fetch = sub.add_parser("fetch", help="数据获取")
    p_fetch.add_argument("--type", choices=["quote","kline","market","financial"], default="quote")
    p_fetch.add_argument("--symbols", help="股票代码，逗号分隔")
    p_fetch.add_argument("--start", help="起始日期 YYYY-MM-DD")
    p_fetch.set_defaults(func=cmd_fetch)

    p_strat = sub.add_parser("strategy", help="策略管理")
    p_strat.add_argument("--run", action="store_true", help="执行所有策略")
    p_strat.set_defaults(func=cmd_strategy)

    p_bt = sub.add_parser("backtest", help="回测")
    p_bt.add_argument("--symbol", default="000001")
    p_bt.set_defaults(func=cmd_backtest)

    p_ai = sub.add_parser("ai", help="AI 选股 (experimental)")
    p_ai.set_defaults(func=cmd_ai)

    p_agent = sub.add_parser("agent", help="Agent 分析")
    p_agent.add_argument("--analyze", help="分析指定股票")
    p_agent.set_defaults(func=cmd_agent)

    p_pt = sub.add_parser("paper-trading", help="模拟交易")
    p_pt.add_argument("--account", default="default")
    p_pt.set_defaults(func=cmd_paper_trading)

    p_report = sub.add_parser("report", help="生成报告")
    p_report.add_argument("--date")
    p_report.set_defaults(func=cmd_report)

    p_pipe = sub.add_parser("pipeline", help="模块检查")
    p_pipe.set_defaults(func=cmd_full_pipeline)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
