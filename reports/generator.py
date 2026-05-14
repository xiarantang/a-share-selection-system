"""
报告层：选股报告生成器
======================
整合数据、策略信号、AI 分析，生成每日选股报告。
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from config.settings import ReportConfig, get_config


class ReportGenerator:
    """选股报告生成器"""

    def __init__(self, config: Optional[ReportConfig] = None):
        self.config = config or get_config().report
        os.makedirs(self.config.output_dir, exist_ok=True)

    def generate_markdown_report(
        self,
        date: str,
        market_summary: Dict,
        strategy_signals: Dict[str, List[Dict]],
        ai_analysis: Optional[str] = None,
        selection_data: Optional[Dict] = None,
    ) -> str:
        """生成 Markdown 格式报告"""
        lines = [
            f"# 🏦 A股智能选股日报",
            f"**日期**: {date}",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## 📊 市场概况",
            "",
        ]

        # 市场数据
        ms = market_summary
        lines.append(f"- 上涨家数: {ms.get('up_count', 'N/A')}")
        lines.append(f"- 下跌家数: {ms.get('down_count', 'N/A')}")
        lines.append(f"- 涨停家数: {ms.get('limit_up_count', 'N/A')}")
        lines.append(f"- 跌停家数: {ms.get('limit_down_count', 'N/A')}")
        lines.append(f"- 成交额: {ms.get('total_amount', 'N/A')} 亿")
        lines.append(f"- 北向资金: {ms.get('north_flow', 'N/A')} 亿")

        # 热门板块
        if ms.get("hot_sectors"):
            lines.append("")
            lines.append("### 热门板块")
            for s in ms["hot_sectors"][:5]:
                lines.append(f"- {s.get('name', '')} ({s.get('pct_change', 0):+.2f}%)")

        lines.extend(["", "---", "", "## 🎯 策略信号", ""])

        # 策略信号
        for strategy_name, signals in strategy_signals.items():
            lines.append(f"### {strategy_name}")
            if not signals:
                lines.append("> 无信号")
            for sig in signals[:5]:  # 最多5条
                symbol = sig.get("symbol", "?")
                name = sig.get("name", "")
                score = sig.get("score", 0)
                action = sig.get("action", "HOLD")
                reason = sig.get("reason", "")
                emoji = "🟢" if action == "BUY" else "🟡" if action == "HOLD" else "🔴"
                lines.append(f"- {emoji} **{symbol}** {name} | 评分:{score} | {action}")
                if reason:
                    lines.append(f"  > {reason}")
            lines.append("")

        # 选股结果（兼容 results 和 top 字段）
        candidates = selection_data.get("top") or selection_data.get("results", [])
        if candidates:
            # 股票池统计
            uni = selection_data.get("universe", "?")
            stats = selection_data.get("stats", {})
            req_start = selection_data.get("requested_start", "?")
            lines.extend(["", "---", "", "## 🎯 批量选股结果", ""])
            lines.append(f"- 股票池: {uni}")
            lines.append(f"- 扫描: {stats.get('total','?')} 只 | 成功: {stats.get('success','?')} | 失败: {stats.get('failed','?')}")
            lines.append(f"- 请求起始: {req_start}")
            lines.append("")

            for r in candidates[:5]:
                sym = r.get("symbol", "?")
                score = r.get("score", 0)
                close = r.get("latest_close", "?")
                src = r.get("data_source", "?")
                rows = r.get("rows", "?")
                start = r.get("actual_start", "?")
                end = r.get("actual_end", "?")
                reasons = ", ".join(r.get("reasons", [])[:3])
                risks_text = ", ".join(r.get("risks", [])[:2])
                cov_note = " ⚠️ 实际覆盖不全" if r.get("coverage_warning") else ""
                lines.append(f"- #{r.get('rank','?')} **{sym}** 评分{score}/100 收盘{close}{cov_note}")
                lines.append(f"  > 理由: {reasons}")
                if risks_text:
                    lines.append(f"  > 风险: {risks_text}")
                lines.append(f"  > 数据: {src} / {rows}行 / {start}~{end}")

        # AI 分析
        if ai_analysis:
            lines.extend(["", "---", "", "## 🤖 AI 综合分析", "", ai_analysis])

        lines.extend(["", "---", "", "## ⚠️ 免责声明", "",
            "> 本报告由系统根据数据和规则自动生成，仅供研究学习，不构成投资建议。投资有风险，入市需谨慎。"])

        report = "\n".join(lines)

        # 保存
        filename = f"report_{date.replace('-', '')}.md"
        filepath = os.path.join(self.config.output_dir, filename)
        with open(filepath, "w") as f:
            f.write(report)
        logger.info(f"报告已保存: {filepath}")

        return report

    def generate_json_signals(
        self, strategy_signals: Dict[str, List[Dict]]
    ) -> str:
        """生成结构化 JSON 信号（供下游系统消费）"""
        result = {
            "generated_at": datetime.now().isoformat(),
            "strategies": strategy_signals,
        }
        filepath = os.path.join(
            self.config.output_dir,
            f"signals_{datetime.now().strftime('%Y%m%d')}.json",
        )
        with open(filepath, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        return filepath
