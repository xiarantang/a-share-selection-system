#!/usr/bin/env python3
"""
A股智能选股系统 - 主入口 (v0.1)
=========================
系统总调度，串联数据→策略→回测→AI→Agent→模拟交易→报告全流程。
"""

import argparse
import os
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
from strategies.selection import SelectionEngine
from data.universe import get_universe


def cmd_fetch(args):
    """数据获取。返回 0=全部成功, 1=有失败。"""
    fetcher = AShareDataFetcher()
    symbols = args.symbols.split(",") if args.symbols else None
    has_failure = False

    if args.type == "quote":
        for s in symbols or ["000001"]:
            quote = fetcher.get_realtime_quote(s)
            name = quote.get('name', '?') if quote else '?'
            price = quote.get('price', '?') if quote else '?'
            if quote and name != '?':
                logger.info(f"  ✅ {s}: {name} {price}")
            else:
                logger.info(f"  ❌ {s}: 获取失败")
                has_failure = True

    elif args.type == "kline":
        results = {"ok": [], "fail": []}
        for s in symbols or ["000001"]:
            df = fetcher.get_daily_kline(s, start_date=args.start or "2024-01-01")
            if df is not None and not df.empty:
                results["ok"].append((s, len(df), df.index[0], df.index[-1], fetcher._last_source))
            else:
                results["fail"].append(s)
        for s, n, start, end, src in results["ok"]:
            logger.info(f"  ✅ {s}: {n} 条K线 [{src}] ({str(start)[:10]} ~ {str(end)[:10]})")
        for s in results["fail"]:
            logger.info(f"  ❌ {s}: 获取失败或空数据")
        logger.info(f"  结果: {len(results['ok'])} 成功 / {len(results['fail'])} 失败")
        # --allow-partial: 至少1只成功才允许exit 0；全部失败仍exit 1
        allow_partial = getattr(args, 'allow_partial', False)
        if results["fail"]:
            if not allow_partial or not results["ok"]:
                has_failure = True

    elif args.type == "market":
        df = fetcher.get_market_spot_all()
        if df is not None and not df.empty:
            logger.info(f"✅ 全市场行情: {len(df)} 只股票")
            top5 = df.head(5)[['代码', '名称', '最新价', '涨跌幅', '成交额']]
            for _, r in top5.iterrows():
                logger.info(f"  {r['代码']} {r['名称']} {r['最新价']} ({r['涨跌幅']:+.2f}%)")
        else:
            logger.info("❌ 全市场行情获取失败")
            has_failure = True

    elif args.type == "financial":
        for s in symbols or ["000001"]:
            statements = fetcher.get_financial_statements(s)
            available = [k for k, v in statements.items() if v is not None and not (hasattr(v, 'empty') and v.empty)]
            if available:
                logger.info(f"  ✅ {s}: 报表 {available}")
            else:
                logger.info(f"  ❌ {s}: 财报获取失败")
                has_failure = True

    return 1 if has_failure else 0


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
        results, stats = registry.run_all_strategies()
        logger.info(
            f"策略执行统计: executed={stats['executed']} "
            f"skipped_doc_only={stats['skipped_doc_only']} "
            f"failed={stats['failed']}"
        )
        for name, r in results.items():
            if r.get("type") == "doc-only":
                status = "⏭️ skipped"
            elif r.get("success"):
                status = "✅"
            else:
                status = "❌"
            detail = r.get("error", r.get("note", ""))
            logger.info(f"  {status} {name}: {detail}")
        return 1 if stats["failed"] > 0 else 0

    return 0


def cmd_backtest(args):
    """回测。返回 0=成功, 1=失败。"""
    engine = AShareBacktestEngine()
    engine.setup(MACrossStrategy)
    ok = engine.add_data_from_fetcher(args.symbol or "000001")
    if not ok:
        logger.info(f"❌ 回测失败: {args.symbol} 无K线数据，无法运行")
        return 1
    results = engine.run()
    if results is None:
        logger.info("❌ 回测失败: 无数据或执行异常")
        return 1
    perf = engine.get_performance()
    if perf.get("error"):
        logger.info(f"❌ 回测失败: {perf['error']}")
        return 1
    logger.info(f"✅ 回测完成: 收益 {perf.get('total_return_pct', '?')}%")
    return 0


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


