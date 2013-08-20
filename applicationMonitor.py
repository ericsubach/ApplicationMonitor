#!/usr/bin/env python

"""Provides the ability to interactively start/stop all the programs needed 
in a system."""

__author__ = 'eric.subach@gmail.com (Eric Subach)'

import os
import os.path
import sys

# Append relative path to libraries.
tPathsToAppend = [
                  'lib',
                  'test',
                  'test/class',
                  'test/unit',
                 ]

for tPath in tPathsToAppend:
   sys.path.append(os.path.join(os.path.dirname(__file__), tPath))

from monitor import Monitor
from process import Process

def main():
   ensureMinPythonRequirement()
   
   tProcesses = createProcesses()
   
   #tProcesses = [(elem, elem) for elem in tProcesses]

   from compiler.ast import flatten
   tProcesses = flatten(tProcesses)
   
   tCommands = createCommands()
   
   tHarness = Monitor(tProcesses, tCommands)

   #import time
   #time.sleep(5)
   #while 1:
   #   pass
   
   try:
      tHarness.run()
   except Exception as tException:
      if not __debug__:
         print tException
      else:
         raise

def ensureMinPythonRequirement():
   if sys.version_info[0] != 2 or sys.version_info[1] < 7:
      print('Requires Python >= 2.7')
      sys.exit(1)

def createProcesses():
   tStatusXPos = 32
   tProcess1 = Process('Process 1', 'python ./lib/test_process_1.py', 'process1', tStatusXPos)
   tProcess2 = Process('Process #2', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess3 = Process('Process #3', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess4 = Process('Process #4', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess5 = Process('Process #5', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess6 = Process('Process #6', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess7 = Process('Process #7', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess8 = Process('Process #8', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess9 = Process('Process #9', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess10 = Process('Process #10', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess11 = Process('Process #11', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess12 = Process('Process #12', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess13 = Process('Process #13', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess14 = Process('Process #14', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   tProcess15 = Process('Process #15', 'python ./lib/test_process_2.py', 'process2', tStatusXPos)
   
   tProcesses = [ tProcess1, tProcess2, tProcess3, tProcess4, tProcess5, tProcess6, tProcess7, tProcess8, tProcess9, tProcess10, tProcess11, tProcess12, tProcess13, tProcess14, tProcess15]
   return tProcesses

def createCommands():
   tCommands = []

   return tCommands

if __name__ == '__main__':
   main()
