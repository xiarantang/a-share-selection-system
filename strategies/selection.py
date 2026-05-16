"""选股引擎 v2.1：可信度校准 + 覆盖降权
覆盖不足自动降 data_quality，confidence 联动 decision。"""
from typing import Dict, List, Tuple
import numpy as np, pandas as pd
from loguru import logger
from data.fetcher import AShareDataFetcher

def _safe_float(val, default=0.0):
    try: v=float(val); return v if pd.notna(v) and np.isfinite(v) else default
    except: return default

def compute_factors(df):
    if df.empty or "close" not in df.columns: return df
    close=df["close"].astype(float); volume=df["volume"].astype(float)
    df["MA5"]=close.rolling(5).mean(); df["MA20"]=close.rolling(20).mean(); df["MA60"]=close.rolling(60).mean()
    df["return_20d"]=close.pct_change(20)*100; df["return_60d"]=close.pct_change(60)*100
    v5=volume.rolling(5).mean(); v20=volume.rolling(20).mean(); df["vol_ratio"]=v5/(v20+1e-8)
    e12=close.ewm(span=12,adjust=False).mean(); e26=close.ewm(span=26,adjust=False).mean()
    df["MACD_DIF"]=e12-e26; df["MACD_DEA"]=df["MACD_DIF"].ewm(span=9,adjust=False).mean()
    df["MACD_HIST"]=2*(df["MACD_DIF"]-df["MACD_DEA"])
    d=close.diff(); g=d.where(d>0,0.0); l=(-d.where(d<0,0.0))
    ag=g.rolling(14).mean(); al=l.rolling(14).mean(); rs=ag/(al+1e-8); df["RSI14"]=100-(100/(1+rs))
    rm=close.rolling(20).max(); df["drawdown_20d"]=(close-rm)/(rm+1e-8)*100
    df["volatility_20d"]=close.pct_change().rolling(20).std()*np.sqrt(252)*100
    return df

def score_stock(df, has_coverage_warning=False):
    fs={"data_quality":0,"trend":0,"momentum":0,"volume":0,"risk":0,"pattern":0}
    reasons,risks,rlist=[],[],[]
    if df.empty or len(df)<20: return (0.0,reasons,risks,fs,{"error":"不足"},"avoid","high","low")
    latest=df.iloc[-1]; rows=len(df)
    dq_raw=10
    if rows<60: dq_raw-=5; risks.append(f"仅{rows}条K线")
    if rows<120: dq_raw-=3
    dq=min(dq_raw,10)
    if has_coverage_warning: dq=min(dq,6); risks.append("数据覆盖不足")
    if rows<120: dq=min(dq,5)
    if rows<60: dq=min(dq,3)
    fs["data_quality"]=max(0,dq)
    ma5=_safe_float(latest.get("MA5")); ma20=_safe_float(latest.get("MA20")); ma60=_safe_float(latest.get("MA60"))
    close_v=_safe_float(latest.get("close")); ret20=_safe_float(latest.get("return_20d"))
    ret60=_safe_float(latest.get("return_60d")); vol_ratio=_safe_float(latest.get("vol_ratio"),1.0)
    dif=_safe_float(latest.get("MACD_DIF")); dea=_safe_float(latest.get("MACD_DEA")); hist=_safe_float(latest.get("MACD_HIST"))
    rsi=_safe_float(latest.get("RSI14"),50); dd20=_safe_float(latest.get("drawdown_20d")); vol20=_safe_float(latest.get("volatility_20d"))
    fv={"MA5":round(ma5,2),"MA20":round(ma20,2),"MA60":round(ma60,2),"return_20d":round(ret20,2),"return_60d":round(ret60,2),"vol_ratio":round(vol_ratio,2),"MACD_DIF":round(dif,4),"MACD_DEA":round(dea,4),"MACD_HIST":round(hist,4),"RSI14":round(rsi,1),"drawdown_20d":round(dd20,2),"volatility_20d":round(vol20,2),"rows":rows}
    if ma5>ma20>ma60>0: fs["trend"]=25; reasons.append("多头排列")
    elif ma5>ma20 and close_v>ma60: fs["trend"]=20; reasons.append("短中期多头")
    elif close_v>ma60: fs["trend"]=15; reasons.append("站上MA60")
    elif ma5<ma20<ma60: fs["trend"]=3; risks.append("空头排列"); rlist.append("trend_bearish")
    else: fs["trend"]=8
    mom=0
    if 3<ret20<15: mom+=12; reasons.append(f"20日动量+{ret20:.1f}%")
    elif 0<ret20<=3: mom+=8
    elif ret20>15: mom+=4; risks.append(f"20日涨幅过大+{ret20:.1f}%"); rlist.append("overbought_20d")
    elif ret20<-10: mom+=2; risks.append(f"20日跌{ret20:.1f}%"); rlist.append("weak_momentum")
    else: mom+=5
    if ret60>0: mom+=6
    elif ret60<-20: mom+=2; risks.append(f"60日弱{ret60:.1f}%")
    else: mom+=4
    if dd20<-10: risks.append(f"20日回撤{dd20:.1f}%"); rlist.append("deep_drawdown")
    fs["momentum"]=min(20,mom)
    if 1.2<vol_ratio<3.0: fs["volume"]=15; reasons.append(f"量能{vol_ratio:.1f}x")
    elif 1.0<vol_ratio<=1.2: fs["volume"]=12
    elif vol_ratio>=3.0: fs["volume"]=8; risks.append(f"异常放量{vol_ratio:.1f}x")
    else: fs["volume"]=6
    rk=20
    if rsi>=80: rk-=8; risks.append(f"RSI过热{rsi:.0f}"); rlist.append("rsi_overheat")
    elif rsi>=70: rk-=5; risks.append(f"RSI偏高{rsi:.0f}"); rlist.append("rsi_high")
    elif rsi<=25: rk-=6; rlist.append("rsi_oversold")
    if ret20>20: rk-=6; rlist.append("chase_risk")
    if vol20>60: rk-=4; risks.append(f"高波动{vol20:.0f}%"); rlist.append("high_volatility")
    if rows<60: rk-=5; rlist.append("insufficient_data")
    fs["risk"]=max(0,rk)
    pat=0
    if dif>dea and dif>0: pat+=5; reasons.append("MACD零轴多头")
    elif dif>dea: pat+=3; reasons.append("MACD金叉")
    elif hist>0: pat+=1
    if len(df)>=3:
        ph=_safe_float(df.iloc[-2].get("MACD_HIST"))
        if ph<0 and hist>0: pat+=2; reasons.append("MACD翻红")
    if dd20>-5 and ret20>0 and ma5>ma20: pat+=3; reasons.append("回踩不破")
    fs["pattern"]=min(10,pat)
    total=sum(fs.values())
    # confidence
    risk_count=len(rlist)
    conf="high"
    if has_coverage_warning: conf="medium"
    if rows<120: conf="low"
    if risk_count>=3 or fs["risk"]<=8: conf=("low" if conf in ("low","medium") else "medium")
    # decision
    if total>=75 and fs["risk"]>=14 and conf!="low" and fs["data_quality"]>=6: dec="strong_watch"
    elif total>=55: dec="watch"
    elif total>=30: dec="neutral"
    else: dec="avoid"
    if dec=="strong_watch" and has_coverage_warning: risks.append("覆盖不足需谨慎")
    if fs["data_quality"]<5 and dec in ("strong_watch","watch"): dec="neutral"; risks.append("数据质量低决策降级")
    # risk_level
    if risk_count>=3 or fs["risk"]<=8: rl="high"
    elif risk_count>=1 or fs["risk"]<=14: rl="medium"
    else: rl="low"
    return (round(total,1), reasons, risks, fs, fv, dec, rl, conf)

