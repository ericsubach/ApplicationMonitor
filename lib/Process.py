import curses
import shlex
import subprocess

#
# RUN, DIE, OFF
#
class Process:
   def __init__(self, aName, aBinaryPath, aLogName):
      self.name = aName
      self.binaryPath = aBinaryPath
      self.status = 'OFF'
      self.process = None

   def getStatus(self):
      if self.process:
         tPoll = self.process.poll()
         if tPoll == None:
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
         return (curses.COLOR_GREEN, curses.COLOR_WHITE)
      elif self.status == 'DIE':
         return (curses.COLOR_RED, curses.COLOR_WHITE)
      elif self.status == 'OFF':
         return (curses.COLOR_BLUE, curses.COLOR_WHITE)
         
   def start(self):
      tArgs = shlex.split(self.binaryPath)
      self.process = self.createProcess(tArgs)
   
   def stop(self):
      if self.process:
         self.process.kill()
         self.process.wait()
   
   # @patch
   def createProcess(self, aArgs):
      return subprocess.Popen(aArgs)
