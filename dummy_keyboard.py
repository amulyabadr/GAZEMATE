"""
Dummy Keyboard for Testing
Provides keyboard keys for testing dwell click
"""

class Key:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def contains(self, cx, cy):
        return (self.x <= cx <= self.x + self.w) and \
               (self.y <= cy <= self.y + self.h)

def create_dummy_keyboard():
    """Create a simple QWERTY keyboard layout"""
    keys = []
    layout = [
        ['Q','W','E','R','T','Y','U','I','O','P'],
        ['A','S','D','F','G','H','J','K','L'],
        ['Z','X','C','V','B','N','M'],
        ['Space', 'Speak', 'Clear', 'SOS']
    ]
    
    y = 100
    for row in layout:
        x = 50
        for text in row:
            keys.append(Key(text, x, y, 50, 50))
            x += 55
        y += 55
    
    return keys