"""
策略层：策略注册与调度
======================
管理多个选股策略，自动扫描脚本，优先使用 real scripts。
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from config.settings import StrategyConfig, get_config

# 各 Skill 的优先执行脚本映射
PRIORITY_SCRIPTS = {
    "a-share-strategy-mainboard-multi-swing-defensive": "daily_decisions.py",
    "macd-trend-resonance-stock-picker": None,     # 文档型
    "macd-second-golden-cross": None,               # 文档型
}


class StrategyRegistry:
    """策略注册中心 - 管理所有启用的选股策略"""

    def __init__(self, config: Optional[StrategyConfig] = None):
        self.config = config or get_config().strategy
        self.skills_dir = Path(self.config.skills_dir)
        self._validate()

    def _validate(self):
        for s in self.config.enabled_strategies:
            skill_path = self.skills_dir / s / "SKILL.md"
            if not skill_path.exists():
                logger.warning(f"策略 Skill 未找到: {s} ({skill_path})")
            else:
                logger.info(f"策略已注册: {s}")

    def list_strategies(self) -> List[Dict]:
        """列出所有已注册策略，附带类型和可执行信息"""
        result = []
        for s in self.config.enabled_strategies:
            skill_path = self.skills_dir / s
            scripts = self._scan_scripts(s)
            priority = PRIORITY_SCRIPTS.get(s)
            has_scripts = len(scripts) > 0
            is_doc_only = (priority is None and not has_scripts)
            info = {
                "name": s,
                "path": str(skill_path),
                "available": skill_path.exists(),
                "scripts": scripts,
                "executable": has_scripts,
                "priority_script": priority,
                "type": "doc-only" if is_doc_only else "script" if has_scripts else "unknown",
            }
            skill_md = skill_path / "SKILL.md"
            if skill_md.exists():
                with open(skill_md, "r") as f:
                    first_line = f.readline().strip().lstrip("#").strip()
                    info["description"] = first_line
            result.append(info)
        return result

    def _scan_scripts(self, strategy_name: str) -> List[str]:
        """扫描 Skill 目录下的真实 Python 脚本"""
        script_dir = self.skills_dir / strategy_name / "scripts"
        if not script_dir.exists():
            return []
        py_files = [
            str(p) for p in script_dir.rglob("*.py")
            if p.name != "__init__.py"
            and "strategy_lab" not in str(p)
        ]
        return py_files

    def find_scripts(self, strategy_name: Optional[str] = None) -> Dict[str, List]:
        targets = (
            [strategy_name] if strategy_name
            else self.config.enabled_strategies
        )
        result = {}
        for s in targets:
            result[s] = self._scan_scripts(s)
        return result

    def _pick_script(self, strategy_name: str) -> Optional[str]:
        """为策略选择合适的执行脚本"""
        priority = PRIORITY_SCRIPTS.get(strategy_name)
        scripts = self._scan_scripts(strategy_name)

        if priority:
            for s in scripts:
                if priority in s or s.endswith(priority):
                    return s
            if scripts:
                return scripts[0]
            return None
        elif scripts:
            return scripts[0]
        else:
            return None

    def execute_strategy(
        self, strategy_name: str, script: Optional[str] = None, args: Optional[List] = None
    ) -> Dict:
        if script is None:
            script_path = self._pick_script(strategy_name)
            if script_path is None:
                return {
                    "strategy": strategy_name,
                    "success": True,
                    "note": "文档型策略，无可执行脚本，需 Agent 直接读取 SKILL.md 使用",
                    "type": "doc-only",
                }
        else:
            script_path = self.skills_dir / strategy_name / "scripts" / script
            if not script_path.exists():
                return {"strategy": strategy_name, "success": False, "error": f"脚本不存在: {script_path}"}
            script_path = str(script_path)

        if not os.path.exists(str(script_path)):
            return {"strategy": strategy_name, "success": False, "error": f"脚本不存在: {script_path}"}

        try:
            cmd = ["python3", str(script_path)] + (args or [])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {
                "strategy": strategy_name,
                "script": os.path.basename(str(script_path)),
                "success": result.returncode == 0,
                "stdout": result.stdout[-3000:],
                "stderr": result.stderr[-1000:],
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"strategy": strategy_name, "success": False, "error": "执行超时"}
        except Exception as e:
            return {"strategy": strategy_name, "success": False, "error": str(e)}

    def run_all_strategies(self) -> Dict[str, Dict]:
        results = {}
        for s in self.config.enabled_strategies:
            logger.info(f"执行策略: {s}")
            results[s] = self.execute_strategy(s)
        return results
