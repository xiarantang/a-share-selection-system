#!/usr/bin/env python3
"""P9.2-1 公开文档口径一致性检查脚本。

检查公开文档是否保持当前口径一致：
- 小白主路径表述
- baostock 数据层表述
- skill_fallback 兜底表述
- 旧流程误导词零命中
- 投资建议措辞禁词零命中
- 免责声明保留

仅做文档文本检查，不调用网络、不跑选股、不检查产品逻辑。
从项目根目录运行：python3 scripts/confirm_docs_consistency.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_file(rel_path: str) -> str:
    p = ROOT / rel_path
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def check_keyword_present(label: str, paths: list[str], keyword: str) -> bool:
    """检查至少一个文件中包含关键词。"""
    for path in paths:
        text = read_file(path)
        if keyword in text:
            return True
    print(f"  ✗ {label}：在 {paths} 中均未找到「{keyword}」")
    return False


def check_keyword_absent(label: str, paths: list[str], keyword: str) -> bool:
    """检查所有文件中均不包含关键词。"""
    ok = True
    for path in paths:
        text = read_file(path)
        for i, line in enumerate(text.splitlines(), 1):
            if keyword in line:
                print(f"  ✗ {label}：{path}:{i} 命中「{keyword}」→ {line.strip()[:80]}")
                ok = False
    if ok:
        return True
    return False


def check_regex_absent(label: str, paths: list[str], pattern: str) -> bool:
    """检查所有文件中均不匹配正则。"""
    ok = True
    for path in paths:
        text = read_file(path)
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(pattern, line):
                print(f"  ✗ {label}：{path}:{i} 命中 /{pattern}/ → {line.strip()[:80]}")
                ok = False
    if ok:
        return True
    return False


def check_disclaimer(label: str, paths: list[str]) -> bool:
    """检查免责声明保留。"""
    phrase = "不构成投资建议"
    ok = True
    for path in paths:
        text = read_file(path)
        if phrase not in text:
            print(f"  ✗ {label}：{path} 中未找到「{phrase}」")
            ok = False
    if ok:
        return True
    return False


def check_fallback_not_required(paths: list[str]) -> bool:
    """检查 skill_fallback 没有被写成启动前提。"""
    forbidden_patterns = [
        r"必须安装.*(?:fallback|兜底|备用)",
        r"先安装.*(?:fallback|兜底|备用)",
        r"安装后.*才能(?:启动|使用|选股)",
    ]
    ok = True
    for path in paths:
        text = read_file(path)
        for i, line in enumerate(text.splitlines(), 1):
            for pat in forbidden_patterns:
                if re.search(pat, line):
                    print(f"  ✗ fallback 非前提：{path}:{i} 命中 /{pat}/ → {line.strip()[:80]}")
                    ok = False
    if ok:
        return True
    return False


def main():
    print("=" * 60)
    print("公开文档口径一致性检查  confirm_docs_consistency.py")
    print("=" * 60)

    results = []

    # ── 1. 小白主路径关键表述 ──
    main_path_docs = [
        "README.md",
        "docs/USER_GUIDE.md",
        "docs/TROUBLESHOOTING.md",
        "PROJECT_STATE.md",
    ]
    main_path_keywords = ["start_ui.command", "选参数", "开始选股", "看结果"]
    for kw in main_path_keywords:
        r = check_keyword_present(
            f"主路径「{kw}」", main_path_docs, kw
        )
        results.append(r)

    # ── 2. baostock 数据层表述 ──
    data_docs = [
        "README.md",
        "docs/USER_GUIDE.md",
        "docs/TROUBLESHOOTING.md",
    ]
    r = check_keyword_present("baostock 数据层", data_docs, "baostock")
    results.append(r)
    r = check_keyword_present("约 570 条日 K", data_docs, "570")
    results.append(r)

    # ── 3. skill_fallback 兜底表述 ──
    all_pub_docs = [
        "README.md",
        "CHANGELOG.md",
        "docs/USER_GUIDE.md",
        "docs/TROUBLESHOOTING.md",
        "docs/MANUAL_UI_CHECKLIST.md",
        "docs/UI_ACCEPTANCE.md",
        "docs/P8_7_RELEASE_REVIEW.md",
        "PROJECT_STATE.md",
    ]
    r = check_keyword_present(
        "skill_fallback 可选兜底", data_docs, "skill_fallback"
    )
    results.append(r)
    r = check_fallback_not_required(all_pub_docs)
    results.append(r)

    # ── 4. 旧流程误导词零命中 ──
    old_terms = ["四步引导", "四步完成", "三步引导", "两步核心", "必须安装备用", "先安装备用"]
    for term in old_terms:
        r = check_keyword_absent(f"旧词「{term}」", all_pub_docs, term)
        results.append(r)

    # ── 5. 投资建议措辞禁词零命中 ──
    ban_terms = ["买入", "卖出", "目标价", "收益预测"]
    for term in ban_terms:
        r = check_keyword_absent(f"禁词「{term}」", all_pub_docs, term)
        results.append(r)

    # ── 6. 免责声明保留 ──
    disclaimer_docs = [
        "README.md",
        "docs/USER_GUIDE.md",
        "docs/P8_7_RELEASE_REVIEW.md",
    ]
    r = check_disclaimer("免责声明", disclaimer_docs)
    results.append(r)

    # ── 汇总 ──
    total = len(results)
    passed = sum(results)
    failed = total - passed

    print()
    print("-" * 60)
    print(f"结果: {passed} 通过 / {failed} 失败  (共 {total} 项)")
    print("-" * 60)

    if failed == 0:
        print("结论: ✓ 全部通过，文档口径一致。")
        print("\n免责声明：本系统仅供研究学习，不构成投资建议。")
        sys.exit(0)
    else:
        print("结论: ✗ 存在不一致项，请修复后再验收。")
        sys.exit(1)


if __name__ == "__main__":
    main()
