"""
策略注册中心 - 元数据注册 (P8.4-1)
===================================
管理策略元数据（id/name/description/...），不执行外部脚本。
当前仅包含默认规则策略；未来可注册更多策略。
"""

from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# 模块级常量
# ---------------------------------------------------------------------------

DEFAULT_STRATEGY_ID = "default"

REQUIRED_FIELDS = (
    "id",
    "name",
    "description",
    "suitable_scenario",
    "risk_reminder",
    "enabled",
    "entry_function",
)

STRATEGY_REGISTRY: Dict[str, Dict[str, Any]] = {}

# ---------------------------------------------------------------------------
# 默认策略元数据
# ---------------------------------------------------------------------------

_DEFAULT_META: Dict[str, Any] = {
    "id": "default",
    "name": "默认规则策略",
    "description": (
        "基于趋势、动量、量能、风控、数据质量、形态六个因子打分排序，"
        "适合刚接触选股研究的使用者快速筛选候选标的。"
    ),
    "suitable_scenario": "A股主板 / 静态股票池研究筛选",
    "risk_reminder": (
        "本策略仅供研究学习，不构成投资建议，不承诺预测收益；"
        "数据质量会影响结果置信度。"
    ),
    "enabled": True,
    "entry_function": "strategies.selection:SelectionEngine",
}

# ---------------------------------------------------------------------------
# 注册 / 查询函数
# ---------------------------------------------------------------------------


def register_strategy(meta: Dict[str, Any]) -> None:
    """注册一条策略元数据。缺少必填字段时抛出 ValueError。"""
    missing = [f for f in REQUIRED_FIELDS if f not in meta]
    if missing:
        raise ValueError(f"策略元数据缺少必填字段: {missing}")
    sid = meta["id"]
    STRATEGY_REGISTRY[sid] = dict(meta)


def get_strategy(strategy_id: str) -> Optional[Dict[str, Any]]:
    """按 id 查询策略元数据，不存在返回 None。"""
    return STRATEGY_REGISTRY.get(strategy_id)


def list_strategies(enabled_only: bool = True) -> List[Dict[str, Any]]:
    """返回已注册策略列表。enabled_only=True 时仅返回启用项。"""
    items = list(STRATEGY_REGISTRY.values())
    if enabled_only:
        items = [s for s in items if s.get("enabled", True)]
    return items


def get_default_strategy() -> Dict[str, Any]:
    """返回默认策略元数据。"""
    return STRATEGY_REGISTRY[DEFAULT_STRATEGY_ID]


# ---------------------------------------------------------------------------
# 启动时注册默认策略
# ---------------------------------------------------------------------------

register_strategy(_DEFAULT_META)


# ---------------------------------------------------------------------------
# 兼容类 — 供 main.py / scripts/pipeline.py 旧式调用
# ---------------------------------------------------------------------------


class StrategyRegistry:
    """策略注册中心 — 兼容旧调用接口。

    不再扫描 Skill 目录、不再执行外部脚本。
    list_strategies() 返回的记录中额外附带 available/executable/type
    等兼容字段，使已有调用方无需改动。
    """

    def __init__(self, config=None):  # noqa: ARG002 – config 保留签名兼容
        pass

    @staticmethod
    def _enrich(meta: Dict[str, Any]) -> Dict[str, Any]:
        """为模块级元数据补上旧调用方期望的兼容字段。"""
        out: Dict[str, Any] = dict(meta)
        out.setdefault("available", True)
        out.setdefault("executable", False)
        out.setdefault("type", "builtin")
        return out

    def list_strategies(self, enabled_only: bool = True) -> List[Dict[str, Any]]:
        """列出策略（兼容旧接口）。"""
        return [self._enrich(s) for s in list_strategies(enabled_only=enabled_only)]

    def run_all_strategies(self):
        """兼容旧接口 — 不执行外部脚本，仅返回元数据标记。

        Returns
        -------
        (results, stats) : tuple
            results: dict[str, dict]  每条策略一条记录
            stats:  dict  executed/skipped_doc_only/failed 计数
        """
        results: Dict[str, Dict[str, Any]] = {}
        stats = {"executed": 0, "skipped_doc_only": 0, "failed": 0}
        for meta in list_strategies(enabled_only=True):
            name = meta["id"]
            results[name] = {
                "strategy": name,
                "success": True,
                "note": "P8.4-1 注册骨架阶段，仅返回元数据，不执行外部脚本",
                "type": "builtin",
            }
            stats["executed"] += 1
        return results, stats

    def execute_strategy(self, strategy_name: str, **_kwargs) -> Dict[str, Any]:
        """兼容旧接口 — 不执行外部脚本。"""
        meta = get_strategy(strategy_name)
        if meta is None:
            return {
                "strategy": strategy_name,
                "success": False,
                "error": f"策略未注册: {strategy_name}",
            }
        return {
            "strategy": strategy_name,
            "success": True,
            "note": "P8.4-1 注册骨架阶段，仅返回元数据，不执行外部脚本",
            "type": "builtin",
        }
