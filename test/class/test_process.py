from fake_subprocess import FakeSubprocess
from process import Process

class TestProcess(Process):
   def __init__(self):
      Process.__init__(self, "Test", "./test", "test")
      self.storedProcess = None

   def createProcess(self, aArgs):
      if self.storedProcess:
         return self.storedProcess
      else:
         return FakeSubprocess()

   def setProcess(self, aProcess):
      self.storedProcess = aProcess