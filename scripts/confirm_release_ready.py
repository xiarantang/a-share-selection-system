#!/usr/bin/env python3
"""
P8.7-1 发布前一键验收脚本
=========================
整合所有发布前检查为一个入口，方便每次发布前快速确认系统仍可运行。

用法:
    python3 scripts/confirm_release_ready.py

退出码:
    0  全部通过
    1  任一项失败

免责声明：本系统仅供研究学习，不构成投资建议。
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── 检查项定义 ──────────────────────────────────────────────
# (标签, 命令列表, 期望 exit code, 跳过条件说明或 None)
CHECKS: list = [
    ("app.py 语法检查", ["python3", "-m", "py_compile", "app.py"], 0, None),
    ("P8.3 UI 验收 (44项)", ["python3", "scripts/confirm_p83_ui.py"], 0, None),
    ("P8.4 策略注册验收", ["python3", "scripts/confirm_p84_registry.py"], 0, None),
    ("P8.4 CLI 策略参数验收", ["python3", "scripts/confirm_p84_cli.py"], 0, None),
    ("P8.4 UI 策略选择器验收", ["python3", "scripts/confirm_p84_ui.py"], 0, None),
    ("P8.4 文档验收", ["python3", "scripts/confirm_p84_docs.py"], 0, None),
    ("CLI 选股 (static 10→Top5)", [".venv/bin/python", "main.py", "select", "--universe", "static", "--limit", "10", "--top", "5"], 0, None),
    ("CLI 报告生成", [".venv/bin/python", "main.py", "report"], 0, None),
    ("废弃 API 残留检查 (应为空)", ["rg", "-n", "use_container_width|\\.applymap\\(", "app.py"], 1, None),
    ("文档口径一致性检查", ["python3", "scripts/confirm_docs_consistency.py"], 0, None),
]

PASSED = 0
FAILED = 0
SKIPPED = 0


def _tail(text: str, n: int = 8) -> str:
    """返回文本最后 n 行。"""
    lines = text.strip().splitlines()
    return "\n".join(lines[-n:]) if lines else "(无输出)"


def run_check(label, cmd, expect_rc, skip_reason):
    global PASSED, FAILED, SKIPPED

    if skip_reason:
        SKIPPED += 1
        print(f"  ⏭  {label} — 跳过原因: {skip_reason}")
        return

    # 解析命令：如果第一个元素是相对路径且不在 PATH 中，使用绝对路径
    exe = cmd[0]
    if not Path(exe).is_absolute() and not Path(exe).exists():
        # 尝试从项目根目录解析
        candidate = ROOT / exe
        if candidate.exists():
            cmd = [str(candidate)] + cmd[1:]

    print(f"  ▶  {label} ...")

    try:
        result = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError:
        FAILED += 1
        print(f"  ✗  {label} — 命令不存在: {exe}")
        return
    except subprocess.TimeoutExpired:
        FAILED += 1
        print(f"  ✗  {label} — 超时 (120s)")
        return

    if result.returncode == expect_rc:
        PASSED += 1
        print(f"  ✓  {label} — 通过")
    else:
        FAILED += 1
        last_output = _tail(result.stdout + result.stderr)
        cmd_display = " ".join(cmd)
        print(f"  ✗  {label} — 失败")
        print(f"      命令: {cmd_display}")
        print(f"      期望退出码: {expect_rc}, 实际: {result.returncode}")
        print(f"      输出:\n{last_output}")


def main() -> None:
    print("=" * 60)
    print("发布前一键验收  confirm_release_ready.py")
    print("=" * 60)
    print()

    for label, cmd, expect_rc, skip_reason in CHECKS:
        run_check(label, cmd, expect_rc, skip_reason)

    print()
    print("-" * 60)
    total = PASSED + FAILED + SKIPPED
    print(f"结果: {PASSED} 通过 / {FAILED} 失败 / {SKIPPED} 跳过  (共 {total} 项)")
    print("-" * 60)

    if FAILED > 0:
        print("结论: ✗ 存在失败项，请修复后再发布。")
        sys.exit(1)
    else:
        print("结论: ✓ 全部通过，可以发布。")
        print()
        print("免责声明：本系统仅供研究学习，不构成投资建议。")
        sys.exit(0)


if __name__ == "__main__":
    main()
