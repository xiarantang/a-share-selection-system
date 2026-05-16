# P8.1 数据源评估报告

> 日期：2026-05-16
> 目的：评估免费 A 股历史日 K 数据补充方案，确定优先接入顺序
> 约束：不破坏 v0.5 skill_fallback，不引入付费/API Key 作为唯一通道

---

## 1. 当前数据链路

```
get_daily_kline(symbol)
  ├── 1. akshare (ak.stock_zh_a_hist)               ← 主数据源
  ├── 2. skill_fallback (fetch_history_fallback.py)  ← ~120条K线，多源轮询
  ├── 3. 本地缓存 (parquet)                          ← 兜底
  └── 4. 返回空 DataFrame                           ← 失败
```

**痛点**：akshare 经常失败 → 大部分时间落在 skill_fallback（仅 ~120 条）→ 100% 覆盖不全标记。

---

## 2. 候选方案评估

### 2.1 baostock ⭐ 首选

| 维度 | 评价 |
|------|------|
| **是否免费** | ✅ 完全免费，无需注册 |
| **是否需要 API Key** | ✅ 不需要 |
| **250+ 条日 K** | ✅ 支持，历史数据从 1990 年起，通常 500-2000+ 条 |
| **稳定性** | ✅ 高。证券宝官网稳定运行多年，非爬虫方式 |
| **字段兼容成本** | 🟡 低。字段名需映射（date/close/open/high/low/volume/amount/pctChg），与 akshare 映射方式类似 |
| **安装** | `pip install baostock` |
| **失败回退** | 网络超时或服务不可用时，退回下一个数据源 |
| **代码量** | ~35 行新方法 `_fetch_baostock()` |

**接入方式**：
```python
import baostock as bs
lg = bs.login()  # 匿名登录即可，无需账号
rs = bs.query_history_k_data_plus(code,
    "date,open,high,low,close,volume,amount,pctChg,turn",
    start_date=start, end_date=end, frequency="d", adjustflag="2")
# 需 bs.logout() 释放连接
```
- symbol 需转换格式：`"000001"` → `"sz.000001"`（深市）/ `"sh.600519"`（沪市）
- `adjustflag="2"` 表示前复权

### 2.2 efinance ⭐ 次选

| 维度 | 评价 |
|------|------|
| **是否免费** | ✅ 完全免费 |
| **是否需要 API Key** | ✅ 不需要 |
| **250+ 条日 K** | ✅ 支持，基于东方财富接口，覆盖全 |
| **稳定性** | 🟡 中等。基于东方财富公开接口，接口可能变更 |
| **字段兼容成本** | 🟡 低。返回 DataFrame，字段名相似 |
| **安装** | `pip install efinance` |
| **失败回退** | 网络故障时退回下一数据源 |
| **代码量** | ~25 行 |
| **风险** | 东方财富接口非官方，未来可能变更；与 akshare 的东财数据源可能重叠 |

### 2.3 tushare（排除）

| 维度 | 评价 |
|------|------|
| 免费 | 🟡 部分免费，需注册获取 token |
| API Key | ❌ 需要 token |
| 限制 | 免费版有频率限制和积分门槛 |
| 结论 | ❌ 不推荐。token 增加小白门槛，免费版限制多 |

### 2.4 yfinance（排除）

| 维度 | 评价 |
|------|------|
| A股覆盖 | ❌ 仅部分 A 股（如 600519.SS），数据不完整 |
| 稳定性 | 🔴 国内访问 Yahoo 不稳定 |
| 结论 | ❌ 不推荐 |

---

## 3. 对比总表

| 方案 | 免费 | 无API Key | 250+条K线 | 稳定 | 兼容 | 推荐 |
|------|------|-----------|----------|------|-----|------|
| **baostock** | ✅ | ✅ | ✅ | ✅ 高 | 🟡 低 | 🥇 首选 |
| **efinance** | ✅ | ✅ | ✅ | 🟡 中 | 🟡 低 | 🥈 次选 |
| tushare | 🟡 | ❌ | 🟡 | 🟡 中 | 🟡 低 | ❌ |
| yfinance | ✅ | ✅ | ❌ | 🔴 低 | 🔴 高 | ❌ |

---

## 4. 推荐接入顺序

```
新 fallback 链路:
  ├── 1. akshare                     ← 保持（偶尔能通）
  ├── 2. baostock ⭐ 新增            ← 稳定主力
  ├── 3. efinance ⭐ 新增            ← 备用补充
  ├── 4. skill_fallback              ← 保留不变（最终兜底）
  ├── 5. 本地缓存                    ← 保留不变
  └── 6. 返回空                      ← 保留不变
```

**为什么是这个顺序？**
- akshare 偶尔能通（约 20% 概率），放最前不影响
- baostock 最稳定免费，优先接管
- efinance 覆盖面广，baostock 失败时补位
- skill_fallback 保留在最终兜底位置
- 缓存始终在最后

---

## 5. 最小实验方案

### 目标
验证 baostock 在本地环境稳定返回 10 只股票 250+ 条 K 线。

### 步骤
1. `pip install baostock`
2. 编写 `scripts/test_baostock.py` 对 static 前 10 只测试
3. 验收：10 只中 ≥8 只返回 250+ 条 K 线，不报错不崩溃

### 实验后行动
- 通过 → 进入 P8.1-1 正式接入
- 失败 → 跳过 baostock，实验 efinance

---

## 6. 不做什么

- ❌ 不修改评分逻辑
- ❌ 不删除 skill_fallback
- ❌ 不修改 UI
- ❌ 不引入 tushare / 商业 API
- ❌ 不改变 get_daily_kline() 签名
- ❌ 不改变 CLI 参数

## 7. 对 v0.5 的影响

- ✅ skill_fallback 保留在第 4 位
- ✅ 选股结果格式不变
- ✅ CLI 接口不变
- ✅ 新增数据源失败时自动回退
- ✅ 用户无感知，数据变多，覆盖不全提示减少
