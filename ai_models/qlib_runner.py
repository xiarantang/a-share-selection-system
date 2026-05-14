"""
AI/ML 层：基于 qlib 的机器学习选股
===================================
整合微软 qlib 平台，提供因子工程 + 模型训练 + 预测 pipeline。
"""

import os
import warnings
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from loguru import logger

from config.settings import AIModelConfig, get_config

warnings.filterwarnings("ignore")


class QlibRunner:
    """qlib AI 选股运行器"""

    def __init__(self, config: Optional[AIModelConfig] = None):
        self.config = config or get_config().ai_model
        self._initialized = False

    def init_qlib(self, data_dir: Optional[str] = None):
        """初始化 qlib 环境"""
        try:
            import qlib
            from qlib.config import REG_CN

            provider_uri = data_dir or self.config.qlib_data_dir
            qlib.init(
                provider_uri=provider_uri,
                region=REG_CN,
            )
            self._initialized = True
            logger.info(f"qlib 初始化完成: {provider_uri}")
        except ImportError:
            logger.error("qlib 未安装: pip install pyqlib")
            raise
        except Exception as e:
            logger.error(f"qlib 初始化失败: {e}")
            logger.info("请先下载 qlib 数据: python -m qlib.cli.data qlib_data "
                        "--target_dir ~/.qlib/qlib_data/cn_data --region cn")
            raise

    def prepare_features(
        self,
        stock_pool: List[str],
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """准备特征数据"""
        if not self._initialized:
            self.init_qlib()

        from qlib.data import D
        from qlib.data.dataset import DatasetH
        from qlib.data.dataset.handler import DataHandlerLP

        # 定义特征列
        fields = [
            # 价量特征
            "Ref($close, -1) / $close - 1",
            "Mean($close, 5) / $close",
            "Mean($close, 20) / $close",
            "Mean($volume, 5) / ($volume + 1e-8)",
            "Std($close, 20) / $close",
            "($high - $low) / $close",
            "($close - $open) / $close",
            # 技术指标
            "RSI($close, 14)",
            "MACD($close, 12, 26)",
            # 收益特征
            "Ref($close, -20) / $close - 1",
            "Ref($close, -60) / $close - 1",
        ]

        labels = [f"Ref($close, -{self.config.horizon}) / $close - 1"]

        handler_conf = {
            "start_time": start_date,
            "end_time": end_date,
            "fit_start_time": start_date,
            "fit_end_time": end_date,
            "instruments": stock_pool if stock_pool else "csi300",
        }

        try:
            dataset = DatasetH(
                handler=DataHandlerLP(
                    instruments=stock_pool or "csi300",
                    start_time=start_date,
                    end_time=end_date,
                    fit_start_time=start_date,
                    fit_end_time=end_date,
                    infer_processors=[],
                ),
                segments={
                    "train": (start_date, end_date),
                    "test": (start_date, end_date),
                },
            )
            df = dataset.prepare(
                ["train"],
                col_set=["feature", "label"],
                data_key=DataHandlerLP.DK_I,
            )
            return df
        except Exception as e:
            logger.error(f"特征准备失败: {e}")
            return pd.DataFrame()

    def train_model(
        self,
        df: pd.DataFrame,
        model_type: Optional[str] = None,
        horizon: Optional[int] = None,
    ) -> Dict:
        """训练 ML 模型"""
        if not self._initialized:
            self.init_qlib()

        from qlib.contrib.model.gbdt import LGBModel
        from qlib.contrib.data.handler import Alpha158
        from qlib.data.dataset import TSDatasetH

        model_type = model_type or self.config.model_type
        horizon = horizon or self.config.horizon

        logger.info(f"训练 {model_type} 模型, 预测周期={horizon}天")

        try:
            if model_type == "lightgbm":
                model = LGBModel(
                    loss="mse",
                    num_leaves=64,
                    learning_rate=0.05,
                    n_estimators=200,
                    early_stopping_rounds=20,
                    feature_fraction=0.8,
                    bagging_fraction=0.8,
                    bagging_freq=1,
                    num_threads=4,
                )
                # 简化训练流程
                model.fit(df["feature"], df["label"])
                pred = model.predict(df["feature"])

                return {
                    "model": "lightgbm",
                    "horizon": horizon,
                    "predictions": pred.values[:10].tolist() if hasattr(pred, "values") else [],
                    "status": "trained",
                }
            else:
                logger.warning(f"不支持的模型类型: {model_type}")
                return {"error": f"Unsupported model: {model_type}"}
        except Exception as e:
            logger.error(f"模型训练失败: {e}")
            return {"error": str(e)}

    def run_pipeline(
        self,
        stock_pool: Optional[List[str]] = None,
        start_date: str = "2024-01-01",
        end_date: Optional[str] = None,
    ) -> Dict:
        """一键运行 AI 选股 pipeline"""
        end_date = end_date or pd.Timestamp.now().strftime("%Y-%m-%d")

        result = {
            "status": "pending",
            "qlib_initialized": self._initialized,
            "config": {
                "model": self.config.model_type,
                "target": self.config.target,
                "horizon": self.config.horizon,
            },
        }

        try:
            # 初始化
            if not self._initialized:
                self.init_qlib()

            # 准备数据
            df = self.prepare_features(stock_pool, start_date, end_date)
            result["features_count"] = len(df) if isinstance(df, pd.DataFrame) else 0

            # 训练
            train_result = self.train_model(df)
            result.update(train_result)
            result["status"] = "success"

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)

        return result


def run_quick_ai_select(symbols: Optional[List[str]] = None) -> Dict:
    """快速 AI 选股入口"""
    runner = QlibRunner()
    return runner.run_pipeline(stock_pool=symbols)
