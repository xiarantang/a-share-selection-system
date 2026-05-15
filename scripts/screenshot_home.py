"""P7.7 验收截图脚本 — 生成首页和结果页截图到 docs/screenshots/。

用法:
    python scripts/screenshot_home.py               # 默认 localhost:8501
    python scripts/screenshot_home.py --port 8502   # 指定端口
    python scripts/screenshot_home.py --help        # 查看帮助

要求: Streamlit 已在运行，Playwright 已安装，系统 Chrome 可用。
输出: docs/screenshots/home.png + docs/screenshots/result.png
"""
import argparse
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = PROJECT_ROOT / "docs" / "screenshots"
HOME_PATH = SCREENSHOT_DIR / "home.png"
RESULT_PATH = SCREENSHOT_DIR / "result.png"


def check_keywords(body: str, label: str, keywords: list[str]) -> dict[str, bool]:
    """检测关键词是否在页面文本中。"""
    return {kw: kw in body for kw in keywords}


def main(port: int = 8501, timeout_sec: int = 120):
    url = f"http://localhost:{port}"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        # ---- 1. 首页截图 ----
        print(f"▸ 打开 {url} ...")
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(5)
        page.screenshot(path=str(HOME_PATH), full_page=True)
        home_text = page.inner_text("body")
        print(f"  首页截图 → {HOME_PATH} ({len(home_text)} 字符)")

        home_checks = check_keywords(home_text, "首页", [
            "A股智能选股系统", "开始选股", "可以开始选股",
            "首次使用检查", "免责声明", "四步完成选股",
        ])
        for kw, ok in home_checks.items():
            print(f"  {'✅' if ok else '❌'} {kw}")

        # ---- 2. 点击开始选股 ----
        print("▸ 点击「开始选股」...")
        page.click("button:has-text('开始选股')")
        print(f"  等待选股完成（最多 {timeout_sec} 秒）...")
        try:
            page.wait_for_selector("div.stAlert[data-testid='stSuccess']", timeout=timeout_sec * 1000)
            print("  ✅ 检测到选股完成")
        except Exception:
            print("  ⚠️ 超时未检测到 success，继续截图")

        time.sleep(8)  # 等 Streamlit 渲染稳定

        # ---- 3. 结果页截图 ----
        page.screenshot(path=str(RESULT_PATH), full_page=True)
        result_text = page.inner_text("body")
        print(f"  结果页截图 → {RESULT_PATH} ({len(result_text)} 字符)")

        result_checks = check_keywords(result_text, "结果页", [
            "选股完成", "候选表格", "数据区间", "覆盖不全",
            "验证摘要", "整体质量", "strong_watch", "免责声明",
        ])
        for kw, ok in result_checks.items():
            print(f"  {'✅' if ok else '❌'} {kw}")

        browser.close()

    # 汇总
    all_ok = all(home_checks.values()) and all(result_checks.values())
    print(f"\n{'='*40}")
    print(f"  {'✅ 验收截图完成' if all_ok else '⚠️ 部分关键词未检出，请检查截图'}")
    print(f"  首页: {HOME_PATH}")
    print(f"  结果: {RESULT_PATH}")
    print(f"{'='*40}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P7.7 验收截图脚本")
    parser.add_argument("--port", type=int, default=8501, help="Streamlit 端口 (默认 8501)")
    parser.add_argument("--timeout", type=int, default=120, help="选股超时秒数 (默认 120)")
    args = parser.parse_args()
    raise SystemExit(main(port=args.port, timeout_sec=args.timeout))
