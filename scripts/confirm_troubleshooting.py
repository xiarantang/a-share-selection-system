#!/usr/bin/env python3
"""P9.4-4.1 排障体验验收脚本。

独立检查 P9.4 排障增强的稳定性：
- start_ui.command 权限、语法、文案
- app.py 错误提示模式
- docs/TROUBLESHOOTING.md 口径
- docs/USER_GUIDE.md FAQ 覆盖
- 禁词和 fallback 可选口径

不调用网络，不跑选股，不修改文件。
从项目根目录运行：python3 scripts/confirm_troubleshooting.py

免责声明：本系统仅供研究学习，不构成投资建议。
"""

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PASSED = 0
FAILED = 0


def _pass(label: str):
    global PASSED
    PASSED += 1
    print(f"  ✓  {label}")


def _fail(label: str, detail: str):
    global FAILED
    FAILED += 1
    print(f"  ✗  {label} — {detail}")


def read_file(rel_path: str) -> str:
    p = ROOT / rel_path
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def check_keyword_present(label: str, rel_path: str, keyword: str) -> bool:
    text = read_file(rel_path)
    if keyword in text:
        _pass(label)
        return True
    _fail(label, f"在 {rel_path} 中未找到「{keyword}」")
    return False


def check_keyword_absent(label: str, rel_path: str, keyword: str) -> bool:
    text = read_file(rel_path)
    if keyword not in text:
        _pass(label)
        return True
    # 找到则报告行号
    for i, line in enumerate(text.splitlines(), 1):
        if keyword in line:
            _fail(label, f"{rel_path}:{i} 命中「{keyword}」→ {line.strip()[:80]}")
            return False
    _fail(label, f"在 {rel_path} 中命中「{keyword}」")
    return False


def check_regex_absent(label: str, rel_path: str, pattern: str) -> bool:
    text = read_file(rel_path)
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(pattern, line):
            _fail(label, f"{rel_path}:{i} 命中 /{pattern}/ → {line.strip()[:80]}")
            return False
    _pass(label)
    return True


def check_keywords_present(label: str, rel_path: str, keywords: list) -> bool:
    """检查文件中包含所有关键词。"""
    text = read_file(rel_path)
    missing = [kw for kw in keywords if kw not in text]
    if not missing:
        _pass(label)
        return True
    _fail(label, f"在 {rel_path} 中缺失: {missing}")
    return False


def main():
    print("=" * 60)
    print("排障体验验收  confirm_troubleshooting.py")
    print("=" * 60)
    print()

    # ── 1. start_ui.command 权限 ──
    sui = ROOT / "start_ui.command"
    if sui.exists() and os.access(sui, os.X_OK):
        _pass("start_ui.command 可执行权限")
    else:
        _fail("start_ui.command 可执行权限", "文件不存在或无可执行权限")

    # ── 2. start_ui.command 语法 ──
    try:
        result = subprocess.run(
            ["bash", "-n", str(sui)],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            _pass("start_ui.command bash 语法检查")
        else:
            _fail("start_ui.command bash 语法检查", result.stderr.strip()[:120])
    except Exception as e:
        _fail("start_ui.command bash 语法检查", str(e))

    # ── 3. start_ui.command 含主路径关键词 ──
    check_keywords_present(
        "start_ui.command 主路径关键词",
        "start_ui.command",
        ["环境自检", "开始选股"],
    )

    # ── 4. app.py 不含旧直暴露写法 ──
    check_keyword_absent(
        "app.py 无旧直暴露写法",
        "app.py",
        "技术详情:",
    )

    # ── 5. app.py 含折叠提示 ──
    check_keyword_present(
        "app.py 含折叠提示「技术详情（发 Issue 时可截图）」",
        "app.py",
        "技术详情（发 Issue 时可截图）",
    )

    # ── 6. app.py 含 TROUBLESHOOTING 指引 ──
    check_keyword_present(
        "app.py 含 docs/TROUBLESHOOTING.md 指引",
        "app.py",
        "docs/TROUBLESHOOTING.md",
    )

    # ── 7. TROUBLESHOOTING.md 不含旧流程词 ──
    check_keyword_absent(
        "TROUBLESHOOTING.md 无旧流程词「两步开始」",
        "docs/TROUBLESHOOTING.md",
        "两步开始",
    )

    # ── 8. TROUBLESHOOTING.md 不含旧误导说法 ──
    check_keyword_absent(
        "TROUBLESHOOTING.md 无旧误导说法",
        "docs/TROUBLESHOOTING.md",
        "某一个源慢不影响最终结果",
    )

    # ── 9. TROUBLESHOOTING.md 无旧 cd 写法 ──
    check_regex_absent(
        "TROUBLESHOOTING.md 无旧 cd 中文写法",
        "docs/TROUBLESHOOTING.md",
        r"cd （|cd（",
    )

    # ── 10. USER_GUIDE.md FAQ 覆盖关键排障 ──
    check_keywords_present(
        "USER_GUIDE.md FAQ 覆盖关键排障场景",
        "docs/USER_GUIDE.md",
        ["浏览器", "安装失败", "全部失败"],
    )

    # ── 11. PROJECT_STATE.md 记录 P9.4-3.1 或之后 ──
    ps_text = read_file("PROJECT_STATE.md")
    has_341 = "P9.4-3.1" in ps_text or "P9.4-4" in ps_text
    if has_341:
        _pass("PROJECT_STATE.md 记录 P9.4-3.1 或之后状态")
    else:
        _fail("PROJECT_STATE.md 记录 P9.4-3.1 或之后状态", "未找到 P9.4-3.1 或 P9.4-4 记录")

    # ── 12. 禁词检查 ──
    ban_targets = [
        "app.py",
        "start_ui.command",
        "docs/TROUBLESHOOTING.md",
        "docs/USER_GUIDE.md",
    ]
    ban_terms = ["买入", "卖出", "目标价", "收益预测", "买卖建议"]
    ban_ok = True
    for rel_path in ban_targets:
        text = read_file(rel_path)
        for term in ban_terms:
            for i, line in enumerate(text.splitlines(), 1):
                if term in line:
                    print(f"  ✗  禁词「{term}」: {rel_path}:{i} → {line.strip()[:80]}")
                    ban_ok = False
    if ban_ok:
        _pass("产品文件无投资建议类禁词")
    else:
        global FAILED
        FAILED += 1

    # ── 13. fallback 仍是可选表达 ──
    check_regex_absent(
        "无「必须安装 fallback/兜底」表述",
        "docs/TROUBLESHOOTING.md",
        r"必须安装.*(?:fallback|兜底|备用)",
    )

    # ── 汇总 ──
    total = PASSED + FAILED
    print()
    print("-" * 60)
    print(f"结果: {PASSED} 通过 / {FAILED} 失败  (共 {total} 项)")
    print("-" * 60)

    if FAILED == 0:
        print("结论: ✓ 全部通过，排障体验稳定。")
        print("\n免责声明：本系统仅供研究学习，不构成投资建议。")
        sys.exit(0)
    else:
        print("结论: ✗ 存在失败项，请检查排障改动是否回退。")
        sys.exit(1)


if __name__ == "__main__":
    main()
