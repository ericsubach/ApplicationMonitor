import curses
import subprocess
import unittest

from mock import patch, Mock

from test_process import TestProcess
from process import Process

class ProcessTest(unittest.TestCase):
   def setUp(self):
      self.process = Process('FakeProcess', '/Fake/Path', 'FakeLog') #TestProcess()
      
      # Setup mock TestProcess
      # TODO can i patch popen? look up patch...set up to create a mock
   
   @unittest.skip('test')   
   def test_getColor_Off_BlueAndWhite(self):
      tExpected = (curses.COLOR_BLUE, curses.COLOR_WHITE)
      tActual = self.process.getColor()
      self.assertEqual(tExpected, tActual)
   
   #@patch('subprocess.Popen', autospec=True)
   #@patch(subprocess, "Popen")
   def test_start_IsRunning_True(self):
      with patch('subprocess.Popen') as pOpen:
         instance = pOpen.return_value
         pOpen.return_value.poll.return_value = None
         #popen.return_value = Mock()
         #popen.return_value.poll = 3
         
         self.process.start()
         self.assertEqual('RUN', self.process.getStatus())
      #self.process.start()
      #self.assertEqual('RUN', self.process.getStatus())
   
   @unittest.skip('test')
   def test_stop_StatusAfterStartAndStop_Off(self):
      self.process.start()
      self.process.stop()
      self.assertEqual('OFF', self.process.getStatus())

   @unittest.skip('test')
   def test_stop_StatusIfNeverStart_Off(self):
      self.process.stop()
      self.assertEqual('OFF', self.process.getStatus())
   
   @unittest.skip('test')
   def test_getStatus_ProcessDied_Die(self):
      self.process.start()
      self.process.process.kill()
      self.assertEqual('DIE', self.process.getStatus())
      
if __name__ == '__main__':
   unittest.main()
