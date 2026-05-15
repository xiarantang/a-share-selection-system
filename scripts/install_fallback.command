#!/bin/bash
# ============================================================
# A 股智能选股系统 — 首次安装 A 股备用数据通道
# ============================================================
# 安装 shouldnotappearcalm/a-share-skill 中的必要 Skill。
# ============================================================

set -e

echo "========================================"
echo "  安装 A 股备用数据通道"
echo "========================================"
echo ""

if ! command -v git &>/dev/null; then
    echo "未找到 git，请先安装 Xcode Command Line Tools 或 Git。"
    echo "可在终端运行：xcode-select --install"
    read -p "按回车键退出..."
    exit 1
fi

SKILL_DIR="$HOME/.agents/skills"
TMP_DIR="$(mktemp -d)"

mkdir -p "$SKILL_DIR"

echo "正在下载 a-share-skill..."
git clone --depth 1 https://github.com/shouldnotappearcalm/a-share-skill.git "$TMP_DIR/a-share-skill"

echo "正在安装数据与策略 Skill..."
for skill in \
    a-share-data \
    a-share-paper-trading \
    a-share-strategy-mainboard-multi-swing-defensive \
    macd-trend-resonance-stock-picker \
    macd-second-golden-cross
do
    rm -rf "$SKILL_DIR/$skill"
    cp -R "$TMP_DIR/a-share-skill/$skill" "$SKILL_DIR/"
done

rm -rf "$TMP_DIR"

echo ""
echo "安装完成。现在可以重新双击 start_ui.command 启动系统。"
echo "说明：如果 akshare 临时不可用，系统会自动使用这个备用数据通道。"
echo ""
read -p "按回车键退出..."
