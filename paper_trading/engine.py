"""
模拟交易层：A 股模拟盘引擎
===========================
封装 a-share-paper-trading Skill，提供模拟下单、持仓管理、策略验证。
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from config.settings import PaperTradingConfig, get_config


class PaperTradingEngine:
    """A 股模拟盘引擎"""

    def __init__(self, config: Optional[PaperTradingConfig] = None):
        self.config = config or get_config().paper_trading
        self.skill_dir = Path(os.path.expanduser(
            "~/.agents/skills/a-share-paper-trading"
        ))
        self.accounts: Dict[str, Dict] = {}
        self._load_accounts()

    def _skill_scripts_dir(self) -> Path:
        return self.skill_dir / "scripts"

    def _run_skill_script(self, script_name: str, *args) -> Dict:
        """运行 paper-trading Skill 的脚本"""
        script_path = self._skill_scripts_dir() / script_name
        if not script_path.exists():
            return {"error": f"Script not found: {script_path}"}

        try:
            cmd = ["python3", str(script_path)] + list(args)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"error": "执行超时"}
        except Exception as e:
            return {"error": str(e)}

    # ---- 账户管理 ----

    def create_account(
        self, account_id: str = "default", initial_cash: Optional[float] = None
    ) -> Dict:
        """创建模拟账户"""
        cash = initial_cash or self.config.initial_cash
        account = {
            "id": account_id,
            "initial_cash": cash,
            "cash": cash,
            "positions": {},
            "orders": [],
            "trades": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        self.accounts[account_id] = account
        self._save_accounts()
        logger.info(f"创建账户 {account_id}: 初始资金={cash}")
        return self.get_account_summary(account_id)

    def get_account_summary(self, account_id: str = "default") -> Dict:
        """获取账户摘要"""
        acc = self.accounts.get(account_id, {})
        if not acc:
            return {"error": f"账户不存在: {account_id}"}

        total_market_value = sum(
            pos.get("market_value", 0) for pos in acc.get("positions", {}).values()
        )
        return {
            "account_id": account_id,
            "cash": acc["cash"],
            "positions_value": total_market_value,
            "total_value": acc["cash"] + total_market_value,
            "positions_count": len(acc.get("positions", {})),
            "updated_at": acc.get("updated_at", ""),
        }

    # ---- 下单 ----

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        price: float,
        quantity: int,
        account_id: str = "default",
    ) -> Dict:
        """下限价单"""
        acc = self.accounts.get(account_id)
        if not acc:
            return {"error": f"账户不存在: {account_id}"}

        if side.lower() not in ("buy", "sell"):
            return {"error": "side 必须是 buy 或 sell"}

        # A 股规则校验：100 股整数倍
        if quantity % self.config.lot_size != 0:
            return {"error": f"A股必须以{self.config.lot_size}股整数倍下单"}

        # 买入校验
        if side.lower() == "buy":
            cost = price * quantity
            if cost > acc["cash"]:
                return {"error": f"资金不足: 需要{cost}, 可用{acc['cash']}"}

        # 卖出校验
        if side.lower() == "sell":
            pos = acc["positions"].get(symbol, {})
            available = pos.get("available", 0)
            if quantity > available:
                return {"error": f"持仓不足: 需要{quantity}, 可用{available}"}

        order = {
            "order_id": f"ORD-{len(acc['orders'])+1:06d}",
            "symbol": symbol,
            "side": side,
            "price": price,
            "quantity": quantity,
            "status": "pending",  # pending -> filled -> cancelled
            "created_at": datetime.now().isoformat(),
        }
        acc["orders"].append(order)
        acc["updated_at"] = datetime.now().isoformat()

        logger.info(f"下单: {order['order_id']} {side} {symbol} {quantity}股@{price}")
        return order

    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        market_price: float,
        account_id: str = "default",
    ) -> Dict:
        """下市价单（立即成交）"""
        order_result = self.place_limit_order(symbol, side, market_price, quantity, account_id)
        if "error" in order_result:
            return order_result

        # 立即成交
        order_result["status"] = "filled"
        order_result["filled_price"] = market_price
        order_result["filled_at"] = datetime.now().isoformat()
        self._apply_fill(account_id, order_result)
        return order_result

    def _apply_fill(self, account_id: str, order: Dict):
        """应用成交"""
        acc = self.accounts[account_id]
        symbol = order["symbol"]
        price = order["filled_price"]
        quantity = order["quantity"]
        side = order["side"]

        if side == "buy":
            cost = price * quantity
            acc["cash"] -= cost
            if symbol not in acc["positions"]:
                acc["positions"][symbol] = {
                    "quantity": 0,
                    "avg_cost": 0,
                    "market_value": 0,
                    "available": 0,
                }
            pos = acc["positions"][symbol]
            total_qty = pos["quantity"] + quantity
            pos["avg_cost"] = (
                (pos["avg_cost"] * pos["quantity"] + cost) / total_qty
                if total_qty > 0 else 0
            )
            pos["quantity"] = total_qty
            pos["market_value"] = total_qty * price
            pos["available"] = total_qty  # T+0 简化，暂不考虑 T+1

        elif side == "sell":
            revenue = price * quantity
            acc["cash"] += revenue
            pos = acc["positions"][symbol]
            pos["quantity"] -= quantity
            pos["available"] -= quantity
            pos["market_value"] = pos["quantity"] * price
            if pos["quantity"] <= 0:
                del acc["positions"][symbol]

        acc["updated_at"] = datetime.now().isoformat()
        acc["trades"].append(order)

    def cancel_order(self, order_id: str, account_id: str = "default") -> Dict:
        """撤单"""
        acc = self.accounts.get(account_id, {})
        if not acc:
            return {"error": f"账户不存在: {account_id}"}
        for o in acc["orders"]:
            if o["order_id"] == order_id and o["status"] == "pending":
                o["status"] = "cancelled"
                return {"success": True, "order_id": order_id}
        return {"error": f"无法撤单: {order_id}"}

    # ---- 持仓更新 ----

    def update_positions(
        self, quotes: Dict[str, float], account_id: str = "default"
    ):
        """更新持仓市值"""
        acc = self.accounts.get(account_id)
        if not acc:
            return
        for symbol, price in quotes.items():
            if symbol in acc["positions"]:
                acc["positions"][symbol]["market_value"] = (
                    acc["positions"][symbol]["quantity"] * price
                )
        acc["updated_at"] = datetime.now().isoformat()

    # ---- 持久化 ----

    def _accounts_file(self) -> Path:
        return Path(__file__).parent / "accounts.json"

    def _save_accounts(self):
        with open(self._accounts_file(), "w") as f:
            json.dump(self.accounts, f, ensure_ascii=False, indent=2)

    def _load_accounts(self):
        f = self._accounts_file()
        if f.exists():
            try:
                with open(f) as fp:
                    self.accounts = json.load(fp)
            except Exception:
                self.accounts = {}