class SelectionEngine:
    def __init__(self): self.fetcher=AShareDataFetcher()
    def select(self, symbols, start_date="2024-01-01"):
        results=[]
        for sym in symbols:
            df=self.fetcher.get_daily_kline(sym, start_date=start_date)
            if df is None or df.empty:
                results.append({"symbol":sym,"error":"获取失败","score":0,"rank":0,"confidence":"low","coverage_warning":False,"decision":"avoid","risk_level":"high"}); continue
            src=self.fetcher._last_source; rows=len(df)
            ast=str(df.index[0])[:10] if rows>0 else "N/A"; aen=str(df.index[-1])[:10] if rows>0 else "N/A"
            # coverage_warning（修正版）：容忍 1-3 天偏差，数据源可靠时放宽
            if ast == "N/A":
                has_cov = True
            elif rows >= 250 and src in ("akshare", "baostock"):
                from datetime import datetime as _dt2
                try:
                    ast_dt = _dt2.strptime(ast, "%Y-%m-%d")
                    req_dt = _dt2.strptime(start_date[:10], "%Y-%m-%d")
                    has_cov = (req_dt - ast_dt).days > 10
                except Exception:
                    has_cov = False
            else:
                has_cov = ast > start_date[:10]
            df=compute_factors(df)
            score,reasons,risks,fs,fv,dec,rl,conf=score_stock(df, has_coverage_warning=has_cov)
            lc=_safe_float(df.iloc[-1].get("close"))
            results.append({"symbol":sym,"score":score,"reasons":reasons,"risks":risks,"latest_close":round(lc,2),"data_source":src,"rows":rows,"actual_start":ast,"actual_end":aen,"factor_scores":fs,"factor_values":fv,"decision":dec,"risk_level":rl,"confidence":conf,"coverage_warning":has_cov})
        results.sort(key=lambda x: x["score"], reverse=True)
        for i,r in enumerate(results): r["rank"]=i+1
        return results
    def select_top(self, symbols, top=10, start_date="2024-01-01"):
        return self.select(symbols, start_date)[:top]
