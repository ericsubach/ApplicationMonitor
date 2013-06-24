import curses

from IndicatorChar import IndicatorChar
from Process import Process

class Harness:
   def __init__(self):
      tProcess1 = Process('Process 1', 'python ./lib/testProcess1.py', 'process1')
      tProcess2 = Process('Process 2', 'python ./lib/testProcess2.py', 'process2')
      
      self.processes = [ tProcess1, tProcess2 ]
      self.indicator = IndicatorChar()
      
      self.initCurses()

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
      
   def printIndicator(self):
      tChar = self.indicator.getChar()
      self.screen.addstr(len(self.processes) + 2 + 7, 0, tChar)
      
   def run(self):
      # TODO addCommand method.
      tStartPos = len(self.processes) + 2
      self.screen.addstr(tStartPos,   0, 'q = quit')
      self.screen.addstr(tStartPos+1, 0, 's = start')
      self.screen.addstr(tStartPos+2, 0, 'k = kill')
      self.screen.addstr(tStartPos+3, 0, 'l = log (then clear)')
      self.screen.addstr(tStartPos+4, 0, 'c = clear log')
      
      while 1:
         self.printProcesses()
         self.printIndicator()

         char = self.screen.getch()
         
         if char == ord('q'):
            break
         elif char == ord('k'):
            self.killProcesses()
         elif char == ord('s'):
            self.startProcesses()
         elif char == ord('l'):
            self.saveLogs()
         elif char == ord('c'):
            self.clearLogs()
      
      self.cleanup()
      
   def initCurses(self):
      self.screen = curses.initscr()
      curses.curs_set(0)        # Invisible cursor
      curses.noecho()           # Don't output keypresses
      curses.cbreak()           # Unbuffered input
      curses.start_color()      # Initialize colors
      self.screen.keypad(1)     # Interpret special keys
      self.screen.timeout(500)  # Non-blocking input (ms)
      
      # curses.wrapper(...)
      
   def cleanupCurses(self):
      # Reverse settings
      curses.nocbreak()
      curses.echo()
      curses.curs_set(1)
      self.screen.keypad(0)

      curses.endwin()
      
   def cleanup(self):
      self.killProcesses()
      self.printProcesses()
      self.screen.refresh()
      self.cleanupCurses()
