"""选股结果验证模块。评估 selection JSON 质量，不预测收益。"""
from collections import Counter

def validate_selection(data):
    if not data: return None
    candidates = data.get("all") or data.get("top") or []
    if not candidates: return {"overall_quality":"poor","warnings":["无选股结果"]}
    total=len(candidates)
    success=[c for c in candidates if not c.get("error")]
    cov_count=sum(1 for c in success if c.get("coverage_warning"))
    cov_ratio=round(cov_count/total,2) if total>0 else 0
    conf_dist=dict(Counter(c.get("confidence","?") for c in success))
    dec_dist=dict(Counter(c.get("decision","?") for c in success))
    rl_dist=dict(Counter(c.get("risk_level","?") for c in success))
    sector_counts=Counter(c.get("sector","?") for c in success)
    src_dist=dict(Counter(c.get("data_source","?") for c in success))
    scores=[c.get("score",0) for c in success if c.get("score",0)>0]
    avg_score=round(sum(scores)/len(scores),1) if scores else 0
    top_score=max(scores) if scores else 0
    low_conf=sum(1 for c in success if c.get("confidence")=="low")
    high_risk=sum(1 for c in success if c.get("risk_level")=="high")
    warnings=[]
    quality="good"
    if len(success)==0: quality="poor"; warnings.append("无成功选股结果")
    elif cov_ratio>0.5: quality="usable_with_caution"; warnings.append(f"覆盖不足率高({cov_ratio:.0%})")
    if low_conf/max(total,1)>0.5: quality="usable_with_caution"; warnings.append(f"低置信度高({low_conf}/{total})")
    if high_risk/max(total,1)>0.3: quality="usable_with_caution"; warnings.append(f"高风险率高({high_risk}/{total})")
    sector_dist=dict(sector_counts.most_common(10))
    total_with_sector=sum(v for k,v in sector_dist.items() if k!="?")
    if total_with_sector>0:
        ts,tsc=sector_counts.most_common(1)[0]
        if tsc/total_with_sector>0.4: warnings.append(f"行业集中({ts}占{tsc/total_with_sector:.0%})")
    if cov_ratio>0: warnings.append(f"数据覆盖不足({cov_count}/{total})")
    return {"total_count":total,"success_count":len(success),"coverage_warning_count":cov_count,"coverage_warning_ratio":cov_ratio,"confidence_dist":conf_dist,"decision_dist":dec_dist,"risk_level_dist":rl_dist,"sector_dist":sector_dist,"data_source_dist":src_dist,"avg_score":avg_score,"top_score":top_score,"low_confidence_count":low_conf,"high_risk_count":high_risk,"sector_concentration_warning":any("行业集中" in w for w in warnings),"data_coverage_warning":cov_ratio>0,"overall_quality":quality,"warnings":warnings}
