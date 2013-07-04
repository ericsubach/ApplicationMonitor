import curses
import shlex
import subprocess

from curses_printable import CursesPrintable

# TODO redirect output

#
# Process states:
# * RUN
# * DIE
# * OFF
#
class Process(CursesPrintable):
   def __init__(self, aName, aBinaryPath, aLogName, aStatusXPos):
      self.name = aName
      self.binaryPath = aBinaryPath
      self.status = 'OFF'
      self.process = None
      self.statusXPos = aStatusXPos

   def getStatus(self):
      if self.process:
         tPoll = self.process.poll()
         if tPoll is None:
            self.status = 'RUN'
         elif tPoll < 0 or tPoll > 0:
            self.status = 'DIE'
         elif tPoll == 0:
            self.status = 'OFF'
      else:
         self.status = 'OFF'
      
      return self.status
         
   def getColor(self):
      if self.status == 'RUN':
         return (3, curses.COLOR_GREEN, curses.COLOR_WHITE)
      elif self.status == 'DIE':
         return (4, curses.COLOR_RED, curses.COLOR_WHITE)
      elif self.status == 'OFF':
         return (5, curses.COLOR_BLUE, curses.COLOR_WHITE)
         
   def start(self):
      # Don't start twice.
      if (self.process is None) or (self.process.poll() is not None):
         tArgs = shlex.split(self.binaryPath)
         self.process = self.createProcess(tArgs)
   
   def stop(self):
      if self.process:
         self.process.kill()
         # TODO possibly use communicate instead of wait...maybe OS deadlock
         #self.process.wait()
         self.process.communicate()
         self.process = None
   
   # @patch
   def createProcess(self, aArgs):
      return subprocess.Popen(aArgs)
      
   def printAtLine(self, aWindowObject, aY, aX):
      #tStatusFormatted = '[' + '{:^5}'.format(self.getStatus()) + ']'
      tStatusFormatted = '[{:^5}]'.format(self.getStatus())
      
      tColor = self.getColor()
      curses.init_pair(tColor[0], tColor[1], tColor[2])
      
      aWindowObject.addstr(aY, aX, self.name)
      aWindowObject.addstr(
         aY, self.statusXPos, tStatusFormatted, curses.color_pair(tColor[0]))
