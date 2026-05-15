#!/bin/bash
# ============================================================
# A 股智能选股系统 — 小白一键启动脚本 (macOS)
# ============================================================
# 双击即可启动。首次运行自动创建虚拟环境并安装依赖。
# 仅供研究学习，不构成投资建议。
# ============================================================

set +e  # 不中途退出，自行处理每个错误

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
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ❌ 未找到 Python3"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  这个系统需要 Python 3.9 以上的版本。"
    echo ""
    echo "  👉 下一步做什么："
    echo "     1. 打开「终端」App（在启动台搜索 Terminal）"
    echo "     2. 粘贴以下命令，按回车："
    echo "        xcode-select --install"
    echo "     3. 如果弹出安装窗口，点击「安装」"
    echo "     4. 安装完成后，重新双击本启动脚本"
    echo ""
    echo "  或者从官网下载安装："
    echo "     https://www.python.org/downloads/"
    echo "     （下载 macOS 安装包，双击安装）"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi
PY_VER=$(python3 --version 2>&1)
echo "  ✅ Python: $PY_VER"

# ---- 2. 检测/创建虚拟环境 ----
echo "▸ 正在检测虚拟环境..."
if [ ! -f ".venv/bin/python" ]; then
    echo "  ⏳ 首次运行，正在创建虚拟环境（约 10 秒）..."
    python3 -m venv .venv 2>&1
    if [ $? -ne 0 ]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  ❌ 虚拟环境创建失败"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "  可能原因：Python 版本太低或安装不完整。"
        echo ""
        echo "  👉 下一步做什么："
        echo "     1. 确认 Python 版本 >= 3.9："
        echo "        打开终端，输入 python3 --version"
        echo "     2. 如果版本太低，从 python.org 下载最新版"
        echo "     3. 安装后重新双击本启动脚本"
        echo ""
        read -p "按回车键退出..."
        exit 1
    fi
    echo "  ✅ 虚拟环境已创建"
else
    echo "  ✅ 虚拟环境已存在"
fi

# ---- 3. 安装/更新依赖 ----
echo "▸ 正在检查依赖..."
.venv/bin/pip install -r requirements-ui.txt -q 2>.pip_err
PIP_RC=$?
if [ $PIP_RC -ne 0 ]; then
    PIP_ERR_MSG=$(cat .pip_err 2>/dev/null | tail -5)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ❌ 依赖安装失败"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  错误信息: $PIP_ERR_MSG"
    echo ""
    echo "  👉 下一步做什么："
    echo "     1. 确认电脑能上网（打开浏览器看看能不能打开网页）"
    echo "     2. 如果是在公司/学校，可能需要设置代理"
    echo "     3. 重新双击本启动脚本再试一次"
    echo "     4. 还是不行？打开「终端」，依次运行："
    echo "        cd $(pwd)"
    echo "        .venv/bin/pip install -r requirements-ui.txt"
    echo "     5. 把报错截图发给懂技术的朋友帮忙看"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi
rm -f .pip_err
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
        echo "  ✅ Streamlit 已在运行中"
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
        echo "  ⚠️  端口 8501 已被其他程序占用，自动切换到端口 $PORT"
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

.venv/bin/streamlit run app.py --server.headless true --server.port $PORT 2>.streamlit_err
ST_RC=$?

if [ $ST_RC -ne 0 ]; then
    ST_ERR_MSG=$(cat .streamlit_err 2>/dev/null | tail -10)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ❌ Streamlit 启动失败"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  错误信息: $ST_ERR_MSG"
    echo ""
    echo "  👉 下一步做什么："
    echo "     1. 确认端口 $PORT 没有被占用"
    echo "     2. 重新双击本启动脚本再试一次"
    echo "     3. 如果还是不行，打开「终端」，运行："
    echo "        cd $(pwd)"
    echo "        .venv/bin/streamlit run app.py --server.headless true --server.port 8501"
    echo "     4. 查看详细报错，按提示处理"
    echo "     5. 遇到问题可查看 docs/TROUBLESHOOTING.md"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi
rm -f .streamlit_err
