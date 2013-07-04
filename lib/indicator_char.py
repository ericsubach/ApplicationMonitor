import curses

from datetime import datetime, timedelta

class IndicatorChar(object):
   def __init__(self):
      self.chars = ['|', '/', '-', '\\']
      self.index = 0
      self.lastChangeTime = datetime.now()
      self.timeDelta = timedelta(milliseconds=500)
   
   def getChar(self):
      tTimeNow = datetime.now()
      if (tTimeNow - self.lastChangeTime) > self.timeDelta:
         self.index = ((self.index + 1) % len(self.chars))
         self.lastChangeTime = tTimeNow
         
      return self.chars[self.index]
