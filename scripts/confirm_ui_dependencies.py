"""P8.2-4 依赖验收：requirements-ui.txt含baostock，.venv可import"""
import sys, importlib
from pathlib import Path

ok = True
txt = Path("requirements-ui.txt").read_text()
if "baostock" not in txt:
    print("❌ requirements-ui.txt 无 baostock")
    ok = False
else:
    print("✅ requirements-ui.txt 含 baostock")

for mod in ("baostock", "streamlit"):
    try:
        importlib.import_module(mod)
        print(f"✅ .venv 可 import {mod}")
    except ImportError:
        print(f"❌ .venv 无法 import {mod}")
        ok = False

print(f"\n{'✅ 全通过' if ok else '❌ 有失败'}")
sys.exit(0 if ok else 1)
