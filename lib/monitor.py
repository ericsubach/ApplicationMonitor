import curses
import os
import sys
import thread
import time

#from commands import *
#import commands
import command
from indicator_char import IndicatorChar
from process import Process
from rectangle import Rectangle
from scrollable_list import ScrollableList

class Monitor(object):
   def __init__(self, aProcesses, aCommands):
      self.processes = aProcesses
      self.commands = self.addCommonCommands(aCommands)
      self.indicator = IndicatorChar()
      
      #old_stdout, old_stderr = sys.stdout, sys.stderr
      tDevNull = open(os.devnull, 'w')
      #sys.stdout = tDevNull
      #sys.stderr = tDevNull
      
      # Initialize curses before using screen.
      self.screen = self.initCurses()
      
      self.processList = ScrollableList(self.screen, Rectangle(0, 0, 40, 10))
      for tY, tProcess in enumerate(aProcesses):
         self.processList.setContentLine(tY, tProcess)
      
      self.commandsList = ScrollableList(self.screen, Rectangle(0, 12, 40, 10), aScrollKeysOrd=(curses.KEY_PPAGE, curses.KEY_NPAGE))
      for tY, tCommand in enumerate(aCommands):
         self.commandsList.setContentLine(tY, tCommand)
      
      self.startIndicatorCharThread()

   def printProcesses(self):
      tMaxLen = 0
      for tProcess in self.processes:
         tMaxLen = max(tMaxLen, len(tProcess.name))

      for tIdx, tProcess in enumerate(self.processes):
         tStatus = tProcess.getStatus()
         tStatusFormatted = '[' + '{:^5}'.format(tStatus) + ']'
         
         tColor = tProcess.getColor()
         curses.init_pair(1, tColor[0], tColor[1])
         
         self.screen.addstr(tIdx, 0, tProcess.name)
         self.screen.addstr(
            tIdx, tMaxLen + 2, tStatusFormatted, curses.color_pair(1))
   
   def killProcesses(self):
      for tProcess in self.processes:
         tProcess.stop()
      
   def startProcesses(self):
      for tProcess in self.processes:
         tProcess.start()
      
   def saveLogs(self):
      for tProcess in self.processes:
         tProcess.pid = 1
      
   def clearLogs(self):
      pass
      
   def drawScrollbar(self):
      self.processList.draw()
      
   def drawCommands(self):
      self.commandsList.draw()
      
   def printIndicator(self):
      tChar = self.indicator.getChar()
      self.screen.addstr(11, 0, tChar)
      
   def run(self):
      try:
         # TODO addCommand method.
         tStartPos = 3 #len(self.processes) + 2
         self.screen.addstr(tStartPos,   0, 'q = quit')
         self.screen.addstr(tStartPos+1, 0, 's = start')
         self.screen.addstr(tStartPos+2, 0, 'k = kill')
         self.screen.addstr(tStartPos+3, 0, 'l = log (then clear)')
         self.screen.addstr(tStartPos+4, 0, 'c = clear log')
         
         while 1:
            self.drawScrollbar()
            #self.printIndicator()
            self.drawCommands()

            tChar = self.screen.getch()
            
            # Special case to break program.
            if tChar == ord('q'):
               break
            elif tChar == ord('l'):
               self.saveLogs()
            elif tChar == ord('c'):
               self.clearLogs()
            
            # Scrollable lists need to handle input.
            self.processList.handleInput(tChar)
            self.commandsList.handleInput(tChar)
            
            # Commands need to handle input.
            for tCommand in self.commands:
               if tCommand.handleInput(tChar):
                  tCommand.do(self.processes)
            
      finally:
         self.cleanup()
      
   def initCurses(self):
      tScreen = curses.initscr()
      curses.curs_set(0)        # Invisible cursor
      curses.noecho()           # Don't output keypresses
      curses.cbreak()           # Unbuffered input
      curses.start_color()      # Initialize colors
      tScreen.keypad(1)     # Interpret special keys
      tScreen.timeout(100)  # Non-blocking input (ms)
      return tScreen
      
   def cleanupCurses(self):
      # Reverse settings
      self.screen.keypad(0)
      curses.nocbreak()
      curses.echo()
      curses.curs_set(1)
      curses.endwin()
      
   def cleanup(self):
      self.killProcesses()
      self.drawScrollbar()
      self.screen.refresh()
      self.cleanupCurses()

   def addCommonCommands(self, aCommands):
      tCommandsExtended = aCommands
      tCommandsExtended.append(command.QuitCommand('q', 'quit'))
      tCommandsExtended.append(command.StartCommand('s', 'start'))
      tCommandsExtended.append(command.KillCommand('k', 'kill'))
      #tCommandsExtended.append(Command('l', 'log (then clear)'))
      #tCommandsExtended.append(Command('c', 'clear log'))
      return tCommandsExtended
   
   def startIndicatorCharThread(self):
      thread.start_new(self.indicatorCharThread, ())
   
   # TODO curses is probably not thread safe
   def indicatorCharThread(self):
      while 1:
         self.printIndicator()
         time.sleep(0.2)
         #print self.indicator.getChar()
   