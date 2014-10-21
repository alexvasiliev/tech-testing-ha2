#!/usr/bin/env python2

import sys
import unittest
#from tests.example_test import ExampleTest
from tests.tests import TestCase


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(TestCase),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
