#!/bin/bash
# ============================================================
# A 股智能选股系统 — 可选：安装第三级兜底数据通道
# ============================================================
# 安装 shouldnotappearcalm/a-share-skill 中的必要 Skill。
# 系统已内置 baostock（约 570 条日 K），本脚本为可选的第三级兜底。
# 仅在网络不稳定时需要，安装后可提供多一层保障。
# ============================================================

set +e  # 不中途退出，自行处理每个错误

echo "========================================"
echo "  可选：安装第三级兜底数据通道"
echo "  （skill_fallback，约 1 分钟）"
echo "========================================"
echo ""

# ---- 1. 检测 Git ----
if ! command -v git &>/dev/null; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ❌ 未找到 Git"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  Git 是下载数据的必需工具。"
    echo ""
    echo "  👉 下一步做什么（选一种）："
    echo "     【方法一】安装 Xcode Command Line Tools（推荐）"
    echo "        1. 打开「终端」App"
    echo "        2. 输入以下命令，按回车："
    echo "           xcode-select --install"
    echo "        3. 弹出窗口点击「安装」"
    echo "        4. 安装完成后重新双击本安装脚本"
    echo ""
    echo "     【方法二】从官网下载安装 Git"
    echo "        1. 打开 https://git-scm.com/download/mac"
    echo "        2. 下载安装包，双击安装"
    echo "        3. 安装完成后重新双击本安装脚本"
    echo ""
    echo "     【方法三】通过 Homebrew 安装（如果已有 Homebrew）"
    echo "        在终端输入: brew install git"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi
echo "✅ Git: $(git --version | head -1)"

# ---- 2. 准备安装目录 ----
SKILL_DIR="$HOME/.agents/skills"
echo "▸ 安装目录: $SKILL_DIR"

if ! mkdir -p "$SKILL_DIR" 2>/dev/null; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ❌ 无法创建安装目录"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  目录: $SKILL_DIR"
    echo ""
    echo "  👉 可能原因：该目录被系统保护或权限不足。"
    echo "     1. 打开「终端」，运行以下命令："
    echo "        mkdir -p $SKILL_DIR"
    echo "     2. 如果提示 Permission denied，试试加 sudo："
    echo "        sudo mkdir -p $SKILL_DIR"
    echo "     3. 输入你的 Mac 登录密码（不会显示，正常）"
    echo "     4. 然后重新双击本安装脚本"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

# ---- 3. 下载 Skill ----
TMP_DIR="$(mktemp -d 2>/dev/null)"
if [ -z "$TMP_DIR" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ❌ 无法创建临时目录"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  👉 可能原因：/tmp 目录权限异常。"
    echo "     重启电脑后再试一次。"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

echo "▸ 正在从 GitHub 下载 a-share-skill..."
echo "  （需要联网，约 10-30 秒）"
git clone --depth 1 https://github.com/shouldnotappearcalm/a-share-skill.git "$TMP_DIR/a-share-skill" 2>.git_clone_err
GIT_RC=$?

if [ $GIT_RC -ne 0 ]; then
    GIT_ERR=$(cat .git_clone_err 2>/dev/null | tail -5)
    rm -f .git_clone_err
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ❌ GitHub 下载失败"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  错误信息: $GIT_ERR"
    echo ""
    echo "  👉 下一步做什么："
    echo "     1. 确认电脑能上网（打开浏览器访问 github.com）"
    echo "     2. 如果 GitHub 打不开，可能需要科学上网"
    echo "     3. 如果在公司/学校，检查是否屏蔽了 GitHub"
    echo "     4. 网络正常后重新双击本安装脚本"
    echo "     5. 仍然失败？在浏览器打开这个地址手动下载："
    echo "        https://github.com/shouldnotappearcalm/a-share-skill"
    echo "        点绿色 Code 按钮 → Download ZIP"
    echo "        解压后把 a-share-data 等文件夹拖到 ~/.agents/skills/"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi
rm -f .git_clone_err
echo "  ✅ 下载完成"

# ---- 4. 安装 Skill 文件 ----
echo "▸ 正在安装数据与策略 Skill..."

INSTALL_FAILURES=0
for skill in \
    a-share-data \
    a-share-paper-trading \
    a-share-strategy-mainboard-multi-swing-defensive \
    macd-trend-resonance-stock-picker \
    macd-second-golden-cross
do
    if [ ! -d "$TMP_DIR/a-share-skill/$skill" ]; then
        echo "  ⚠️  跳过不存在的 Skill: $skill"
        continue
    fi
    rm -rf "$SKILL_DIR/$skill" 2>/dev/null
    if ! cp -R "$TMP_DIR/a-share-skill/$skill" "$SKILL_DIR/" 2>/dev/null; then
        echo "  ❌ 安装 $skill 失败（权限不足？）"
        INSTALL_FAILURES=$((INSTALL_FAILURES + 1))
    else
        echo "  ✅ $skill"
    fi
done

# ---- 5. 清理 ----
rm -rf "$TMP_DIR"

# ---- 6. 结果 ----
echo ""
if [ $INSTALL_FAILURES -gt 0 ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ⚠️  部分 Skill 安装失败 ($INSTALL_FAILURES 个)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  可能是权限问题。在终端运行以下命令后重试："
    echo "    sudo chown -R \$(whoami) $SKILL_DIR"
    echo ""
else
    echo "========================================"
    echo "  ✅ 安装完成！"
    echo "========================================"
fi

echo ""
echo "  现在可以重新双击 start_ui.command 启动系统。"
echo "  说明：系统已内置 baostock（约 570 条日 K），skill_fallback 为第三级兜底，"
echo "  在网络不稳定时可提供多一层保障。"
echo ""
read -p "按回车键退出..."
