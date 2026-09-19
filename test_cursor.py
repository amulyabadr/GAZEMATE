"""
Test Cursor Control Module
"""

import time
from cursor_control import CursorControl

print("🚀 Testing Cursor Control...")
cursor = CursorControl()

print("📌 Moving to (100, 100)")
cursor.move(100, 100)
time.sleep(1)

print("📌 Moving to (500, 300)")
cursor.move(500, 300)
time.sleep(1)

print("📌 Moving to (1000, 500)")
cursor.move(1000, 500)
time.sleep(1)

print("✅ Cursor Control test complete!")