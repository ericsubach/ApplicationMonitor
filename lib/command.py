from process import Process
from curses_printable import CursesPrintable

class Command(CursesPrintable):
   # TODO option if not need to convert to ordinal
   def __init__(self, aAsciiChar, aDescription):
      self.char = aAsciiChar
      self.description = aDescription
      pass

   def handleInput(self, aInputChar):
      return (aInputChar == ord(self.char))
      
   def do(self, aProcesses):
      pass
   
   def printAtLine(self, aWindowObject, aY, aX):
      tFormattedStr = self.char + ' = ' + self.description
      aWindowObject.addstr(aY, aX, tFormattedStr)


class QuitCommand(Command):
   def __init__(self, aAsciiChar, aDescription):
      super(QuitCommand, self).__init__(aAsciiChar, aDescription)
   
   def do(self, aProcesses):
      # Command handled specially in application loop.
      pass


class StartCommand(Command):
   def __init__(self, aAsciiChar, aDescription):
      super(StartCommand, self).__init__(aAsciiChar, aDescription)
   
   def do(self, aProcesses):
      for tProcess in aProcesses:
         tProcess.start()
      
      
class KillCommand(Command):
   def __init__(self, aAsciiChar, aDescription):
      super(KillCommand, self).__init__(aAsciiChar, aDescription)
   
   def do(self, aProcesses):
      for tProcess in aProcesses:
         tProcess.stop()
      
      
class LogCommand(Command):
   def __init__(self, aAsciiChar, aDescription):
      super(LogCommand, self).__init__(aAsciiChar, aDescription)
   
   def do(self, aProcesses):
      # TODO
      pass

      
class ClearCommand(Command):
   def __init__(self, aAsciiChar, aDescription):
      super(ClearCommand, self).__init__(aAsciiChar, aDescription)
   
   def do(self, aProcesses):
      # TODO
      pass
      
      #tCommandsExtended.append(Command('q', 'quit'))
      #tCommandsExtended.append(Command('s', 'start'))
      #tCommandsExtended.append(Command('k', 'kill'))
      #tCommandsExtended.append(Command('l', 'log (then clear)'))
      #tCommandsExtended.append(Command('c', 'clear log'))
