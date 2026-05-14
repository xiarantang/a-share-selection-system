"""
Agent 层：AI Agent 桥接模块
============================
连接 Agent Skill、MCP 服务和大模型，统一调度分析任务。
"""

import json
import os
from typing import Any, Dict, List, Optional

import requests
from loguru import logger

from config.settings import AgentConfig, get_config


class AgentBridge:
    """Agent 桥接器 - 统一调度 Skill / MCP / LLM"""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or get_config().agent

    # ---- MCP 调用 ----

    def mcp_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        endpoint: Optional[str] = None,
    ) -> Dict:
        """调用 MCP 服务"""
        url = (endpoint or self.config.mcp_cn_stock_url).rstrip("/")
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
            "id": 1,
        }
        try:
            resp = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            if resp.status_code == 200:
                data = resp.json()
                if "result" in data:
                    return {"success": True, "data": data["result"]}
                return {"success": False, "error": data.get("error", "Unknown")}
            return {"success": False, "error": f"HTTP {resp.status_code}"}
        except Exception as e:
            logger.error(f"MCP 调用失败 [{tool_name}]: {e}")
            return {"success": False, "error": str(e)}

    def query_stock_brief(self, stock_name: str) -> Dict:
        """查询股票基本信息（brief 工具）"""
        return self.mcp_call("brief", {"stock_name": stock_name})

    def query_stock_medium(self, stock_name: str) -> Dict:
        """查询股票基本信息+财务（medium 工具）"""
        return self.mcp_call("medium", {"stock_name": stock_name})

    def query_stock_full(self, stock_name: str) -> Dict:
        """查询股票全维度数据（full 工具）"""
        return self.mcp_call("full", {"stock_name": stock_name})

    # ---- LLM 调用 ----

    def llm_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.3,
    ) -> Dict:
        """调用大模型"""
        url = f"{self.config.llm_api_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.llm_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.config.llm_model,
            "messages": messages,
            "temperature": temperature,
        }
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "success": True,
                    "content": data["choices"][0]["message"]["content"],
                    "usage": data.get("usage", {}),
                }
            return {"success": False, "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
        except Exception as e:
            logger.error(f"LLM 调用失败: {e}")
            return {"success": False, "error": str(e)}

    def analyze_stock(self, symbol: str, stock_data: Dict) -> str:
        """让大模型分析单只股票"""
        prompt = f"""你是一位专业的A股投资分析师。请根据以下数据对股票 {symbol} 进行分析：

{json.dumps(stock_data, ensure_ascii=False, indent=2)}

请从以下维度给出分析：
1. 技术面评估（趋势、支撑阻力、指标信号）
2. 估值水平（PE/PB分位）
3. 资金面（主力资金、北向资金）
4. 风险提示
5. 综合评级（买入/持有/卖出）

请用简洁专业的语言回答。"""
        messages = [
            {"role": "system", "content": "你是一位专业的A股投资分析师。"},
            {"role": "user", "content": prompt},
        ]
        result = self.llm_chat(messages)
        return result.get("content", "分析失败") if result.get("success") else f"错误: {result.get('error')}"

    def generate_daily_report(self, market_data: Dict, strategy_results: Dict) -> str:
        """生成每日选股报告"""
        prompt = f"""请根据以下数据生成今日A股选股报告：

## 市场概况
{json.dumps(market_data, ensure_ascii=False, indent=2)[:3000]}

## 策略信号
{json.dumps(strategy_results, ensure_ascii=False, indent=2)[:3000]}

请生成一份结构化的每日选股报告，包括：
1. 市场环境判断
2. 今日推荐标的（按策略评分排序，最多5只）
3. 每只推荐的理由和风险提示
4. 建议仓位
5. 需要关注的变量"""
        messages = [
            {"role": "system", "content": "你是一位专业的A股投资策略分析师，擅长生成选股报告。"},
            {"role": "user", "content": prompt},
        ]
        result = self.llm_chat(messages)
        return result.get("content", "生成失败") if result.get("success") else f"错误: {result.get('error')}"
