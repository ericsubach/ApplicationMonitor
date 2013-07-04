import curses
import math

from curses_printable import CursesPrintable
from rectangle import Rectangle

# Vertical scroll list.
class ScrollableList(object):
   def __init__(self, aWindowObject, aRectangle, aScrollKeysOrd=(curses.KEY_UP, curses.KEY_DOWN), aTitle=''):
      self.title = aTitle
      self.scrollKeys = aScrollKeysOrd
      self.rectangle = aRectangle
      self.viewRectangle = Rectangle(0, 0, aRectangle.width-1, aRectangle.height-1)
      # List of NCursesPrintable objects.
      self.content = []
      self.screen = aWindowObject
   
   def handleInput(self, aInput):
      if aInput == self.scrollKeys[0]:
         self.scrollUp()
      elif aInput == self.scrollKeys[1]:
         self.scrollDown()
      
   def scrollUp(self, aNumLines=1):
      self.scroll(1*aNumLines)
   
   def scrollDown(self, aNumLines=1):
      self.scroll(-1*aNumLines)
   
   # Positive number = up; negative number = down
   def scroll(self, aNumLines):
      tTempPos = self.viewRectangle.y - aNumLines
      
      # Ensure we can scroll.
      if (tTempPos >= 0) and (tTempPos + self.viewRectangle.height) <= len(self.content):
         self.viewRectangle.y = tTempPos
   
   def draw(self):
      self.drawContent()
      self.drawBorder()
      # Draw scrollbar on top of border.
      if self.shouldShowScrollbar():
         self.drawScrollbar()
   
   def shouldShowScrollbar(self):
      if len(self.content) > self.viewHeight:
         return True
      else:
         return False
   
   def drawBorder(self):
      tUpperLeft = (self.rectangle.y, self.rectangle.x)
      tUpperRight = (self.rectangle.y, self.rectangle.x+self.rectangle.width)
      tLowerLeft = (self.rectangle.y+self.rectangle.height, self.rectangle.x)
      tLowerRight = (self.rectangle.y+self.rectangle.height, self.rectangle.x+self.rectangle.width)
      self.screen.vline(tUpperLeft[0], tUpperLeft[1], curses.ACS_VLINE, self.rectangle.height)
      self.screen.hline(tUpperLeft[0], tUpperLeft[1], curses.ACS_HLINE, self.rectangle.width)
      self.screen.hline(tLowerLeft[0], tLowerLeft[1], curses.ACS_HLINE, self.rectangle.width)
      self.screen.vline(tUpperRight[0], tUpperRight[1], curses.ACS_VLINE, self.rectangle.height)
      self.screen.addch(tUpperLeft[0], tUpperLeft[1], curses.ACS_ULCORNER)
      self.screen.addch(tUpperRight[0], tUpperRight[1], curses.ACS_URCORNER)
      self.screen.addch(tLowerRight[0], tLowerRight[1], curses.ACS_LRCORNER)
      self.screen.addch(tLowerLeft[0], tLowerLeft[1], curses.ACS_LLCORNER)
   
   def drawScrollbar(self):
      self.drawBarOutline()
      self.drawBar()
      
   def drawBarOutline(self):
      tBarOutlineYMin = self.rectangle.y + 1
      tBarOutlineYMax = self.rectangle.y + self.viewHeight + 1
      
      tX = self.rectangle.x + self.barXPos()
      for tY in range(tBarOutlineYMin, tBarOutlineYMax):
         curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
         self.screen.addstr(tY, tX, ' ', curses.color_pair(1))
   
   def drawBar(self):
      tBarSize = self.calculateBarSize()
      tBarYMin = self.calculateBarYMin()+1
      
      tX = self.barXPos()
      for tY in range(tBarYMin, tBarYMin + tBarSize):
         curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
         self.screen.addstr(tY, tX, ' ', curses.color_pair(2))
   
   def drawContent(self):
      # Only draw viewable content.
      tStart = self.viewPos
      tEnd = tStart + self.viewHeight
      tViewable = self.content[tStart:tEnd]
      for tY, tCursesPrintable in enumerate(tViewable, start=1):
         tTransformedY = self.rectangle.y + tY
         tTransformedX = self.rectangle.x + 1
         # Clear line.
         self.screen.addstr(tTransformedY, tTransformedX, ' '*self.viewRectangle.width)
         tCursesPrintable.printAtLine(self.screen, tTransformedY, tTransformedX)
   
   # Get the view rectangle of the content (the visible rectangle, 
   # excluding the border).
   #def viewRectangle(self):
   #   pass
   
   def barBounds(self):
      return (self.calculateBarSize(), self.calculateBarYMin())
   
   def calculateBarSize(self):
      tBarSize = 1
      try:
         tBarSize = (float(float(self.viewHeight) / len(self.content)) * self.viewHeight)
         tBarSize = math.trunc(tBarSize)
      except:
         # Divide-by-zero
         tBarSize = 1
      
      if tBarSize < 1:
         tBarSize = 1
      
      return tBarSize
   
   def calculateBarYMin(self):
      tPosPercentageOfTotal = 0
      try:
      # - self.viewHeight()
         #print self.calculateBarSize()
         tPosPercentageOfTotal = (float(self.viewPos) / (len(self.content) - self.viewHeight))
         #tPosPercentageOfTotal = math.trunc(tPosPercentageOfTotal)
         #self.screen.addstr(0, 0, str(tPosPercentageOfTotal))
      except:
         # Divide-by-zero
         tPosPercentageOfTotal = 0
      
      if tPosPercentageOfTotal < 0:
         tPosPercentageOfTotal = 0
      
      # TODO make some of these calculations solely on the number of buffer lines (self.content) and the current position
      # at 100% when len(self.content) - (self.viewPos() + self.viewHeight()) == 0
      # equivalently when len(self.content) - self.viewPos() == self.viewHeight()
      #
      # len(self.content) - self.viewHeight() = whole
      # self.viewPos() = part
      tBarYMin = tPosPercentageOfTotal * (self.viewHeight - self.calculateBarSize())
      tBarYMin = math.trunc(tBarYMin)
      
      return tBarYMin
   
   # 0-based indices.
   def setContentLine(self, aLineNum, aCursesPrintable):
      # TODO extend content if line not yet given
      #self.content[aLineNum] = aCursesPrintable
      self.content.append(aCursesPrintable)
   
   #def setRectange(self):
   #   pass
   
   def barXPos(self):
      return self.rectangle.width
   
   # Height of just the content pane (excludes the border).
   @property
   def viewHeight(self):
      return self.viewRectangle.height

   @property
   def viewPos(self):
      return self.viewRectangle.y
