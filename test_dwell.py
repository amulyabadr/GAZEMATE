"""
Test Dwell Click Module
"""

import time
from dwell_click import DwellClick

# Dummy key class
class DummyKey:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def contains(self, cx, cy):
        return (self.x <= cx <= self.x + self.w) and \
               (self.y <= cy <= self.y + self.h)

# Create test keys
dummy_keys = [
    DummyKey("H", 100, 100, 60, 60),
    DummyKey("E", 160, 100, 60, 60),
    DummyKey("L", 220, 100, 60, 60),
    DummyKey("O", 280, 100, 60, 60),
]

print("🚀 Testing Dwell Click...")
dwell = DwellClick(dwell_time=700)

print("📌 Test: Looking at 'H' key for 700ms")
print("   Looking at 'H'...")
result = dwell.check(120, 120, dummy_keys)
print(f"   After 0ms: {result} (None expected)")
time.sleep(0.2)

result = dwell.check(120, 120, dummy_keys)
print(f"   After 200ms: {result} (None expected)")
time.sleep(0.2)

result = dwell.check(120, 120, dummy_keys)
print(f"   After 400ms: {result} (None expected)")
time.sleep(0.2)

result = dwell.check(120, 120, dummy_keys)
print(f"   After 600ms: {result} (None expected)")
time.sleep(0.2)

result = dwell.check(120, 120, dummy_keys)
print(f"   After 800ms: {result} (H should be clicked!)")

print("\n✅ Dwell Click test complete!")