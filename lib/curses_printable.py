# Line-based printable string. Content should not be drawn outside the line, and not extend very far horizontally.
class CursesPrintable(object):
   def __init__(self):
      pass

   # Note: Curses color pairs not guaranteed to be preserved.
   # Note: There is no safeguard for drawing outside the line.
   def printAtLine(self, aWindowObject, aY, aX):
      pass
