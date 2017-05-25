#!/usr/bin/env python

import os
import sys
import unittest


sys.path.insert(0, os.path.abspath('..'))


if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(testsuite)
