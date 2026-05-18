#!/usr/bin/env python3
"""
A股智能选股系统 - Streamlit 本地可视化 UI (P7.0)
=================================================
小白也能用的一键选股界面。选参数、开始选股、看结果。
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
from strategies.selection import SelectionEngine, build_run_metadata
from strategies.registry import DEFAULT_STRATEGY_ID, get_strategy, list_strategies
from validation.selection_validator import validate_selection
from validation.backtest_validator import run_backtest_validation
from reports.generator import ReportGenerator
from data.fetcher import AShareDataFetcher


FALLBACK_SCRIPT = Path.home() / ".agents/skills/a-share-data/scripts/fetch_history_fallback.py"

# ========== 展示层中文化映射（只改 UI 展示，不改底层 JSON/CSV/策略字段） ==========
DECISION_ZH = {"strong_watch": "强观察", "watch": "观察", "neutral": "中性", "avoid": "回避"}
RISK_ZH = {"low": "低风险", "medium": "中风险", "high": "高风险"}
CONFIDENCE_ZH = {
    "high": "高置信度",
    "medium": "中置信度",
    "low": "低置信度",
}

# ---------- UI 展示 helper（仅用于页面渲染，不改底层字段） ----------
RISK_TEXT_COLOR = {"low": "#155724", "medium": "#856404", "high": "#721c24"}
RISK_BG_COLOR = {"low": "#d4edda", "medium": "#fff3cd", "high": "#f8d7da"}
DECISION_TEXT_COLOR = {"strong_watch": "#155724", "watch": "#1b5e20", "neutral": "#856404", "avoid": "#721c24"}
DECISION_BG_COLOR = {"strong_watch": "#d4edda", "watch": "#e8f5e9", "neutral": "#fff3cd", "avoid": "#f8d7da"}

FACTOR_ICONS = {
    "trend": "📈 趋势", "momentum": "🚀 动量", "volume": "📊 量能",
    "risk": "🛡️ 风控", "data_quality": "📋 数据质量", "pattern": "🔮 形态",
}


def _badge(text: str, bg: str, color: str) -> str:
    """生成 HTML 彩色标签（仅用于 st.markdown unsafe_allow_html）。"""
    return (
        f'<span style="background:{bg};color:{color};padding:2px 10px;'
        f'border-radius:4px;font-weight:bold;font-size:0.9em;">{text}</span>'
    )


def risk_badge(level: str) -> str:
    """风险等级 HTML 标签。"""
    return _badge(
        RISK_ZH.get(level, level),
        RISK_BG_COLOR.get(level, "#e2e3e5"),
        RISK_TEXT_COLOR.get(level, "#6c757d"),
    )


def decision_badge(dec: str) -> str:
    """决策标签 HTML 标签。"""
    return _badge(
        DECISION_ZH.get(dec, dec),
        DECISION_BG_COLOR.get(dec, "#e2e3e5"),
        DECISION_TEXT_COLOR.get(dec, "#6c757d"),
    )


def friendly_date_range(start: str, end: str) -> str:
    """日期区间 + 友好'约近 X 个月'提示。"""
    try:
        s = datetime.strptime(start, "%Y-%m-%d")
        e = datetime.strptime(end, "%Y-%m-%d")
        months = round((e - s).days / 30)
        suffix = f"（约近 {months} 个月）" if months >= 1 else ""
        return f"{start} ~ {end} {suffix}"
    except Exception:
        return f"{start} ~ {end}"


def risk_alert(level: str, message: str):
    """按风险等级用不同颜色展示提示：高→error 红 / 中→warning 橙 / 低→info 绿灰。"""
    if level == "high":
        st.error(message)
    elif level == "medium":
        st.warning(message)
    else:
        st.info(message)


# ========== 页面配置 ==========
st.set_page_config(
    page_title="A股智能选股系统",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ========== 初始化 session_state ==========
for key in ["selection_data", "backtest_per_stock", "backtest_summary", "last_params", "last_strategy"]:
    if key not in st.session_state:
        st.session_state[key] = None


# ========== 函数：执行选股 ==========
def run_selection(universe: str, limit: int, top: int, start_date: str,
                  strategy_id: str = DEFAULT_STRATEGY_ID):
    """执行选股流程，复用底层模块。返回 selection_data dict。"""
    # 校验策略
    strategy_meta = get_strategy(strategy_id)
    if strategy_meta is None or not strategy_meta.get("enabled", True):
        raise ValueError(f"策略 '{strategy_id}' 不可用或已禁用")

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

    strategy_info = {
        "id": strategy_meta["id"],
        "name": strategy_meta["name"],
        "description": strategy_meta["description"],
        "suitable_scenario": strategy_meta["suitable_scenario"],
        "risk_reminder": strategy_meta["risk_reminder"],
    }

    data = {
        "generated_at": datetime.now().isoformat(),
        "strategy_id": strategy_id,
        "strategy": strategy_info,
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
    # 构建 run_metadata（只读取已有数据，不重新跑评分）
    ui_params = {
        "universe": universe,
        "limit": limit,
        "top": top,
        "start": start_date,
        "strategy_id": strategy_id,
    }
    data["run_metadata"] = build_run_metadata(
        data, params=ui_params, entrypoint="ui", command="streamlit run app.py",
    )
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
            "决策": DECISION_ZH.get(r.get("decision", "?"), r.get("decision", "?")),
            "风险": RISK_ZH.get(r.get("risk_level", "?"), r.get("risk_level", "?")),
            "置信度": CONFIDENCE_ZH.get(r.get("confidence", "?"), r.get("confidence", "?")),
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
    st.dataframe(df, width="stretch", hide_index=True)


# ========== 辅助：流程引导卡片 ==========
def render_step_guide():
    """未选股前的引导卡片：简洁操作引导，含首次安装提示。"""
    st.markdown("### 👋 欢迎使用 A 股智能选股系统")

    # 可选第三级兜底提示（仅未安装时显示）
    if not FALLBACK_SCRIPT.exists():
        with st.container(border=True):
            st.info(
                "💡 **可选**：双击 `scripts/install_fallback.command` 可安装第三级兜底数据通道（skill_fallback），"
                "在网络不稳定时多一层保障。系统已内置 baostock（约 570 条日 K），不装也能正常使用。"
            )

    # 核心操作引导
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("#### ① 在左侧选参数")
            st.markdown("保持默认即可（static 55只精选 / 扫描 10 只），然后点击左侧 **🚀 开始选股** 按钮")
    with col2:
        with st.container(border=True):
            st.markdown("#### ② 等待结果")
            st.markdown("预计 30-60 秒，完成后可直接查看排名、评分和风险提示")


# ========== 主界面 ==========
st.title("🏦 A股智能选股系统")
st.caption("选参数 → 开始选股 → 看结果 · 小白也能用 · 仅供研究学习，不构成投资建议")

st.success("✅ **系统就绪** — 点击左侧「🚀 开始选股」即可开始，预计 30-60 秒出结果")
if not FALLBACK_SCRIPT.exists():
    st.info(
        "💡 **可选**：未安装第三级兜底数据通道（skill_fallback）。系统已内置 baostock（约 570 条日 K），"
        "可以正常使用。如需在网络不稳定时多一层保障，可双击 `scripts/install_fallback.command` 安装。"
    )

# 首次使用检查区（可折叠）
with st.expander("🔧 环境检查（点击展开）", expanded=False):
    import sys as _sys
    import glob as _glob

    # 逐项检查
    py_ok = True  # Python 已经在运行，必然 OK
    fallback_ok = FALLBACK_SCRIPT.exists()
    cache_dir = Path("data/cache")
    cache_count = len(list(cache_dir.glob("*.parquet"))) if cache_dir.exists() else 0
    cache_ok = cache_count > 0

    latest_json = Path("reports/output/selection_latest.json")
    latest_ok = latest_json.exists()
    _latest_ts = ""
    _latest_cnt = 0
    if latest_ok:
        import json as _json
        try:
            with open(latest_json) as _f:
                _latest = _json.load(_f)
            _latest_ts = _latest.get("generated_at", "")[:19]
            _latest_cnt = len(_latest.get("top", []))
        except Exception:
            latest_ok = False

    st.markdown("#### 📋 环境自检")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"{'✅' if py_ok else '❌'} **Python**: {_sys.version.split()[0]}")
        st.markdown(f"{'✅' if fallback_ok else '💡'} **第三级兜底**: {'已安装' if fallback_ok else '未安装（可选）'}")
    with col_b:
        st.markdown(f"{'✅' if cache_ok else '⚠️'} **本地缓存**: {cache_count} 个文件")
        if latest_ok:
            st.markdown(f"✅ **最近选股**: {_latest_ts} (Top {_latest_cnt} 只)")
        else:
            st.markdown("⏳ **最近选股**: 暂无")

    # 汇总判定
    if fallback_ok and cache_ok:
        st.success("✅ 环境就绪，可以开始选股。点击左侧「🚀 开始选股」按钮即可。")
    elif not fallback_ok:
        st.info(
            "💡 第三级兜底数据通道（skill_fallback）未安装。系统已内置 baostock（约 570 条日 K），"
            "可以正常选股。如需在网络不稳定时多一层保障，可双击 `scripts/install_fallback.command` 安装。"
        )
    else:
        st.info("💡 环境基本就绪，但本地缓存为空。首次选股会慢一些（需要拉取数据），之后会变快。")

# ---- 左侧栏 ----
with st.sidebar:
    st.header("⚙️ 选股参数")

    universe = st.selectbox(
        "股票池",
        options=["static", "hs300", "top_amount"],
        format_func=lambda x: {"static": "static (55只精选)", "hs300": "沪深300", "top_amount": "成交额TOP"}.get(x, x),
        help="static: 55只精选A股 | hs300: 沪深300成分股 | top_amount: 全市场成交额排序",
        label_visibility="collapsed",
    )

    # 策略选择器
    enabled_strategies = list_strategies(enabled_only=True)
    strategy_options = {s["id"]: s["name"] for s in enabled_strategies}
    strategy_ids = list(strategy_options.keys())
    default_sid = DEFAULT_STRATEGY_ID if DEFAULT_STRATEGY_ID in strategy_ids else (strategy_ids[0] if strategy_ids else DEFAULT_STRATEGY_ID)
    selected_strategy = st.selectbox(
        "策略",
        options=strategy_ids,
        format_func=lambda x: strategy_options.get(x, x),
        index=strategy_ids.index(default_sid) if default_sid in strategy_ids else 0,
        help="当前为规则策略选择，不改变评分公式；仅供研究学习，不构成投资建议。",
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
    st.caption("首次体验建议保持默认参数，预计 30-60 秒出结果")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_select = st.button("🚀 开始选股", type="primary", width="stretch")
    with col_btn2:
        btn_backtest = st.button("📈 历史复盘", width="stretch",
                                 disabled=(st.session_state.selection_data is None),
                                 help="对 Top 候选做 In-Sample 窗口验证（较慢）")

    st.markdown("---")
    st.caption("""⚠️ **免责声明**：本系统根据数据和规则自动生成选股结果，仅供研究学习，不构成投资建议。A股市场风险较高，投资需谨慎。""")

# ---- 主区域 ----
if btn_select:
    with st.spinner("⏳ 正在选股中，通常需要 30-60 秒。正在拉取数据、计算评分，请不要关闭页面..."):
        try:
            data = run_selection(universe, limit, top, start_str, strategy_id=selected_strategy)
            st.session_state.selection_data = data
            st.session_state.backtest_per_stock = None
            st.session_state.backtest_summary = None
            st.session_state.last_params = {
                "universe": universe, "limit": limit, "top": top, "start": start_str,
            }
            st.session_state.last_strategy = selected_strategy

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
                    "请先检查网络连接，然后重试。如持续失败，可安装第三级兜底数据通道：双击 `scripts/install_fallback.command`。"
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
    universe_meta = data.get("universe", {})
    stats = data.get("stats", {})
    top_results = data.get("top", [])
    v = data.get("validation", {})

    # ====== Top3 速览卡片（选股完成第一眼就能看到） ======
    if top_results:
        st.markdown("### 🏆 Top 3 候选速览")
        t3_cols = st.columns(3)
        medals = ["🥇", "🥈", "🥉"]
        for i, r in enumerate(top_results[:3]):
            with t3_cols[i]:
                with st.container(border=True):
                    sym = r.get("symbol", "?")
                    name = r.get("name", "")
                    score = r.get("score", 0)
                    dec = r.get("decision", "?")
                    rl = r.get("risk_level", "?")
                    exp = r.get("explain", {})
                    summary = exp.get("summary", "")
                    st.markdown(f"**{medals[i]} #{r.get('rank', i+1)} {sym} {name}**")
                    st.markdown(
                        f"**{score}分** "
                        f'{decision_badge(dec)} {risk_badge(rl)}',
                        unsafe_allow_html=True,
                    )
                    if summary:
                        st.caption(f"_{summary}_")
    else:
        st.warning("无候选结果。可能原因：数据全部获取失败，请检查网络或稍后重试。")

    # ====== 紧凑数据概览（合并原信息条 + 覆盖摘要 + 验证摘要） ======
    st.markdown("---")
    source_dist = stats.get("source_dist", {})
    source_str = " ".join(f"{k}:{v}" for k, v in source_dist.items())
    cov = build_coverage_summary(data.get("all", []), data.get("requested_start", ""))
    quality = v.get("overall_quality", "?") if v else "?"
    quality_short = {"good": "🟢 良好", "usable_with_caution": "🟡 需谨慎", "poor": "🔴 差"}.get(quality, quality)

    ov_cols = st.columns(4)
    with ov_cols[0]:
        st.caption("股票池")
        st.markdown(f"**{universe_meta.get('universe_source','?')}** | 扫描 {stats.get('total','?')} 只")
    with ov_cols[1]:
        st.caption("数据区间")
        st.markdown(f"**{friendly_date_range(cov.get('earliest_actual', '?'), cov.get('latest_actual', '?'))}**")
    with ov_cols[2]:
        st.caption("K线 / 数据源")
        st.markdown(f"平均 **{cov.get('avg_rows','?')}** 条 | {source_str or 'N/A'}")
    with ov_cols[3]:
        st.caption("整体质量")
        st.markdown(f"**{quality_short}**")

    # 紧凑提示行
    # 当前策略说明（克制展示）
    strategy_display = data.get("strategy", {})
    if strategy_display:
        st.caption(
            f"📋 当前策略：{strategy_display.get('name', '?')} | "
            f"适用场景：{strategy_display.get('suitable_scenario', '')} | "
            f"⚠️ {strategy_display.get('risk_reminder', '')}"
        )

    warn_parts = []
    if cov.get("coverage_warn_count", 0) > 0:
        warn_parts.append(f"覆盖不全: {cov['coverage_warn_count']}/{cov['total_success']}只")
    if v and v.get("high_risk_count", 0) > 0:
        warn_parts.append(f"高风险: {v['high_risk_count']}/{v.get('total_count','?')}")
    if warn_parts:
        st.warning(" | ".join(warn_parts))

    if universe_meta.get("is_fallback"):
        st.warning(f"⚠️ 股票池回退到 static: {universe_meta.get('fallback_reason','?')}")

    if cov.get("coverage_warn_count", 0) > cov.get("total_success", 1) // 2:
        st.info(
            "覆盖不全不是报错：系统会自动降低评分和置信度。"
            "结果仍可用于研究观察，但不应当直接作为买卖建议。"
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
                if val == "强观察":
                    return "background-color: #d4edda; color: #155724"
                elif val == "观察":
                    return "background-color: #e8f5e9"
                elif val == "回避":
                    return "background-color: #f8d7da; color: #721c24"
                return ""

            styled_df = df.style.map(color_decision, subset=["决策"])
            st.dataframe(
                styled_df,
                width="stretch",
                hide_index=True,
                column_config={
                    "决策": st.column_config.TextColumn(help="强观察 > 观察 > 中性 > 回避"),
                    "风险": st.column_config.TextColumn(help="低风险 / 中风险 / 高风险"),
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

                # 标题加覆盖警告（中文决策+风险）
                dec_zh_detail = DECISION_ZH.get(dec, dec)
                rl_zh_detail = RISK_ZH.get(rl, rl)
                title = f"#{r.get('rank','?')} {sym} {name} [{r.get('sector','')}] — {score}/100 {dec_zh_detail} · {rl_zh_detail}"
                if cov_warn:
                    title += " ⚠️覆盖不全"

                with st.expander(title):
                    # explain（优雅降级：无字段时不显示）
                    exp = r.get("explain", {})
                    if exp:
                        st.markdown(f"**📝 {exp.get('summary', '')}**")
                        strs = exp.get("strengths", [])
                        ws = exp.get("weaknesses", [])
                        if strs or (ws and ws != ["暂无显著风险信号"]):
                            ec1, ec2 = st.columns(2)
                            with ec1:
                                if strs:
                                    st.caption(f"✅ 主要加分: {' | '.join(strs)}")
                            with ec2:
                                if ws and ws != ["暂无显著风险信号"]:
                                    st.caption(f"⚠️ 主要风险: {' | '.join(ws)}")
                        if exp.get("confidence_note"):
                            with st.expander("📊 可靠性说明"):
                                st.caption(exp.get("risk_note", ""))
                                st.caption(exp.get("confidence_note", ""))
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(
                            f"**评分**: {score}/100 | **决策**: "
                            f'{decision_badge(dec)} | **风险**: '
                            f'{risk_badge(rl)} | **置信度**: {CONFIDENCE_ZH.get(conf, conf)}',
                            unsafe_allow_html=True,
                        )
                        st.markdown(f"**收盘价**: {r.get('latest_close','?')} | **数据源**: {r.get('data_source','?')} | **K线条数**: {r.get('rows','?')}")
                        st.markdown(f"**数据区间**: {friendly_date_range(actual_start, actual_end)}")
                        if cov_warn:
                            st.warning(f"⚠️ 数据覆盖不全：请求起始日早于实际数据起始日 {actual_start}，模型已自动下调评分和置信度。")
                    with col_b:
                        st.markdown("**因子得分**:")
                        factor_parts = []
                        for fk, label in FACTOR_ICONS.items():
                            fv_score = fs.get(fk, "?")
                            factor_parts.append(f"{label}: {fv_score}")
                        st.markdown(" / ".join(factor_parts))
                        # 技术指标详情（默认收起）
                        with st.expander("📐 技术指标详情"):
                            st.markdown(
                                f"- MA5: {fv.get('MA5','?')} | MA20: {fv.get('MA20','?')} | MA60: {fv.get('MA60','?')}\n"
                                f"- 20日动量: {fv.get('return_20d','?')}%\n"
                                f"- RSI(14): {fv.get('RSI14','?')}\n"
                                f"- 波动率(20日): {fv.get('volatility_20d','?')}%"
                            )
                    if reasons:
                        st.success("✅ " + reasons)
                    if risks_text:
                        risk_alert(rl, "⚠️ " + risks_text)

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
    # 未选股时的引导
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
