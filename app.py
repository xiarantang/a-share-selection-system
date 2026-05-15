#!/usr/bin/env python3
"""
A股智能选股系统 - Streamlit 本地可视化 UI (P7.0)
=================================================
小白也能用的一键选股界面。三步引导、错误提示友好化、数据覆盖可视化。
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


FALLBACK_SCRIPT = Path.home() / ".agents/skills/a-share-data/scripts/fetch_history_fallback.py"


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
        data_range = f"{r.get('actual_start','?')}~{r.get('actual_end','?')}"
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
            "数据区间": data_range,
            "数据源": r.get("data_source", "?"),
            "K线条数": r.get("rows", "?"),
            "覆盖": "⚠️不全" if r.get("coverage_warning") else "✓",
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


# ========== 辅助：构建数据覆盖摘要 ==========
def build_coverage_summary(all_results: list, requested_start: str) -> dict:
    """从选股结果中汇总数据覆盖情况。"""
    success = [r for r in all_results if not r.get("error")]
    if not success:
        return {"min_rows": 0, "max_rows": 0, "avg_rows": 0,
                "coverage_warn_count": 0, "total_success": 0,
                "earliest_actual": "N/A", "latest_actual": "N/A"}
    rows_list = [r.get("rows", 0) for r in success]
    cov_warn = sum(1 for r in success if r.get("coverage_warning"))
    starts = [r.get("actual_start", "9999") for r in success if r.get("actual_start")]
    ends = [r.get("actual_end", "0000") for r in success if r.get("actual_end")]
    return {
        "min_rows": min(rows_list), "max_rows": max(rows_list),
        "avg_rows": round(sum(rows_list) / len(rows_list)),
        "coverage_warn_count": cov_warn, "total_success": len(success),
        "earliest_actual": min(starts) if starts else "N/A",
        "latest_actual": max(ends) if ends else "N/A",
    }


# ========== 辅助：渲染验证摘要 ==========
def render_validation(v: dict):
    """渲染验证摘要区域。"""
    if not v:
        st.warning("无验证数据")
        return

    quality = v.get("overall_quality", "?")
    quality_icon = {"good": "🟢", "usable_with_caution": "🟡", "poor": "🔴"}.get(quality, "")
    quality_label = {"good": "数据充足，风险可控", "usable_with_caution": "覆盖不足或置信度偏低，结果仅供参考", "poor": "数据质量差，不建议参考"}.get(quality, "")
    st.markdown(f"### {quality_icon} 整体质量: **{quality}**")
    st.caption(quality_label)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总候选数", v.get("total_count", "?"))
    col2.metric("选股成功", v.get("success_count", "?"))
    col3.metric("覆盖不足率", f"{v.get('coverage_warning_ratio',0)*100:.0f}%")
    col4.metric("平均分 / 最高分", f"{v.get('avg_score','?')} / {v.get('top_score','?')}")

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
        for w in warnings:
            st.warning(f"⚠️ {w}")


# ========== 辅助：渲染复盘摘要 ==========
def render_backtest_summary(summary: dict, per_stock: list):
    """渲染复盘摘要 + 详情表格。"""
    if not summary:
        st.warning("无复盘数据")
        return

    st.markdown("### 📊 复盘汇总 (In-Sample，不预测未来)")
    st.caption("对已有K线做窗口内验证，不代表未来收益。")

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


# ========== 辅助：三步引导卡片 ==========
def render_step_guide():
    """未选股前的引导卡片。"""
    st.markdown("### 👋 欢迎使用 A 股智能选股系统")
    st.caption("三步完成选股，小白也能轻松上手。")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("#### ① 选参数")
            st.markdown("在左侧栏选择：\n- 股票池（精选55只/沪深300/成交额TOP）\n- 扫描数量和展示数量\n- 数据起始日期")
    with col2:
        with st.container(border=True):
            st.markdown("#### ② 开始选股")
            st.markdown("点击左侧 **🚀 开始选股** 按钮\n系统会自动拉取数据、评分、排序\n稍等片刻即可看到结果")
    with col3:
        with st.container(border=True):
            st.markdown("#### ③ 看结果")
            st.markdown("选股完成后切换 Tab：\n- 🎯 候选表格\n- 📋 验证摘要\n- 📈 历史复盘\n- 📄 完整报告")


# ========== 主界面 ==========
st.title("🏦 A股智能选股系统")
st.caption("三步完成选股 · 小白也能用 · 仅供研究学习，不构成投资建议")

if FALLBACK_SCRIPT.exists():
    st.info("📡 数据通道：当前主要使用 A 股备用数据通道（skill_fallback）。如果 akshare 临时不可用，系统仍可正常出结果。")
else:
    st.warning("⚠️ 缺少 A 股备用数据通道。首次使用请先运行 `scripts/install_fallback.command`，否则新数据可能拉取失败。")

# ---- 左侧栏 ----
with st.sidebar:
    st.header("⚙️ 选股参数")

    st.markdown("**① 选择股票池**")
    universe = st.selectbox(
        "股票池",
        options=["static", "hs300", "top_amount"],
        format_func=lambda x: {"static": "static (55只精选)", "hs300": "沪深300", "top_amount": "成交额TOP"}.get(x, x),
        help="static: 55只精选A股 | hs300: 沪深300成分股 | top_amount: 全市场成交额排序",
        label_visibility="collapsed",
    )
    limit = st.slider("扫描数量", min_value=10, max_value=55, value=10, step=5,
                      help="首次体验建议保持 10 只，通常需要 30-60 秒。数量越多等待越久。")
    top = st.slider("展示数量", min_value=3, max_value=20, value=5, step=1,
                    help="Top N 候选")
    start_date = st.date_input(
        "数据起始日期",
        value=pd.to_datetime("2024-01-01"),
        min_value=pd.to_datetime("2020-01-01"),
        max_value=pd.to_datetime(datetime.now().strftime("%Y-%m-%d")),
    )
    start_str = start_date.strftime("%Y-%m-%d") if hasattr(start_date, "strftime") else str(start_date)

    st.markdown("---")
    st.markdown("**② 一键运行**")
    st.caption("首次体验建议保持默认 static + 10 只，预计 30-60 秒。看到备用数据源提示不代表系统坏了。")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_select = st.button("🚀 开始选股", type="primary", use_container_width=True)
    with col_btn2:
        btn_backtest = st.button("📈 历史复盘", use_container_width=True,
                                 disabled=(st.session_state.selection_data is None),
                                 help="对 Top 候选做 In-Sample 窗口验证（较慢）")

    st.markdown("---")
    st.markdown("**③ 查看结果**")
    st.caption("选股完成后，在右侧切换 Tab 查看候选表格、验证摘要、历史复盘和完整报告。")

    st.markdown("---")
    st.caption("""⚠️ **免责声明**：本系统根据数据和规则自动生成选股结果，仅供研究学习，不构成投资建议。A股市场风险较高，投资需谨慎。""")

# ---- 主区域 ----
if btn_select:
    with st.spinner("⏳ 正在选股中，通常需要 30-60 秒。正在拉取数据、计算评分，请不要关闭页面..."):
        try:
            data = run_selection(universe, limit, top, start_str)
            st.session_state.selection_data = data
            st.session_state.backtest_per_stock = None
            st.session_state.backtest_summary = None
            st.session_state.last_params = {
                "universe": universe, "limit": limit, "top": top, "start": start_str,
            }

            # 人性化提示
            success_count = data["stats"]["success"]
            failed_count = data["stats"]["failed"]
            total_count = data["stats"]["total"]
            source_dist = data["stats"].get("source_dist", {})

            if success_count > 0:
                msg = f"✅ 选股完成！成功 {success_count}/{total_count} 只"
                # 提示数据源情况
                if source_dist.get("skill_fallback", 0) > 0 and "akshare" not in source_dist:
                    msg += "。当前使用 A 股备用数据通道，属于正常运行；数据覆盖可能不全，系统已自动下调置信度。"
                elif source_dist.get("skill_fallback", 0) > 0:
                    msg += "。部分数据来自 A 股备用数据通道。"
                st.success(msg)
            else:
                st.error(
                    f"❌ 选股异常：{total_count} 只股票全部获取失败。"
                    "请先确认已安装 A 股备用数据通道：运行 `scripts/install_fallback.command`，然后重试。"
                )

        except Exception as e:
            st.error(f"❌ 选股过程出错。可能原因：网络不通、数据接口临时故障。\n\n技术详情: {e}")

if btn_backtest and st.session_state.selection_data is not None:
    with st.spinner("⏳ 正在复盘验证中，请稍候（需重新拉取数据，较慢）..."):
        try:
            per_stock, summary = run_backtest(st.session_state.selection_data, top)
            st.session_state.backtest_per_stock = per_stock
            st.session_state.backtest_summary = summary

            checked = summary.get("total_checked", 0)
            skipped = summary.get("skipped", 0)
            if skipped > 0:
                st.success(f"复盘完成：验证 {checked} 只，跳过 {skipped} 只")
            else:
                st.success(f"复盘完成：验证 {checked} 只")
        except Exception as e:
            st.error(f"❌ 复盘过程出错。可能原因：网络不通、数据接口临时故障。\n\n技术详情: {e}")

# ---- 结果展示 ----
if st.session_state.selection_data is not None:
    data = st.session_state.selection_data

    # 顶部信息条
    universe_meta = data.get("universe", {})
    stats = data.get("stats", {})
    info_cols = st.columns(4)
    info_cols[0].info(f"**股票池**: {universe_meta.get('universe_source','?')}")
    info_cols[1].info(f"**数据起始请求**: {data.get('requested_start','?')}")
    info_cols[2].info(f"**扫描 / 成功 / 失败**: {stats.get('total','?')} / {stats.get('success','?')} / {stats.get('failed','?')}")
    source_dist = stats.get("source_dist", {})
    source_str = " ".join(f"{k}:{v}" for k, v in source_dist.items())
    info_cols[3].info(f"**数据源**: {source_str or 'N/A'}")

    if universe_meta.get("is_fallback"):
        st.warning(f"⚠️ 股票池回退到 static: {universe_meta.get('fallback_reason','?')}")

    # 数据覆盖摘要卡片
    cov = build_coverage_summary(data.get("all", []), data.get("requested_start", ""))
    if cov["total_success"] > 0:
        cov_cols = st.columns(5)
        cov_cols[0].metric("数据范围", f"{cov['earliest_actual']} ~ {cov['latest_actual']}")
        cov_cols[1].metric("最少K线", cov["min_rows"])
        cov_cols[2].metric("最多K线", cov["max_rows"])
        cov_cols[3].metric("平均K线", cov["avg_rows"])
        cov_cols[4].metric("覆盖不全", f"{cov['coverage_warn_count']}/{cov['total_success']}只",
                           delta="⚠️" if cov["coverage_warn_count"] > cov["total_success"]//2 else None)

    # 纯文本数据覆盖摘要（便于验收检测，放在 Tab 外确保渲染）
    st.info(
        f"📊 数据区间: {cov['earliest_actual']} ~ {cov['latest_actual']} "
        f"| K线: {cov['min_rows']}-{cov['max_rows']} 条（平均 {cov['avg_rows']} 条）"
        f"| 覆盖不全: {cov['coverage_warn_count']}/{cov['total_success']} 只"
    )
    if cov["coverage_warn_count"] > 0:
        st.warning(
            "覆盖不全不是报错：当前备用数据通道通常提供约 120 条 K 线。"
            "系统会自动降低数据质量评分和置信度，结果仍可用于研究观察，但不应当直接作为买卖建议。"
        )

    # Tab 切换
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 候选表格", "📋 验证摘要", "📈 历史复盘", "📄 报告"])

    with tab1:
        top_results = data.get("top", [])
        if not top_results:
            st.warning("无候选结果。可能原因：数据全部获取失败，请检查网络或稍后重试。")
        else:
            st.caption(f"Top {len(top_results)} 候选 | 评分从高到低 | 数据区间供参考")

            df = build_candidates_df(top_results)
            # 决策列着色
            def color_decision(val):
                if val == "strong_watch":
                    return "background-color: #d4edda; color: #155724"
                elif val == "watch":
                    return "background-color: #e8f5e9"
                elif val == "avoid":
                    return "background-color: #f8d7da; color: #721c24"
                return ""

            styled_df = df.style.applymap(color_decision, subset=["决策"])
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "决策": st.column_config.TextColumn(help="strong_watch(强观察)>watch(观察)>neutral(中性)>avoid(回避)"),
                    "风险": st.column_config.TextColumn(help="low/medium/high"),
                    "覆盖": st.column_config.TextColumn(width="small", help="✓正常 ⚠️不全=数据起始日晚于请求日"),
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
                cov_warn = r.get("coverage_warning")
                fs = r.get("factor_scores", {})
                fv = r.get("factor_values", {})
                actual_start = r.get("actual_start", "?")
                actual_end = r.get("actual_end", "?")

                # 标题加覆盖警告
                title = f"#{r.get('rank','?')} {sym} {name} [{r.get('sector','')}] — {score}/100 {dec} {rl}"
                if cov_warn:
                    title += " ⚠️覆盖不全"

                with st.expander(title):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**评分**: {score}/100 | **决策**: {dec} | **风险**: {rl} | **置信度**: {conf}")
                        st.markdown(f"**收盘价**: {r.get('latest_close','?')} | **数据源**: {r.get('data_source','?')} | **K线条数**: {r.get('rows','?')}")
                        st.markdown(f"**数据区间**: {actual_start} ~ {actual_end}")
                        if cov_warn:
                            st.warning(f"⚠️ 数据覆盖不全：请求起始日早于实际数据起始日 {actual_start}，模型已自动下调评分和置信度。")
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
            st.info("💡 尚未运行历史复盘。请点击左侧「📈 历史复盘」按钮，对 Top 候选做 In-Sample 窗口验证。")
            st.caption("复盘需要重新拉取数据，较慢。结果仅供参考，不代表未来收益。")

    with tab4:
        with st.spinner("⏳ 正在生成报告..."):
            report_md = generate_report(data)
        st.markdown(report_md)
        st.info("📁 报告已保存至 `reports/output/report_latest.md`")

    # 底部产品目标提示
    st.markdown("---")
    st.caption("🎯 产品目标：打造小白也能用的可视化 A 股选股系统。当前为本地 Streamlit 版。CLI 命令仍是底层引擎和验收入口。")

else:
    # 未选股时的三步引导
    render_step_guide()


# ========== 底部免责 ==========
st.markdown("---")
st.markdown(
    "> ⚠️ **免责声明**：本系统由程序根据数据和规则自动生成选股结果，**仅供研究学习，不构成投资建议**。"
    "当前选股模型为规则因子评分（多因子分组，满分100），不是收益预测。"
    "A 股市场风险较高，投资需谨慎。"
    "\n\n"
    "> 📊 **数据说明**：数据来源 akshare + 多源 fallback（腾讯/新浪/雪球/东财）+ 本地缓存。"
    "当 akshare 不可用时会自动降级到备用数据源。若出现「覆盖不全」提示，表示数据起始日晚于请求起始日，"
    "模型已自动下调评分和置信度。数据覆盖不足时不构成选股建议。"
)
