"""
A股智能选股系统 - 全局配置
============================
统一管理所有模块的参数，支持 .env 覆盖。
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import yaml
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class DataConfig:
    """数据层配置"""
    cache_dir: str = str(PROJECT_ROOT / "data" / "cache")
    refresh_interval: int = 3600
    universe: str = "all"
    custom_symbols: List[str] = field(default_factory=list)


@dataclass
class StrategyConfig:
    """策略层配置"""
    enabled_strategies: List[str] = field(default_factory=lambda: [
        "a-share-strategy-mainboard-multi-swing-defensive",
        "macd-trend-resonance-stock-picker",
        "macd-second-golden-cross",
    ])
    skills_dir: str = os.path.expanduser("~/.agents/skills")


@dataclass
class BacktestConfig:
    """回测层配置"""
    initial_cash: float = 1_000_000.0
    commission: float = 0.0003
    stamp_duty: float = 0.001
    start_date: str = "2024-01-01"
    end_date: Optional[str] = None


@dataclass
class AIModelConfig:
    """AI/ML 层配置"""
    qlib_data_dir: str = os.path.expanduser("~/.qlib/qlib_data/cn_data")
    model_type: str = "lightgbm"
    target: str = "return"
    horizon: int = 5


@dataclass
class AgentConfig:
    """Agent 层配置"""
    mcp_cn_stock_url: str = os.getenv(
        "MCP_CN_STOCK_URL",
        "http://82.156.17.205/cnstock/mcp"
    )
    llm_api_url: str = os.getenv("LLM_API_URL", "https://api.deepseek.com/v1")
    llm_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "deepseek-chat")


@dataclass
class PaperTradingConfig:
    """模拟交易层配置"""
    initial_cash: float = 1_000_000.0
    t_plus_1: bool = True
    lot_size: int = 100


@dataclass
class ReportConfig:
    """报告层配置"""
    output_dir: str = str(PROJECT_ROOT / "reports" / "output")
    enable_push: bool = False
    push_channels: List[str] = field(default_factory=list)


@dataclass
class SystemConfig:
    """系统总配置"""
    data: DataConfig = field(default_factory=DataConfig)
    strategy: StrategyConfig = field(default_factory=StrategyConfig)
    backtest: BacktestConfig = field(default_factory=BacktestConfig)
    ai_model: AIModelConfig = field(default_factory=AIModelConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    paper_trading: PaperTradingConfig = field(default_factory=PaperTradingConfig)
    report: ReportConfig = field(default_factory=ReportConfig)

    @classmethod
    def from_yaml(cls, path: str) -> "SystemConfig":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data) if data else cls()

    def to_yaml(self, path: str):
        import dataclasses
        with open(path, "w") as f:
            yaml.dump(dataclasses.asdict(self), f, allow_unicode=True)


_config: Optional[SystemConfig] = None


def get_config() -> SystemConfig:
    global _config
    if _config is None:
        _config = SystemConfig()
    return _config


def init_config(config: SystemConfig):
    global _config
    _config = config
