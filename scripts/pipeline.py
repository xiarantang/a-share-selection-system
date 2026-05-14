#!/usr/bin/env python3
"""
一键运行 Pipeline 脚本
=======================
集成数据获取 → 策略执行 → 回测验证 → AI 预测 → 报告生成
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime
from loguru import logger

from data.fetcher import AShareDataFetcher
from strategies.registry import StrategyRegistry
from reports.generator import ReportGenerator
from config.settings import get_config


def quick_pipeline(symbols=None):
    """快速运行完整 pipeline"""
    config = get_config()
    logger.info("启动 A 股选股 Pipeline...")

    # 1. 数据
    fetcher = AShareDataFetcher()

    # 2. 市场概况
    market = fetcher.get_market_spot_all()
    up_count = len(market[market["涨跌幅"] > 0]) if not market.empty else 0
    down_count = len(market[market["涨跌幅"] < 0]) if not market.empty else 0
    market_summary = {
        "up_count": up_count,
        "down_count": down_count,
        "total_stocks": len(market),
        "timestamp": datetime.now().isoformat(),
    }
    logger.info(f"市场: 涨{up_count} 跌{down_count}")

    # 3. 策略
    registry = StrategyRegistry()
    strategies = registry.list_strategies()
    logger.info(f"策略: {[s['name'] for s in strategies if s['available']]}")

    # 4. 报告
    reporter = ReportGenerator()
    report_path = reporter.generate_json_signals({"strategies": strategies})
    logger.info(f"报告: {report_path}")

    return {
        "market_summary": market_summary,
        "strategies": strategies,
        "report_path": report_path,
    }


if __name__ == "__main__":
    symbols = sys.argv[1:] if len(sys.argv) > 1 else None
    result = quick_pipeline(symbols)
    logger.info(f"Pipeline 完成: {result['report_path']}")
