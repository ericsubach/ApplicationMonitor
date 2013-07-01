#!/usr/bin/env python

"""Provides the ability to start/stop all the programs needed in a system."""

__author__ = 'subach.code@gmail.com (Eric Subach)'

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

from Monitor import Monitor
from Process import Process

tProcess1 = Process('Process 1', 'python ./lib/testProcess1.py', 'process1')
tProcess2 = Process('Process 2', 'python ./lib/testProcess2.py', 'process2')
tProcesses = [ tProcess1, tProcess2 ]

tHarness = Monitor(tProcesses)
tHarness.run()
