#!/bin/bash
# ============================================================
# A 股智能选股系统 — 小白一键启动脚本 (macOS)
# ============================================================
# 双击即可启动。首次运行自动创建虚拟环境并安装依赖。
# 仅供研究学习，不构成投资建议。
# ============================================================

set -e

# 动态定位项目根目录（脚本所在目录）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  🏦 A 股智能选股系统"
echo "  仅供研究学习，不构成投资建议"
echo "========================================"
echo ""

# ---- 1. 检测 Python3 ----
if ! command -v python3 &>/dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.9+"
    echo "   下载: https://www.python.org/downloads/"
    echo "   或通过 Homebrew: brew install python3"
    read -p "按回车键退出..."
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# ---- 2. 检测/创建虚拟环境 ----
if [ ! -f ".venv/bin/python" ]; then
    echo "⏳ 首次运行，正在创建虚拟环境..."
    python3 -m venv .venv
    echo "✅ 虚拟环境已创建"
else
    echo "✅ 虚拟环境已存在"
fi

# ---- 3. 安装/更新依赖 ----
echo "⏳ 检查依赖..."
.venv/bin/pip install -r requirements-ui.txt -q 2>&1 | tail -1
echo "✅ 依赖就绪"

# ---- 4. 检查 Skill fallback（非阻塞，只提示） ----
FALLBACK_SCRIPT="$HOME/.agents/skills/a-share-data/scripts/fetch_history_fallback.py"
if [ ! -f "$FALLBACK_SCRIPT" ]; then
    echo ""
    echo "⚠️  数据 fallback 未安装（首次需要）。"
    echo "   选股功能仍可使用本地缓存，但新数据可能无法拉取。"
    echo "   安装方式请见 README.md 中的「Skill 安装」章节。"
    echo ""
fi

# ---- 5. 启动 Streamlit ----
echo "🚀 正在启动可视化界面..."
echo "   👉 浏览器打开 http://localhost:8501"
echo "   👉 按 Ctrl+C 停止"
echo ""

.venv/bin/streamlit run app.py --server.headless true --server.port 8501
