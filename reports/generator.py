"""
报告层：选股报告生成器
======================
整合数据、策略信号、AI 分析、选股结果，生成每日选股报告。
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from loguru import logger

from config.settings import ReportConfig, get_config


class ReportGenerator:
    def __init__(self, config: Optional[ReportConfig] = None):
        self.config = config or get_config().report
        os.makedirs(self.config.output_dir, exist_ok=True)

    def generate_markdown_report(
        self, date: str, market_summary: Dict,
        strategy_signals: Dict[str, List[Dict]],
        ai_analysis: Optional[str] = None,
        selection_data: Optional[Dict] = None,
    ) -> str:
        lines = [
            f"# 🏦 A股智能选股日报",
            f"**日期**: {date}",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "", "---", "", "## 📊 市场概况", "",
        ]
        ms = market_summary
        if ms.get("up_count") is not None:
            lines.append(f"- 上涨家数: {ms.get('up_count', 'N/A')}")
            lines.append(f"- 下跌家数: {ms.get('down_count', 'N/A')}")
        else:
            lines.append("> 市场概况数据源不可用，本次报告仅基于个股K线评分")

        lines.extend(["", "---", "", "## 🎯 策略信号", ""])
        for strategy_name, signals in strategy_signals.items():
            lines.append(f"### {strategy_name}")
            if not signals:
                lines.append("> 无信号")
            for sig in signals[:5]:
                symbol = sig.get("symbol", "?")
                name = sig.get("name", "")
                score = sig.get("score", 0)
                action = sig.get("action", "HOLD")
                emoji = "🟢" if action == "BUY" else "🟡"
                lines.append(f"- {emoji} **{symbol}** {name} | 评分:{score} | {action}")
            lines.append("")

        # 验证摘要
        v = (selection_data or {}).get("validation")
        if v:
            lines.extend(["", "---", "", "## 📋 验证摘要", ""])
            lines.append(f"- 整体质量: {v.get('overall_quality','?')}")
            lines.append(f"- 覆盖不足率: {v.get('coverage_warning_ratio','?')} ({v.get('coverage_warning_ratio',0)*100:.0f}%)")
            lines.append(f"- 置信度分布: {v.get('confidence_dist',{})}")
            lines.append(f"- 决策分布: {v.get('decision_dist',{})}")
            lines.append(f"- 风险分布: {v.get('risk_level_dist',{})}")
            sd5 = dict(list((v.get('sector_dist') or {}).items())[:5])
            lines.append(f"- 行业分布(top5): {sd5}")
            if v.get('warnings'):
                for w in v['warnings']:
                    lines.append(f"- ⚠️ {w}")
            lines.append("")

        # 选股结果
        candidates = (selection_data or {}).get("top") or (selection_data or {}).get("results", [])
        if candidates:
            uni = selection_data.get("universe", {})
            stats = selection_data.get("stats", {})
            lines.extend(["", "---", "", "## 🎯 批量选股结果", ""])
            if isinstance(uni, dict):
                fb = uni.get("is_fallback")
                lines.append(f"- 请求股票池: {uni.get('universe_requested','?')}")
                lines.append(f"- 实际使用: {uni.get('universe_source','?')}")
                lines.append(f"- 是否fallback: {'是' if fb else '否'}")
                if fb:
                    lines.append(f"- fallback原因: {uni.get('fallback_reason','?')}")
            lines.append(f"- 扫描总数: {stats.get('total','?')}")
            lines.append(f"- 成功: {stats.get('success','?')} / 失败: {stats.get('failed','?')}")
            sd = stats.get("source_dist", {})
            if sd:
                lines.append(f"- 数据源分布: {sd}")
            lines.append("")

            for r in candidates[:5]:
                sym = r.get("symbol", "?")
                name = r.get("name", "")
                sector = r.get("sector", "")
                score = r.get("score", 0)
                dec = r.get("decision", "?")
                rl = r.get("risk_level", "?")
                conf = r.get("confidence", "?")
                close = r.get("latest_close", "?")
                src = r.get("data_source", "?")
                rows = r.get("rows", "?")
                start = r.get("actual_start", "?")
                end = r.get("actual_end", "?")
                reasons = ", ".join(r.get("reasons", [])[:3])
                risks_text = ", ".join(r.get("risks", [])[:2])
                cov = " ⚠️ 覆盖不全" if r.get("coverage_warning") else ""
                fs = r.get("factor_scores", {})
                fs_str = f"趋势{fs.get('trend','?')}/动量{fs.get('momentum','?')}/量能{fs.get('volume','?')}/风控{fs.get('risk','?')}/质量{fs.get('data_quality','?')}/形态{fs.get('pattern','?')}"
                label = f"{sym} {name} [{sector}]" if name else sym
                lines.append(f"- #{r.get('rank','?')} **{label}** 评分{score}/100 {dec} 风险{rl} 置信{conf} 收盘{close}{cov}")
                lines.append(f"  > 因子: {fs_str}")
                lines.append(f"  > 理由: {reasons}")
                if risks_text:
                    lines.append(f"  > 风险: {risks_text}")
                lines.append(f"  > 数据: {src} / {rows}行 / {start}~{end}")
                # explain（优雅降级：无字段时不报错）
                exp = r.get("explain", {})
                if exp:
                    lines.append(f"  > 📝 解释: {exp.get('summary', '')}")
                    strs = exp.get("strengths", [])
                    if strs:
                        lines.append(f"  > ✅ 加分: {' | '.join(strs)}")
                    ws = exp.get("weaknesses", [])
                    if ws and ws != ["暂无显著风险信号"]:
                        lines.append(f"  > ⚠️ 风险: {' | '.join(ws)}")
                    if exp.get("risk_note"):
                        lines.append(f"  > 📊 可靠性: {exp.get('risk_note', '')}")
                    if exp.get("confidence_note"):
                        lines.append(f"  > 💡 数据说明: {exp.get('confidence_note', '')}")

        # 历史窗口复盘
        bt = (selection_data or {}).get("backtest_validation")
        if bt:
            lines.extend(["", "---", "", "## 📈 历史窗口复盘（非未来收益表现）", ""])
            lines.append(f"- 验证数量: {bt.get('total_checked','?')} 跳过: {bt.get('skipped','?')}")
            lines.append(f"- win: {bt.get('win_count','?')} flat: {bt.get('flat_count','?')} loss: {bt.get('loss_count','?')}")
            lines.append(f"- 平均 forward return: {bt.get('avg_forward_return_pct','?')}%")
            lines.append(f"- 平均 max drawdown: {bt.get('avg_max_drawdown_pct','?')}%")
            lines.append(f"- best: {bt.get('best','?')}% worst: {bt.get('worst','?')}%")
            if bt.get('warnings'):
                for w in bt['warnings']:
                    lines.append(f"- ⚠️ {w}")

        # 本次运行复盘信息（优雅降级：无 run_metadata 时不显示）
        rm = (selection_data or {}).get("run_metadata")
        if rm:
            lines.extend(["", "---", "", "## 🧾 本次运行复盘信息", ""])
            entry_map = {"cli": "命令行", "ui": "可视化界面 (Streamlit)", "script": "脚本调用"}
            entry_label = entry_map.get(rm.get("entrypoint", ""), rm.get("entrypoint", ""))
            lines.append(f"- 生成时间: {rm.get('generated_at', '')}")
            lines.append(f"- 运行方式: {entry_label}")
            cmd = rm.get("command", "")
            if cmd:
                lines.append(f"- 命令/入口: `{cmd}`")
            p = rm.get("params", {})
            if p:
                p_parts = []
                for k in ["universe", "limit", "top", "start", "strategy_id"]:
                    if k in p:
                        label_map = {"universe": "股票池", "limit": "扫描数量",
                                     "top": "展示数量", "start": "起始日期",
                                     "strategy_id": "策略ID"}
                        p_parts.append(f"{label_map.get(k, k)}={p[k]}")
                if "symbols" in p:
                    p_parts.append(f"指定代码={p['symbols']}")
                if p_parts:
                    lines.append(f"- 参数: {' / '.join(p_parts)}")
            stg = rm.get("strategy", {})
            if stg:
                lines.append(f"- 策略: {stg.get('name', '')} ({stg.get('id', '')})")
            ds = rm.get("data_summary", {})
            dsd = ds.get("data_source_dist", {})
            if dsd:
                dsd_parts = [f"{k}: {v}只" for k, v in dsd.items()]
                lines.append(f"- 数据源分布: {' / '.join(dsd_parts)}")
            rs_rows = ds.get("rows_summary", {})
            if rs_rows:
                lines.append(f"- 数据条数: 最少 {rs_rows.get('min', '?')} / 最多 {rs_rows.get('max', '?')} / 平均 {rs_rows.get('avg', '?')} / 共 {rs_rows.get('count', '?')} 只")
            cwr = ds.get("coverage_warning_ratio")
            if cwr is not None:
                lines.append(f"- 覆盖不足率: {cwr:.0%}")
            rsum = rm.get("result_summary", {})
            oq = rsum.get("overall_quality", "")
            if oq:
                lines.append(f"- 整体质量: {oq}")
            ts_score = rsum.get("top_score")
            as_score = rsum.get("avg_score")
            if ts_score is not None or as_score is not None:
                lines.append(f"- Top 评分: {ts_score} / 平均评分: {as_score}")
            sp = rm.get("selection_path", "")
            if sp:
                lines.append(f"- 选股结果: `{sp}`")
            rp = rm.get("report_path", "")
            if rp:
                lines.append(f"- 报告路径: `{rp}`")

        if ai_analysis:
            lines.extend(["", "---", "", "## 🤖 AI 综合分析", "", ai_analysis])

        lines.extend(["", "---", "", "## ⚠️ 免责声明", "",
            "> 当前结果基于可用K线数据评分；若出现覆盖不足，决策置信度会下调。",
            "> 当前选股模型为规则因子评分（多因子分组，满分100），不代表未来表现。",
            "> 本报告由系统根据数据和规则自动生成，仅供研究学习，不构成投资建议。投资有风险，入市需谨慎。"])

        report = "\n".join(lines)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{ts}.md"
        filepath = os.path.join(self.config.output_dir, filename)
        with open(filepath, "w") as f:
            f.write(report)
        # 覆盖 latest
        import shutil
        shutil.copy(filepath, os.path.join(self.config.output_dir, "report_latest.md"))
        logger.info(f"报告已保存: {filepath} (+ report_latest.md)")
        return report

    def generate_json_signals(self, strategy_signals: Dict[str, List[Dict]]) -> str:
        result = {"generated_at": datetime.now().isoformat(), "strategies": strategy_signals}
        filepath = os.path.join(self.config.output_dir, f"signals_{datetime.now().strftime('%Y%m%d')}.json")
        with open(filepath, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        return filepath
