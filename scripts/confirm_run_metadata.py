#!/usr/bin/env python3
"""P9.3-4.1 run_metadata 复盘记录验收脚本。

独立验收 selection_latest.json 中 run_metadata 的结构与关键内容。
不接入发布前一键验收（留到 P9.3-4.2）。

检查内容：
1. CLI 选股后 JSON 顶层存在 run_metadata
2. 9 个必需字段：generated_at / entrypoint / command / params / strategy /
   data_summary / result_summary / report_path / selection_path
3. data_summary.data_source_dist 为 dict
4. data_summary.rows_summary 包含 min/max/avg/count
5. result_summary 包含 total / success / top_score / avg_score
6. entrypoint 为 "cli"，command 含 main.py select
7. params 包含 universe=static / limit=10 / top=5
8. selection_path 指向的文件存在
9. report_path 可为空（报告尚未生成不算失败）

从项目根目录运行：python3 scripts/confirm_run_metadata.py

免责声明：本系统仅供研究学习，不构成投资建议。
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SELECTION_JSON = ROOT / "reports" / "output" / "selection_latest.json"

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


def _run_select():
    """调用 CLI 最小链路生成选股 JSON。"""
    print("  ▶  CLI 选股 (static 10→Top5) ...")
    result = subprocess.run(
        [".venv/bin/python", "main.py", "select",
         "--universe", "static", "--limit", "10", "--top", "5"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        print(f"  ✗  CLI 选股失败 (exit {result.returncode})")
        print(f"      {result.stdout[-200:] if result.stdout else ''}")
        print(f"      {result.stderr[-200:] if result.stderr else ''}")
        sys.exit(1)
    print("  ✓  CLI 选股完成")


def _load_json() -> dict:
    """加载 selection_latest.json。"""
    if not SELECTION_JSON.exists():
        _fail("JSON 文件存在", f"{SELECTION_JSON} 不存在")
        sys.exit(1)
    with open(SELECTION_JSON, encoding="utf-8") as f:
        return json.load(f)


def main():
    global PASSED, FAILED

    print("=" * 60)
    print("run_metadata 复盘记录验收  confirm_run_metadata.py")
    print("=" * 60)
    print()

    # Step 1: 生成选股 JSON
    _run_select()

    # Step 2: 加载 JSON
    data = _load_json()

    # Step 3: 顶层 run_metadata 存在
    rm = data.get("run_metadata")
    if rm is None:
        _fail("run_metadata 存在", "JSON 顶层无 run_metadata 字段")
        _print_summary()
        sys.exit(1)
    _pass("run_metadata 顶层字段存在")

    # Step 4: 9 个必需字段
    required_fields = [
        "generated_at", "entrypoint", "command", "params",
        "strategy", "data_summary", "result_summary",
        "report_path", "selection_path",
    ]
    for field in required_fields:
        if field in rm:
            _pass(f"字段 {field} 存在")
        else:
            _fail(f"字段 {field} 存在", "缺失")

    # Step 5: entrypoint
    if rm.get("entrypoint") == "cli":
        _pass("entrypoint == cli")
    else:
        _fail("entrypoint == cli", f"实际值: {rm.get('entrypoint')!r}")

    # Step 6: command 含 main.py select
    cmd = rm.get("command", "")
    if "main.py" in cmd and "select" in cmd:
        _pass("command 含 main.py select")
    else:
        _fail("command 含 main.py select", f"实际值: {cmd!r}")

    # Step 7: params 关键值
    params = rm.get("params", {})
    param_checks = [
        ("universe", "static"),
        ("limit", 10),
        ("top", 5),
    ]
    for key, expected in param_checks:
        actual = params.get(key)
        if actual == expected:
            _pass(f"params.{key} == {expected!r}")
        else:
            _fail(f"params.{key} == {expected!r}", f"实际值: {actual!r}")

    # Step 8: data_summary.data_source_dist 为 dict
    ds = rm.get("data_summary", {})
    dsd = ds.get("data_source_dist")
    if isinstance(dsd, dict) and len(dsd) > 0:
        _pass(f"data_summary.data_source_dist 为 dict ({len(dsd)} 项)")
    else:
        _fail("data_summary.data_source_dist 为 dict", f"实际类型: {type(dsd).__name__}, 值: {dsd!r}")

    # Step 9: data_summary.rows_summary 包含 min/max/avg/count
    rs = ds.get("rows_summary", {})
    rs_fields = ["min", "max", "avg", "count"]
    rs_ok = all(f in rs for f in rs_fields)
    if rs_ok:
        _pass(f"data_summary.rows_summary 含 {rs_fields}")
    else:
        missing = [f for f in rs_fields if f not in rs]
        _fail("data_summary.rows_summary 完整", f"缺失: {missing}")

    # Step 10: result_summary 关键字段
    rsum = rm.get("result_summary", {})
    rsum_fields = ["total", "success", "top_score", "avg_score"]
    rsum_ok = all(f in rsum for f in rsum_fields)
    if rsum_ok:
        _pass(f"result_summary 含 {rsum_fields}")
    else:
        missing = [f for f in rsum_fields if f not in rsum]
        _fail("result_summary 关键字段", f"缺失: {missing}")

    # Step 11: selection_path 指向的文件存在
    sel_path = rm.get("selection_path", "")
    if sel_path and (ROOT / sel_path).exists():
        _pass(f"selection_path 文件存在 ({sel_path})")
    else:
        _fail("selection_path 文件存在", f"路径: {sel_path!r}")

    # Step 12: report_path 可为空（报告尚未生成不算失败）
    rp = rm.get("report_path", "")
    if not rp:
        _pass("report_path 为空（报告尚未生成，不判失败）")
    elif (ROOT / rp).exists():
        _pass(f"report_path 文件存在 ({rp})")
    else:
        _fail("report_path 文件存在", f"路径: {rp!r} 不存在")

    # 汇总
    _print_summary()


def _print_summary():
    total = PASSED + FAILED
    print()
    print("-" * 60)
    print(f"结果: {PASSED} 通过 / {FAILED} 失败  (共 {total} 项)")
    print("-" * 60)

    if FAILED == 0:
        print("结论: ✓ 全部通过，run_metadata 结构与内容稳定。")
        print("\n免责声明：本系统仅供研究学习，不构成投资建议。")
        sys.exit(0)
    else:
        print("结论: ✗ 存在失败项，请检查 run_metadata 生成逻辑。")
        sys.exit(1)


if __name__ == "__main__":
    main()
