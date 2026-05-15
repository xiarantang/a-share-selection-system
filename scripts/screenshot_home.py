"""截图 Streamlit 首页（使用系统 Chrome）。"""
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8501", wait_until="networkidle", timeout=30000)
    time.sleep(5)
    page.screenshot(path="/tmp/p76_home_v2.png", full_page=True)
    title = page.title()
    body_text = page.inner_text("body")[:3000]
    print(f"TITLE: {title}")
    print("---BODY PREVIEW---")
    print(body_text)
    browser.close()
    print("DONE")
