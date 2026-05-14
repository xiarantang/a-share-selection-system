#!/usr/bin/env python3
"""
A股智能选股系统 - Streamlit 本地可视化 UI (P6.0)
=================================================
小白也能用的一键选股界面。
复用全部现有底层模块，不复制评分逻辑。
仅供研究学习，不构成投资建议。
"""

import os
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from data.universe import get_universe, lookup_meta
from strategies.selection import SelectionEngine
from validation.selection_validator import validate_selection
from validation.backtest_validator import run_backtest_validation
from reports.generator import ReportGenerator
from data.fetcher import AShareDataFetcher


# ========== 页面配置 ==========
st.set_page_config(
    page_title="A股智能选股系统",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ========== 初始化 session_state ==========
for key in ["selection_data", "backtest_per_stock", "backtest_summary", "last_params"]:
    if key not in st.session_state:
        st.session_state[key] = None


# ========== 函数：执行选股 ==========
def run_selection(universe: str, limit: int, top: int, start_date: str):
    """执行选股流程，复用底层模块。返回 selection_data dict。"""
    symbols, meta = get_universe(universe, limit=limit)
    engine = SelectionEngine()
    all_results = engine.select(symbols, start_date=start_date)

    # 注入 name/sector
    for r in all_results:
        info = lookup_meta(r["symbol"])
        r["name"] = info.get("name", "")
        r["sector"] = info.get("sector", "")

    # 统计
    stats = {"total": len(symbols), "success": 0, "failed": 0, "source_dist": {}}
    for r in all_results:
        if r.get("error"):
            stats["failed"] += 1
        else:
            stats["success"] += 1
            src = r.get("data_source", "unknown")
            stats["source_dist"][src] = stats["source_dist"].get(src, 0) + 1

    top_results = [r for r in all_results if not r.get("error")][:top]

    data = {
        "generated_at": datetime.now().isoformat(),
        "requested_start": start_date,
        "universe": meta,
        "stats": {
            **stats,
            "universe_requested": meta["universe_requested"],
            "universe_source": meta["universe_source"],
            "is_fallback": meta["is_fallback"],
            "fallback_reason": meta.get("fallback_reason", ""),
        },
        "top": top_results,
        "all": all_results,
    }
    data["validation"] = validate_selection(data)
    return data


# ========== 函数：执行复盘 ==========
def run_backtest(data: dict, top: int):
    """执行历史窗口复盘。复用 validation.backtest_validator。"""
    fetcher = AShareDataFetcher()
    per_stock, summary = run_backtest_validation(data, top=top, fetcher=fetcher)
    # 回写到 data
    data["backtest_validation"] = summary
    data["backtest_validation_details"] = per_stock
    return per_stock, summary


# ========== 函数：生成报告 ==========
def generate_report(data: dict) -> str:
    """生成 Markdown 报告。复用 reports.generator。"""
    reporter = ReportGenerator()
    report_md = reporter.generate_markdown_report(
        date=datetime.now().strftime("%Y-%m-%d"),
        market_summary={},
        strategy_signals={},
        selection_data=data,
    )
    return report_md


# ========== 辅助：构建展示用 DataFrame ==========
def build_candidates_df(top_results: list) -> pd.DataFrame:
    """将 top 候选转为展示用 DataFrame。"""
    rows = []
    for r in top_results:
        fs = r.get("factor_scores", {})
        rows.append({
            "排名": r.get("rank", "?"),
            "代码": r.get("symbol", "?"),
            "名称": r.get("name", ""),
            "行业": r.get("sector", ""),
            "评分": r.get("score", 0),
            "决策": r.get("decision", "?"),
            "风险": r.get("risk_level", "?"),
            "置信度": r.get("confidence", "?"),
            "收盘价": r.get("latest_close", "?"),
            "趋势": fs.get("trend", "?"),
            "动量": fs.get("momentum", "?"),
            "量能": fs.get("volume", "?"),
            "风控": fs.get("risk", "?"),
            "数据质量": fs.get("data_quality", "?"),
            "形态": fs.get("pattern", "?"),
            "数据源": r.get("data_source", "?"),
            "K线条数": r.get("rows", "?"),
            "覆盖不全": "⚠️" if r.get("coverage_warning") else "",
        })
    return pd.DataFrame(rows)


def build_backtest_df(per_stock: list) -> pd.DataFrame:
    """将复盘结果转为展示用 DataFrame。"""
    rows = []
    for r in per_stock:
        if r.get("skipped"):
            rows.append({
                "代码": r.get("symbol", "?"),
                "状态": f"跳过({r.get('skipped_reason','?')})",
                "区间": "-",
                "持有天数": "-",
                "起始价": "-",
                "终止价": "-",
                "Forward收益%": "-",
                "最大回撤%": "-",
                "波动率%": "-",
                "结论": "-",
            })
        else:
            rows.append({
                "代码": r.get("symbol", "?"),
                "名称": r.get("name", ""),
                "评分": r.get("score", 0),
                "决策": r.get("decision", "?"),
                "置信度": r.get("confidence", "?"),
                "区间": f"{r.get('start_date','?')}~{r.get('end_date','?')}",
                "持有天数": r.get("holding_days", "?"),
                "起始价": r.get("start_price", "?"),
                "终止价": r.get("end_price", "?"),
                "Forward收益%": r.get("forward_return_pct", "?"),
                "最大回撤%": r.get("max_drawdown_pct", "?"),
                "波动率%": r.get("volatility_pct", "?"),
                "结论": r.get("result_label", "?"),
            })
    return pd.DataFrame(rows)


# ========== 辅助：渲染验证摘要 ==========
def render_validation(v: dict):
    """渲染验证摘要区域。"""
    if not v:
        st.warning("无验证数据")
        return

    quality = v.get("overall_quality", "?")
    quality_icon = {"good": "🟢", "usable_with_caution": "🟡", "poor": "🔴"}.get(quality, "")
    st.markdown(f"### {quality_icon} 整体质量: **{quality}**")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总数", v.get("total_count", "?"))
    col2.metric("成功", v.get("success_count", "?"))
    col3.metric("覆盖不足率", f"{v.get('coverage_warning_ratio',0)*100:.0f}%")
    col4.metric("平均分/最高分", f"{v.get('avg_score','?')}/{v.get('top_score','?')}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**置信度分布**")
        st.json(v.get("confidence_dist", {}))
    with col2:
        st.write("**决策分布**")
        st.json(v.get("decision_dist", {}))
    with col3:
        st.write("**风险分布**")
        st.json(v.get("risk_level_dist", {}))

    sector_dist = v.get("sector_dist", {})
    if sector_dist:
        st.write("**行业分布 (Top 10)**")
        st.bar_chart(pd.DataFrame(
            list(sector_dist.items()), columns=["行业", "数量"]
        ).set_index("行业"))

    warnings = v.get("warnings", [])
    if warnings:
        st.warning("⚠️ " + " | ".join(warnings))


# ========== 辅助：渲染复盘摘要 ==========
def render_backtest_summary(summary: dict, per_stock: list):
    """渲染复盘摘要 + 详情表格。"""
    if not summary:
        st.warning("无复盘数据")
        return

    st.markdown("### 📊 复盘汇总 (In-Sample，不预测未来)")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("验证总数", summary.get("total_checked", "?"))
    col2.metric("跳过", summary.get("skipped", "?"))
    col3.metric("🟢 Win", summary.get("win_count", "?"))
    col4.metric("🟡 Flat", summary.get("flat_count", "?"))
    col5.metric("🔴 Loss", summary.get("loss_count", "?"))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("平均收益%", summary.get("avg_forward_return_pct", "?"))
    col2.metric("平均回撤%", summary.get("avg_max_drawdown_pct", "?"))
    col3.metric("最佳%", summary.get("best", "?"))
    col4.metric("最差%", summary.get("worst", "?"))

    if summary.get("warnings"):
        for w in summary["warnings"]:
            st.info(f"⚠️ {w}")

    st.markdown("### 📋 逐只复盘详情")
    df = build_backtest_df(per_stock)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ========== 主界面 ==========
st.title("🏦 A股智能选股系统")
st.caption("小白也能用的一键选股 · 仅供研究学习，不构成投资建议")

# ---- 左侧栏 ----
with st.sidebar:
    st.header("⚙️ 选股参数")

    universe = st.selectbox(
        "股票池",
        options=["static", "hs300", "top_amount"],
        format_func=lambda x: {"static": "static (55只精选)", "hs300": "沪深300", "top_amount": "成交额TOP"}.get(x, x),
        help="static: 55只精选A股 | hs300: 沪深300成分股 | top_amount: 全市场成交额排序",
    )
    limit = st.slider("扫描数量", min_value=10, max_value=55, value=20, step=5,
                      help="从股票池中取多少只来评分")
    top = st.slider("展示数量", min_value=3, max_value=20, value=10, step=1,
                    help="Top N 候选")
    start_date = st.date_input(
        "数据起始日期",
        value=pd.to_datetime("2024-01-01"),
        min_value=pd.to_datetime("2020-01-01"),
        max_value=pd.to_datetime(datetime.now().strftime("%Y-%m-%d")),
    )
    start_str = start_date.strftime("%Y-%m-%d") if hasattr(start_date, "strftime") else str(start_date)

    st.markdown("---")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_select = st.button("🚀 开始选股", type="primary", use_container_width=True)
    with col_btn2:
        btn_backtest = st.button("📈 历史复盘", use_container_width=True,
                                 disabled=(st.session_state.selection_data is None),
                                 help="对 Top 候选做 In-Sample 窗口验证（较慢）")

    st.markdown("---")
    st.caption("""**免责声明**：本系统根据数据和规则自动生成选股结果，仅供研究学习，不构成投资建议。A股市场风险较高，投资需谨慎。""")

# ---- 主区域 ----
if btn_select:
    with st.spinner("正在选股中，请稍候..."):
        try:
            data = run_selection(universe, limit, top, start_str)
            st.session_state.selection_data = data
            st.session_state.backtest_per_stock = None
            st.session_state.backtest_summary = None
            st.session_state.last_params = {
                "universe": universe, "limit": limit, "top": top, "start": start_str,
            }
            st.success(f"选股完成！扫描 {data['stats']['total']} 只，成功 {data['stats']['success']} 只")
        except Exception as e:
            st.error(f"选股失败: {e}")

if btn_backtest and st.session_state.selection_data is not None:
    with st.spinner("正在复盘验证中，请稍候（较慢）..."):
        try:
            per_stock, summary = run_backtest(st.session_state.selection_data, top)
            st.session_state.backtest_per_stock = per_stock
            st.session_state.backtest_summary = summary
            st.success("复盘完成")
        except Exception as e:
            st.error(f"复盘失败: {e}")

# ---- 结果展示 ----
if st.session_state.selection_data is not None:
    data = st.session_state.selection_data

    # 顶部信息条
    universe_meta = data.get("universe", {})
    stats = data.get("stats", {})
    info_cols = st.columns(4)
    info_cols[0].info(f"**股票池**: {universe_meta.get('universe_source','?')}")
    info_cols[1].info(f"**是否fallback**: {'是' if universe_meta.get('is_fallback') else '否'}")
    info_cols[2].info(f"**扫描/成功/失败**: {stats.get('total','?')}/{stats.get('success','?')}/{stats.get('failed','?')}")
    info_cols[3].info(f"**数据请求起始**: {data.get('requested_start','?')}")

    if universe_meta.get("is_fallback"):
        st.warning(f"⚠️ 股票池 fallback: {universe_meta.get('fallback_reason','?')}")

    # Tab 切换
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 候选表格", "📋 验证摘要", "📈 历史复盘", "📄 报告"])

    with tab1:
        top_results = data.get("top", [])
        if not top_results:
            st.warning("无候选结果")
        else:
            st.caption(f"Top {len(top_results)} 候选 | 评分从高到低")

            df = build_candidates_df(top_results)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "决策": st.column_config.TextColumn(help="strong_watch>watch>neutral>avoid"),
                    "风险": st.column_config.TextColumn(help="low/medium/high"),
                    "覆盖不全": st.column_config.TextColumn(width="small"),
                },
            )

            # 逐只展开详情
            st.markdown("---")
            st.markdown("### 🔍 逐只详情")
            for r in top_results:
                sym = r.get("symbol", "?")
                name = r.get("name", "")
                score = r.get("score", 0)
                dec = r.get("decision", "?")
                rl = r.get("risk_level", "?")
                conf = r.get("confidence", "?")
                reasons = ", ".join(r.get("reasons", [])[:5])
                risks_text = ", ".join(r.get("risks", [])[:5])
                cov = " ⚠️ 覆盖不全" if r.get("coverage_warning") else ""
                fs = r.get("factor_scores", {})
                fv = r.get("factor_values", {})

                with st.expander(f"#{r.get('rank','?')} {sym} {name} [{r.get('sector','')}] — {score}/100 {dec} {rl}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**评分**: {score}/100 | **决策**: {dec} | **风险**: {rl} | **置信度**: {conf}")
                        st.markdown(f"**收盘价**: {r.get('latest_close','?')} | **数据源**: {r.get('data_source','?')} | **K线条数**: {r.get('rows','?')}{cov}")
                        st.markdown(f"**数据区间**: {r.get('actual_start','?')} ~ {r.get('actual_end','?')}")
                    with col_b:
                        st.markdown("**因子得分**:")
                        st.markdown(f"趋势{fs.get('trend','?')}/动量{fs.get('momentum','?')}/量能{fs.get('volume','?')}/风控{fs.get('risk','?')}/数据质量{fs.get('data_quality','?')}/形态{fs.get('pattern','?')}")
                        st.markdown("**因子数值**:")
                        st.markdown(f"MA5:{fv.get('MA5','?')} MA20:{fv.get('MA20','?')} MA60:{fv.get('MA60','?')} | 20日动量:{fv.get('return_20d','?')}% | RSI:{fv.get('RSI14','?')} | 波动率:{fv.get('volatility_20d','?')}%")
                    if reasons:
                        st.success("✅ " + reasons)
                    if risks_text:
                        st.error("⚠️ " + risks_text)

    with tab2:
        v = data.get("validation")
        render_validation(v)

    with tab3:
        if st.session_state.backtest_per_stock is not None:
            render_backtest_summary(st.session_state.backtest_summary, st.session_state.backtest_per_stock)
        else:
            st.info("请点击左侧「📈 历史复盘」按钮进行 In-Sample 窗口验证（较慢，需要重新拉取数据）")

    with tab4:
        with st.spinner("正在生成报告..."):
            report_md = generate_report(data)
        st.markdown(report_md)
        st.info("📁 报告已保存至 `reports/output/report_latest.md`")

    # 底部产品目标提示
    st.markdown("---")
    st.caption("🎯 产品目标：打造小白也能用的可视化 A 股选股系统。当前为本地 Streamlit 第一版。CLI 命令仍是底层引擎和验收入口。")

else:
    # 未选股时的占位提示
    st.info("👈 在左侧栏设置参数，点击「🚀 开始选股」按钮开始")


# ========== 底部免责 ==========
st.markdown("---")
st.markdown(
    "> ⚠️ **免责声明**：本系统由程序根据数据和规则自动生成选股结果，**仅供研究学习，不构成投资建议**。"
    "当前选股模型为规则因子评分（多因子分组，满分100），不是收益预测。"
    "A 股市场风险较高，投资需谨慎。"
    "\n\n"
    "> 📊 **数据说明**：数据来源 akshare + 多源 fallback（腾讯/新浪/雪球/东财）+ 本地缓存。"
    "当 akshare 不可用时会自动降级。若出现「覆盖不全」提示，表示数据起始日晚于请求起始日，模型已自动下调评分和置信度。"
)
