#!/usr/bin/env python

import os
import os.path
import sys
import unittest

# Append relative path to libraries.
tPathsToAppend = [
                  'lib',
                  'test',
                  'test/class',
                  'test/unit',
                 ]

for tPath in tPathsToAppend:
   sys.path.append(os.path.join(os.path.dirname(__file__), tPath))

from test.unit.process_test import *

tSuite = unittest.TestLoader().loadTestsFromTestCase(ProcessTest)
unittest.TextTestRunner(verbosity=2).run(tSuite)