def cmd_select(args):
    """批量选股：支持 universe 参数扩大股票池"""
    import csv, json

    # 获取股票池
    req_start = getattr(args, 'start', None) or "2024-01-01"
    universe = getattr(args, 'universe', None) or "sample"
    limit = int(getattr(args, 'limit', 50) or 50)
    top = int(getattr(args, 'top', 10) or 10)
    manual_symbols = args.symbols.split(",") if getattr(args, 'symbols', None) else None

    if manual_symbols:
        symbols, universe_src = get_universe("manual", limit=limit, symbols=manual_symbols)
    else:
        symbols, universe_src = get_universe(universe, limit=limit)

    os.makedirs("reports/output", exist_ok=True)

    # 批量选股
    engine = SelectionEngine()
    all_results = engine.select(symbols, start_date=req_start)

    # 统计
    stats = {"total": len(symbols), "success": 0, "failed": 0, "source_dist": {}}
    for r in all_results:
        if r.get("error"):
            stats["failed"] += 1
        else:
            stats["success"] += 1
            # coverage check
            if r.get("actual_start", "N/A") > req_start[:10]:
                r["coverage_warning"] = True
            # source distribution
            src = r.get("data_source", "unknown")
            stats["source_dist"][src] = stats["source_dist"].get(src, 0) + 1

    # Top N
    top_results = [r for r in all_results if not r.get("error")][:top]

    logger.info(f"选股统计: universe={universe_src}, total={stats['total']}, "
                f"success={stats['success']}, failed={stats['failed']}, "
                f"sources={stats['source_dist']}")
    logger.info(f"Top {top} 候选:")
    for r in top_results:
        cov = " ⚠️" if r.get("coverage_warning") else ""
        logger.info(f"  #{r['rank']} {r['symbol']}: {r['score']}/100 | {r['latest_close']} | "
                    f"{r['data_source']} | {r['rows']}行{cov}")

    # 保存 CSV
    date_str = datetime.now().strftime("%Y%m%d")
    csv_path = os.path.join("reports", "output", f"selection_{date_str}.csv")
    csv_fields = ["rank","symbol","score","latest_close","data_source","rows",
                  "requested_start","actual_start","actual_end","coverage_warning"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=csv_fields)
        w.writeheader()
        for r in all_results:
            row = {k: r.get(k, "") for k in csv_fields}
            row["requested_start"] = req_start
            w.writerow(row)
    logger.info(f"CSV已保存: {csv_path}")

    # 保存 JSON
    json_path = os.path.join("reports", "output", f"selection_{date_str}.json")
    payload = {
        "generated_at": datetime.now().isoformat(),
        "universe": universe_src,
        "requested_start": req_start,
        "stats": stats,
        "top": top_results,
        "all": all_results,
    }
    with open(json_path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    logger.info(f"JSON已保存: {json_path}")

    if stats["success"] == 0:
        logger.info("❌ 选股失败: 所有股票数据获取失败")
        return 1
    return 0


def cmd_report(args):
    """生成报告，读取最新 selection 结果"""
    reporter = ReportGenerator()
    # 尝试读取最新 selection
    import glob
    sel_files = sorted(glob.glob(os.path.join(reporter.config.output_dir, "selection_*.json")))
    selection_data = {}
    if sel_files:
        import json
        try:
            with open(sel_files[-1]) as f:
                selection_data = json.load(f)
        except Exception:
            pass
    report = reporter.generate_markdown_report(
        date=args.date or datetime.now().strftime("%Y-%m-%d"),
        market_summary={},
        strategy_signals={},
        selection_data=selection_data,
    )
    logger.info(f"✅ 报告已生成: {report[:50]}...")


def cmd_selfcheck(args):
    """数据自检：测试样例股票的数据源可用性。"""
    fetcher = AShareDataFetcher()
    test_symbols = args.symbols.split(",") if getattr(args, 'symbols', None) else ["600519", "000001", "300750"]
    req_start = getattr(args, 'start', None) or "2024-01-01"

    results = []
    for s in test_symbols:
        df = fetcher.get_daily_kline(s, start_date=req_start)
        source = fetcher._last_source
        ok = df is not None and not df.empty
        rows = len(df) if ok else 0
        actual_start = str(df.index[0])[:10] if ok and rows > 0 else "N/A"
        actual_end = str(df.index[-1])[:10] if ok and rows > 0 else "N/A"
        coverage_ok = ok and actual_start <= req_start[:10] if actual_start != "N/A" else False
        results.append({
            "symbol": s, "status": "success" if ok else "failed",
            "source": source, "rows": rows,
            "req_start": req_start, "actual_start": actual_start, "actual_end": actual_end,
            "coverage_ok": coverage_ok,
        })

    logger.info("数据自检结果:")
    for r in results:
        icon = "✅" if r["status"] == "success" else "❌"
        cov = "" if r.get("coverage_ok") else " ⚠️ coverage_warning" if r["status"] == "success" else ""
        logger.info(
            f"  {icon} {r['symbol']}: {r['status']}{cov} | source={r['source']} | "
            f"rows={r['rows']} | requested={r['req_start']} actual={r['actual_start']}~{r['actual_end']}"
        )

    success_count = sum(1 for r in results if r["status"] == "success")
    logger.info(f"自检: {success_count}/{len(results)} 成功")
    return 0 if success_count == len(results) else (0 if success_count > 0 else 1)


def cmd_full_pipeline(args):
    """PASS/FAIL 全模块检查"""
    logger.info("=" * 60)
    logger.info("A股智能选股系统 v0.1 - 模块检查")
    logger.info("=" * 60)

    checks = {}

    # 1. 数据层 - 自检3只样本股票
    logger.info("[1/7] 数据层自检...")
    try:
        fetcher = AShareDataFetcher()
        test_symbols = ["600519", "000001", "300750"]
        data_ok = []
        for s in test_symbols:
            df = fetcher.get_daily_kline(s, start_date="2024-01-01")
            if df is not None and not df.empty:
                data_ok.append((s, len(df), fetcher._last_source))
        if data_ok:
            detail = ", ".join(f"{s}({n},{src})" for s, n, src in data_ok)
            checks["data"] = ("PASS", f"{len(data_ok)}/{len(test_symbols)} 成功: {detail}")
            pipeline_data_symbol = data_ok[0][0]  # 用于回测
        else:
            checks["data"] = ("FAIL", f"0/{len(test_symbols)} 全部失败")
            pipeline_data_symbol = None
    except Exception as e:
        checks["data"] = ("FAIL", str(e)[:80])
        pipeline_data_symbol = None

    # 2. 策略层 - 必需
    logger.info("[2/7] 策略层...")
    try:
        registry = StrategyRegistry()
        strategies = registry.list_strategies()
        executable = [s for s in strategies if s.get("type") != "doc-only"]
        checks["strategy"] = ("PASS", f"{len(strategies)} 个Skill, {len(executable)} 个可执行")
    except Exception as e:
        checks["strategy"] = ("FAIL", str(e)[:80])

    # 3. 回测层 - 使用数据自检成功的股票
    logger.info("[3/7] 回测层...")
    if pipeline_data_symbol is None:
        checks["backtest"] = ("FAIL", "无可用数据样本")
    else:
        try:
            engine = AShareBacktestEngine()
            engine.setup(MACrossStrategy)
            ok = engine.add_data_from_fetcher(pipeline_data_symbol)
            if ok:
                engine.run()
                perf = engine.get_performance()
                if not perf.get("error"):
                    checks["backtest"] = ("PASS", f"{pipeline_data_symbol} 收益 {perf.get('total_return_pct','?')}%")
                else:
                    checks["backtest"] = ("FAIL", perf["error"])
            else:
                checks["backtest"] = ("FAIL", f"{pipeline_data_symbol} 无K线数据")
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
    return 0 if core_pass else 1


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
    p_fetch.add_argument("--allow-partial", action="store_true", help="允许部分失败仍返回0")
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

    p_select = sub.add_parser("select", help="批量选股")
    p_select.add_argument("--symbols", help="股票代码，逗号分隔(manual模式)")
    p_select.add_argument("--universe", choices=["sample","hs300","top_amount","manual"], default="sample", help="股票池类型")
    p_select.add_argument("--limit", type=int, default=50, help="股票池上限")
    p_select.add_argument("--top", type=int, default=10, help="输出 Top N")
    p_select.add_argument("--start", default="2024-01-01", help="起始日期")
    p_select.set_defaults(func=cmd_select)

    p_selfcheck = sub.add_parser("selfcheck", help="数据源自检")
    p_selfcheck.add_argument("--symbols", help="股票代码，逗号分隔")
    p_selfcheck.add_argument("--start", help="起始日期")
    p_selfcheck.set_defaults(func=cmd_selfcheck)

    p_pipe = sub.add_parser("pipeline", help="模块检查")
    p_pipe.set_defaults(func=cmd_full_pipeline)

    args = parser.parse_args()
    if hasattr(args, "func"):
        exit_code = args.func(args)
        sys.exit(exit_code if exit_code is not None else 0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
