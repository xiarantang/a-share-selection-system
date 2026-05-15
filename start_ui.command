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

echo ""
echo "========================================"
echo "  🏦 A 股智能选股系统"
echo "  小白一键选股 · 仅供研究学习"
echo "========================================"
echo ""

# ---- 1. 检测 Python3 ----
echo "▸ 正在检测 Python3..."
if ! command -v python3 &>/dev/null; then
    echo ""
    echo "❌ 未找到 python3，请先安装 Python 3.9+"
    echo ""
    echo "   下载地址：https://www.python.org/downloads/"
    echo "   或通过 Homebrew：brew install python3"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi
echo "  ✅ Python: $(python3 --version)"

# ---- 2. 检测/创建虚拟环境 ----
echo "▸ 正在检测虚拟环境..."
if [ ! -f ".venv/bin/python" ]; then
    echo "  ⏳ 首次运行，正在创建虚拟环境（约 10 秒）..."
    python3 -m venv .venv
    echo "  ✅ 虚拟环境已创建"
else
    echo "  ✅ 虚拟环境已存在"
fi

# ---- 3. 安装/更新依赖 ----
echo "▸ 正在检查依赖..."
.venv/bin/pip install -r requirements-ui.txt -q 2>&1 | tail -1
echo "  ✅ 依赖就绪"

# ---- 4. 检查 Skill fallback ----
FALLBACK_SCRIPT="$HOME/.agents/skills/a-share-data/scripts/fetch_history_fallback.py"
if [ ! -f "$FALLBACK_SCRIPT" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ⚠️  重要：缺少 A 股备用数据通道"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  akshare 在网络不稳定时可能暂时不可用，"
    echo "  备用数据通道可以确保系统仍能正常出结果。"
    echo ""
    echo "  👉 下一步做什么："
    echo "     双击 scripts/install_fallback.command"
    echo "     （安装只需运行一次，约 1 分钟）"
    echo "     安装后重新双击本启动脚本即可。"
    echo ""
    echo "  ⚡ 也可以跳过安装直接继续，但新数据可能拉取失败。"
    echo ""
else
    echo "  ✅ 备用数据通道已安装"
fi

# ---- 5. 端口检测 ----
PORT=8501
if lsof -Pi :$PORT -sTCP:LISTEN -t &>/dev/null; then
    STREAMLIT_PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t | head -1)
    STREAMLIT_CMD=$(ps -p "$STREAMLIT_PID" -o command= 2>/dev/null || echo "")
    if echo "$STREAMLIT_CMD" | grep -q "streamlit"; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  ✅ Streamlit 已在运行中 (PID $STREAMLIT_PID)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "  👉 浏览器打开 http://localhost:$PORT 即可使用。"
        echo ""
        read -p "按回车键退出..."
        exit 0
    else
        PORT=8502
        if lsof -Pi :$PORT -sTCP:LISTEN -t &>/dev/null; then
            PORT=8503
        fi
        echo ""
        echo "  ⚠️  端口 8501 已被占用，自动切换到端口 $PORT"
        echo ""
    fi
fi

# ---- 6. 启动 Streamlit ----
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 正在启动可视化界面..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  👉 浏览器打开 http://localhost:$PORT"
echo "  👉 看到页面后，点击「🚀 开始选股」即可"
echo "  👉 首次选股需要 30-60 秒，请耐心等待"
echo "  👉 按 Ctrl+C 可以停止系统"
echo ""

.venv/bin/streamlit run app.py --server.headless true --server.port $PORT
