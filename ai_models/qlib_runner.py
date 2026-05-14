"""
AI/ML 层：基于 qlib 的机器学习选股 (experimental)
==================================================
状态：experimental / not ready
原因：qlib 数据未下载，pipeline 未真实跑通。
"""

import os
import warnings
from typing import Dict, Optional

from loguru import logger

from config.settings import AIModelConfig, get_config

warnings.filterwarnings("ignore")

NOT_READY_MSG = (
    "experimental / not ready: qlib 数据未下载，pipeline 未真实跑通。"
    "请先执行: python -m qlib.cli.data qlib_data "
    "--target_dir ~/.qlib/qlib_data/cn_data --region cn"
)


class QlibRunner:
    """qlib AI 选股运行器 (experimental)"""

    def __init__(self, config: Optional[AIModelConfig] = None):
        self.config = config or get_config().ai_model
        self._initialized = False

    def init_qlib(self, data_dir: Optional[str] = None) -> bool:
        try:
            import qlib
            from qlib.config import REG_CN
            provider_uri = data_dir or self.config.qlib_data_dir
            if not os.path.exists(provider_uri):
                logger.warning(f"qlib 数据目录不存在: {provider_uri}")
                return False
            qlib.init(provider_uri=provider_uri, region=REG_CN)
            self._initialized = True
            logger.info(f"qlib 初始化完成: {provider_uri}")
            return True
        except ImportError:
            logger.warning("qlib 未安装")
            return False
        except Exception as e:
            logger.warning(f"qlib 初始化失败: {e}")
            return False

    def run_pipeline(self, *args, **kwargs) -> Dict:
        qlib_ok = False
        try:
            qlib_ok = self.init_qlib()
        except Exception:
            pass
        return {
            "status": "experimental",
            "message": NOT_READY_MSG,
            "qlib_available": qlib_ok,
        }


def run_quick_ai_select(symbols=None) -> Dict:
    runner = QlibRunner()
    return runner.run_pipeline()
