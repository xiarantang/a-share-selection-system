#!/usr/bin/env python3
"""P10.1-1 release tag/main 状态验收脚本。

检查 release tag (v0.6-rc1)、main 最新提交、远端 tag 之间的一致性：
- 本地 tag 存在且指向正确 commit
- HEAD 与 tag 的关系（可无 tag，这是正常的）
- 远端 tag 存在
- tag 指向的提交内容正确
- tag 到 HEAD 之间无产品代码变更

不接入 confirm_release_ready.py，独立运行。
从项目根目录运行：python3 scripts/confirm_release_state.py
"""

import subprocess
import sys

TAG = "v0.6-rc1"
TAG_COMMIT = "3461390"

# tag 后允许新增的 scripts/ 文件（本脚本自身）
ALLOWED_SCRIPTS = {"scripts/confirm_release_state.py"}

# 不允许出现在 tag..HEAD diff 中的路径前缀/文件
PRODUCT_GUARDS = [
    "app.py",
    "main.py",
    "start_ui.command",
    "data/",
    "strategies/",
    "reports/generator.py",
    "reports/__init__.py",
    "validation/",
]

PASSED = 0
FAILED = 0


def run_git(*args: str) -> tuple[int, str]:
    """运行 git 命令，返回 (returncode, stdout)。"""
    result = subprocess.run(
        ["git"] + list(args),
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.returncode, result.stdout.strip()


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  ✓ {label}")
    else:
        FAILED += 1
        msg = f"  ✗ {label}"
        if detail:
            msg += f" — {detail}"
        print(msg)


def main() -> None:
    global PASSED, FAILED
    PASSED = 0
    FAILED = 0

    print("=" * 60)
    print(f"release tag/main 状态验收  confirm_release_state.py")
    print("=" * 60)
    print()

    # ── 检查 1：本地 tag 存在 ──
    print(f"  ▶ 本地 tag {TAG} 存在 ...")
    rc, out = run_git("tag", "-l", TAG)
    check(f"本地 tag {TAG} 存在", out == TAG,
          f"git tag -l {TAG} 输出为空或异常: {out!r}")

    # ── 检查 2：tag 指向发布 commit ──
    print(f"  ▶ tag {TAG} 指向 commit {TAG_COMMIT} ...")
    rc, out = run_git("tag", "--points-at", TAG_COMMIT)
    has_tag = TAG in out.splitlines() if out else False
    check(f"tag {TAG} 指向 commit {TAG_COMMIT}", has_tag,
          f"git tag --points-at {TAG_COMMIT} 输出: {out!r}")

    # ── 检查 3：HEAD 可无 tag（正常） ──
    print(f"  ▶ HEAD 的 tag 状态 ...")
    rc, out = run_git("tag", "--points-at", "HEAD")
    if out:
        head_tags = [t for t in out.splitlines() if t.strip()]
        # HEAD 有 tag 也是可以的（如果 main 没有新提交）
        check("HEAD tag 状态", True)
        print(f"      HEAD 指向 tag: {', '.join(head_tags)}")
    else:
        # HEAD 无 tag 是正常的（main 在 tag 后有文档提交）
        check("HEAD 无 tag（正常：main 在 tag 后有文档提交）", True)

    # ── 检查 4：远端 tag 存在 ──
    print(f"  ▶ 远端 tag {TAG} 存在 ...")
    rc, out = run_git("ls-remote", "--tags", "origin", TAG)
    has_remote = f"refs/tags/{TAG}" in out if out else False
    check(f"远端 tag {TAG} 存在", has_remote,
          f"git ls-remote --tags origin {TAG} 输出为空或异常: {out!r}")

    # ── 检查 5：tag 指向的提交内容 ──
    print(f"  ▶ tag {TAG} 指向的提交内容 ...")
    rc, out = run_git("show", "--stat", "--oneline", "--no-patch", TAG)
    tag_ok = TAG_COMMIT in out if out else False
    check(f"tag {TAG} 指向 commit {TAG_COMMIT}", tag_ok,
          f"git show 输出中未找到 {TAG_COMMIT}: {out[:120]!r}")

    # ── 检查 6：tag 到 HEAD 之间无产品代码变更 ──
    print(f"  ▶ tag..HEAD diff 无产品代码变更 ...")
    rc, out = run_git("diff", f"{TAG}..HEAD", "--name-status")
    if rc != 0:
        check("tag..HEAD diff 可执行", False,
              f"git diff {TAG}..HEAD 失败: returncode={rc}")
    else:
        violations = []
        if out:
            for line in out.splitlines():
                parts = line.strip().split("\t")
                if len(parts) < 2:
                    continue
                filepath = parts[-1]
                # 检查是否为产品代码文件
                for guard in PRODUCT_GUARDS:
                    if filepath.startswith(guard) or filepath == guard:
                        violations.append(filepath)
                        break
                # scripts/ 特殊处理：允许本脚本自身
                if filepath.startswith("scripts/"):
                    if filepath not in ALLOWED_SCRIPTS:
                        violations.append(filepath)
        if violations:
            check("tag..HEAD diff 无产品代码变更", False,
                  f"发现不允许的文件: {', '.join(violations)}")
        else:
            check("tag..HEAD diff 无产品代码变更", True)

    # ── 汇总 ──
    print()
    print("-" * 60)
    total = PASSED + FAILED
    print(f"结果: {PASSED} 通过 / {FAILED} 失败  (共 {total} 项)")
    print("-" * 60)

    if FAILED == 0:
        print(f"结论: ✓ 全部通过，release tag/main 状态一致。")
        print()
        print("免责声明：本系统仅供研究学习，不构成投资建议。")
        sys.exit(0)
    else:
        print(f"结论: ✗ {FAILED} 项未通过，请检查 release tag/main 状态。")
        sys.exit(1)


if __name__ == "__main__":
    main()
