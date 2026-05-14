"""
策略层：策略注册与调度
======================
管理多个选股策略，统一调度执行。
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from loguru import logger

from config.settings import StrategyConfig, get_config


class StrategyRegistry:
    """策略注册中心 - 管理所有启用的选股策略"""

    def __init__(self, config: Optional[StrategyConfig] = None):
        self.config = config or get_config().strategy
        self.skills_dir = Path(self.config.skills_dir)
        self._validate()

    def _validate(self):
        """验证策略 Skill 是否存在"""
        for s in self.config.enabled_strategies:
            skill_path = self.skills_dir / s / "SKILL.md"
            if not skill_path.exists():
                logger.warning(f"策略 Skill 未找到: {s} ({skill_path})")
            else:
                logger.info(f"策略已注册: {s}")

    def list_strategies(self) -> List[Dict]:
        """列出所有已注册策略"""
        result = []
        for s in self.config.enabled_strategies:
            skill_path = self.skills_dir / s
            info = {
                "name": s,
                "path": str(skill_path),
                "available": skill_path.exists(),
            }
            # 读取 SKILL.md 获取描述
            skill_md = skill_path / "SKILL.md"
            if skill_md.exists():
                with open(skill_md, "r") as f:
                    first_line = f.readline().strip().lstrip("#").strip()
                    info["description"] = first_line
            result.append(info)
        return result

    def find_scripts(self, strategy_name: Optional[str] = None) -> Dict[str, List]:
        """查找策略可执行的 Python 脚本"""
        targets = (
            [strategy_name]
            if strategy_name
            else self.config.enabled_strategies
        )
        result = {}
        for s in targets:
            script_dir = self.skills_dir / s / "scripts"
            if script_dir.exists():
                py_files = list(script_dir.rglob("*.py"))
                result[s] = [str(p) for p in py_files]
        return result

    def execute_strategy(
        self, strategy_name: str, script: str = "main.py", args: Optional[List] = None
    ) -> Dict:
        """执行指定策略的脚本并返回结果"""
        script_path = self.skills_dir / strategy_name / "scripts" / script
        if not script_path.exists():
            logger.error(f"策略脚本不存在: {script_path}")
            return {"error": f"Script not found: {script_path}"}

        try:
            cmd = ["python3", str(script_path)] + (args or [])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {
                "strategy": strategy_name,
                "script": script,
                "success": result.returncode == 0,
                "stdout": result.stdout[-5000:],
                "stderr": result.stderr[-2000:],
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"error": "执行超时"}
        except Exception as e:
            return {"error": str(e)}

    def run_all_strategies(self) -> Dict[str, Dict]:
        """执行所有已注册策略"""
        results = {}
        for s in self.config.enabled_strategies:
            logger.info(f"执行策略: {s}")
            results[s] = self.execute_strategy(s)
        return results
